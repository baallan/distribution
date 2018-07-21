# Controlling LDMSD with libgenders

[This is a work in progress page. check back after 7/23/18]
 
Genders support is useful whether configuring LDMSD for a workstation or an entire cluster.
Table of Contents
1. [Compiling genders support in ldmsd](#compiling-genders-support-in-ldmsd)
1. [Using genders files with ldmsd](#using-genders-files-with-ldmsd)
1. [Local workstation data collector](#local-workstation-data-collector)
    1. [Setting the security key](#setting-the-security-key)
    1. [Starting the collector](#starting-the-collector)
    1. [Checking the result](#checking-the-result)
1. [Defining an aggregator and storage](#defining-an-aggregator-and-storage)
1. [Advanced debugging of ldmsd](#advanced-debugging-of-ldmsd)
1. [Scaling ldmsd](#scaling-ldmsd)
1. [Serrano example](#serrano-example)
1. [Special considerations](#special-considerations)
    1. [Timing](#timing)
    1. [Sysclassib](#sysclassib)
    1. [Opa2](#opa2)
    1. [Procnetdev](#procnetdev)
    1. [Meminfo](#meminfo)
    1. [Splunk followers](#splunk-followers)
1. [Milly example](#milly-example)
    1. [Csv archive](#csv-archive)

This is a simple getting-started tutorial for LDMS 3 versions >= 3.4.7.

## Compiling genders support in ldmsd 

If not building one of the supported HPC rpm configurations, you can enable genders support by including

    --enable-libgenders --enable-genderssystemd

in your configure options. If boost or libgenders are not installed in the normal locations, you
will also need to specify --with-boost=<location> and/or --with-libgenders=<location>.
The needed package files for genders are available in EPEL and other repositories or you can
install from source with https://github.com/chaos/genders. Prebuilt packages are highly recommended.

After completing an installation from source, add its bin directory to your PATH and try running

    ldms-static-test.sh meminfo 

Review the output in ./ldmstest/meminfo/

    meminfo
    ├── logs
    │   ├── 1.txt
    │   ├── 2.txt
    │   └── 3.txt
    ├── run
    │   ├── conf.1
    │   ├── conf.2
    │   ├── conf.3
    │   ├── ldmsd
    │   │   └── secret
    └── store
        └── node
            └── meminfo

## Using genders files with ldmsd

By default, the libgenders-based LDMS systemd script ldmsd.service uses /etc/sysconfig/ldms.d/ClusterGenders/genders.local.
Systemd can manage additional instances where each has a distinct name %I.
The ldmsd@%I.service by default uses /etc/sysconfig/ldms.d/ClusterGenders/genders.%I.
(Here %I is an arbitrary daemon instance name).
The file /etc/sysconfig/ldms.d/ldmsd.local.conf can override the name of the genders file to use.
Similarly, the file /etc/sysconfig/ldms.d/ldmsd.%I.conf can override the name of the genders file used by instance %I.
The LDMS_GENDERS setting in the .conf files overrides the default.

The genders file format is a simple text database associating attributes (with or without explicit values) to hostnames. See ldmsd-genders(8) and ldms-attributes(5) manual pages for details.

## Local workstation data collector

This example genders file configures data collection for a single node named twain.
This is annotated with comments (# explaining the next line in each case).

::: /etc/sysconfig/ldms.d/ClusterGenders/genders.local :::


    # mark twain as a host ldmsd should run on.
    # If the attribute ldmsd is not present, the systemd startup script will exit without starting ldmsd
    twain ldmsd

    # define the default sampling schedule (1 second interval with 0 microsecond offset)
    # these can be overridden on a per sampler basis
    twain ldmsd_interval_default=1000000,ldmsd_offset_default=0
    
    # define the hostname that should be used by aggregation daemons collecting from twain.
    # if twain has more than one network card, particularly a faster card, the name of that
    # interface should be assigned to ldmsd_host, e.g. ldmsd_host=twain-ib0
    twain ldmsd_host=twain
    # producer is the name of this host as it should appear in data sets.
    twain ldmsd_producer=twain

    # set a component id (8 byte unsigned integer). should be unique across an entire site,
    # define the port and transport type you want the collector to provide to aggregators.
    twain ldmsd_port=411,ldmsd_xprt=sock

    # list the sampler plugins you want to use, separated by colons (more can be added later)
    twain ldmsd_metric_plugins=meminfo:vmstat

    # override the sampler interval for meminfo (slower) 10 seconds and schema name
    twain ldmsd_meminfo=interval/10000000:schema/meminfo_ws

    # enable debug logging
    twain ldmsd_dbg=DEBUG

    # override where the log goes. note the leading // is required in the filename
    # by default, the logs will go to syslog /var/log/messages on most systems
    twain ldmsd_log=//var/log/ldmstest.log

## Setting the security key

LDMSD running as root should not be accessible to unprivileged users. To ensure this,
a secret key file must be defined in the ldmsd.local.conf file. Typically, this file
is located in /etc/sysconfig/ldms.d/ClusterSecrets/ldmsauth.conf. This location can be
redefined in the ldmsd.local.conf with variable LDMS_AUTH_FILE. See ldms_authentication(7) and
ldms_auth_ovis(7) man pages.

## Starting the collector

    systemctl start ldmsd
    sleep 2
    systemctl status -l ldmsd

## Checking the result 

Substitute the path value of conf= here if you used another location in your .conf file.

     ldms_ls -h localhost -p 411 -x sock -a ovis -A conf=/etc/sysconfig/ldms.d/ClusterSecrets/ldmsauth.conf

A bare ldms_ls with no options may work if you have changed none of the defaults in your options.
If you see no output or an error from ldms_ls, check the log file defined with ldmsd_log.

## Defining an aggregator and storage

We can create an aggregator instance simply by setting up the needed configuration files and starting the systemd service:

    systemctl start ldmsd@agg.service
    
For this, the new genders file needed is genders.agg

::: /etc/sysconfig/ldms.d/ClusterGenders/genders.agg :::

    # ldmsaggd=<list> defines the set of nodes this aggregator should collect from
    twain ldmsaggd=localhost
    # The port for the aggregator should not be the same as for the data collector
    twain ldmsd_port=412
    # This is the list of store plugins. if more than one is wanted, separate the
    # names with colon :.
    twain ldmsd_store_plugins=store_csv:store_flatfile
    # for each store, list the schemas you want in that format.
    # Flatfile stores one metric per file (plus source and timestamp, in a csv format)
    twain ldmsd_schemas_store_csv=meminfo_ws
    # the same data can be routed to multiple stores.
    twain ldmsd_schemas_store_flatfile=vmstat:meminfo_ws
    # set options for each store
    # here the files roll over at midnight and have a separate header.
    twain ldmsd_store_csv=path//var/log/twain-ldms/csv:altheader/1:rolltype/2:rollover/0    
    twain ldmsd_store_flatfile=path//var/log/twain-ldms/flat:altheader/01:rolltype/2:rollover/0    
    # enable debug logging
    twain ldmsd_dbg=DEBUG
    # override where the log goes. note the leading // is required in the filename
    # by default, the logs will go to the journal then /var/log/messages on most systems
    twain ldmsd_log=//var/log/ldmstest/agg.log

## Advanced debugging of ldmsd 

When started with libgenders supported systemd, a number of files that help administrators or users determine the presently running or most recently failed ldmsd details are created in /var/run/ldmsd. See the FILES section of the ldmsd-genders(8) manual page.
Most notable is the generated configuration script all-config.local (or all-config.agg).

On large production systems, be sure to configure as ldmsd_dbg=CRITICAL or ERROR to avoid flooding log systems.

## Scaling ldmsd

On a multicluster site, consistent application of locally chosen conventions simplifies and speeds ldmsd administration. Use of libgenders eliminates the need for administrators to learn the detailed and highly flexible ldmsd control language and also eliminates the need for interactive configuration tools. Use of carefully chosen convention will also ease downstream data management and analysis.

The same ldmsd systemd scripts handle difficult cases requiring complex hand-crafted or machine generated configurations. The escape hatches enabling generated configuration or bypassing libgenders use entirely are covered in the manual pages.

HPC systems typically have equipment requiring special configuration to collect the right data. The next section provides a complete example of production system data collection and robust routing to multiple storage locations. Modest annotations are included that may be helpful when porting the example to another production system.

## Serrano example

    # UUR text here

## Special considerations

While some sampler plugins collect a standard data set, others must be configured to select the right data. Additionally, some must be configured to avoid conflicts in data types.

## Timing

Data samples are collected synchronously across a cluster by specifying an interval between the samples (in microseconds) and an offset. Store plugins should be configured with the same interval or one which is an even multiple of the sampling interval if logging less data is desired. The target time will be (time since the epoch / interval) + offset. The offsets allowed are in the half-interval range (-(interval/2 - 1) : interval/2 i- 1). By convention, plugins producing job ids are run with a negative offset (such as -100000) and most other samplers receive an offset of 0. To ensure that all metrics have been collected before aggregation, a positive offset (200000 is applied).

## Sysclassib

The sysclassib sampler collects InfiniBand (IB) data from local network ports. A port or ports are specified as configuration argument "ports/card1.port1&card2.port2". Port identifiers can be found by running ibstat. When reviewing the ibstat output, check that the interface is active and is an IB interface rather than high speed Ethernet or Omnipath interface. If, as is usually the case, node classes within the cluster have different numbers of active IB ports, then a different schema name is needed on each node type. For example, schema/sysclassib_gw on Lustre gateway nodes and schema/sysclassib_ln on login nodes. On compute nodes, schema/sysclassib_cn:with_jobid=1. Bandwidth rates will be computed and stored if option metrics_type/1 is specified. Rates are left out if metrics_type/0 is specified.

## Opa2

The opa2 sampler collects Omnipath data from local network ports. The ibstat command can be used to gather the port names. As with sysclassib, read carefully to distinguish the HFI ports from IB and Ethernet ports.

## Procnetdev

Similar to the sysclassib sampler, the Ethernet interfaces monitored are specified with a list parameter ifaces/ethport1&ethport2. For example, ifaces/lo&eth0. Different node classes may need to be separated by specifying schema name such as schema/procnetdev_login or schema/procnetdev_cn.

## Meminfo 

The contents of meminfo /proc/meminfo depend on the compiled kernel and/or the memory features used by applications. The metrics are an initial group and optionally cma, dma, or huge page related values. The meminfo plugin collects and reports the metrics it first sees. Different nodes, not just different node classes may need schema/meminfo_{something} to prevent misidentification or omission of data.

## Splunk followers

Both store_csv and store_flatfile output can be read by a splunk input tool. In both cases, a shell script may also be used to filter the data into a format that makes the data smaller or more useful as needed.

    [fixme: serrano example from mark]

## Flat file roll over

Presently the flat file store does not support rollover directly by ldmsd. They can be rolled using logrotate. Prerotate should use "systemctl stop ldmsd@agg.service" and postrotate should restart it. At lower sampling frequencies, data loss may be avoid by carefully scheduling logrotate with cron.

## Milly example

Milly is a second-level (L2) ldmsd aggregation and storage host for serrano. It has a different set of administrators than serrano, and they have only read access to the genders.serrano file. The ldmsd instance ldmsd@serrano.service is used to manage the archiving of serrano data.

The configuration of the storage for serrano on milly is kept in a separate file milly.genders.serrano, and both files are listed in the ldmsd.serrano.conf on milly. The systemd launch script assembles these into a single file. 

    LDMS_GENDERS="/projects/ovis/ClusterGenders/genders.serrano /etc/sysconfig/ldms.d/ClusterGenders/milly.genders.serrano"

The content of genders.serrano may vary, and the milly team receives notice when this occurs so they can restart the L2 daemon. 

::: /etc/sysconfig/ldms.d/ClusterGenders/milly.genders.serrano :::

    fixme insert file here

## Csv archive

CSV stores are usually rolled over periodically (or by size) and migrated in some way to archive systems for analysis work later. The manual page details options for renaming closed files at rollover time. There are also the create_ options allowing files to be accessed by analysts and administrators without elevated privileges. For example files to be readable by group with number 1000666 while still being written will need an adjustment: ldmsd_store_csv=create_gid/100666:create_perm/0740.

