# Controlling LDMSD with libgenders

Genders support is useful whether configuring LDMSD for a workstation or an entire cluster.
It provides scalability and in some cases allows reuse of node set definitions. A single declarative text file defines the ldmsd roles and details for an entire cluster.

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

**::: /etc/sysconfig/ldms.d/ClusterGenders/genders.local :::**


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

**::: /etc/sysconfig/ldms.d/ClusterGenders/genders.agg :::**

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
    # enable debug logging.
    twain ldmsd_dbg=DEBUG
    # override where the log goes. note the leading // is required in the filename.
    # by default, the logs will go to the journal then /var/log/messages on most systems.
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

The file /etc/genders contains numerous definitions controlling the services each node offers.
Only the ldms related lines are given here. The bootnode property is used by more than ldmsd.

**::: /etc/genders (the ldms parts) :::**

    ## bootnode specification ##
    ser[1-187],sergw[1-3],serln1    bootnode=seradmin1
    ser[188-374],sergw[4-6],serln2    bootnode=seradmin2
    ser[375-561],sergw[7-9],serln3    bootnode=seradmin3
    ser[562-748],sergw[10-12],serln4    bootnode=seradmin4
    ser[749-935],sergw[13-15],serln5    bootnode=seradmin5
    ser[936-1122],sergw[16-18],serln6    bootnode=seradmin6
    ## Run data collectors (ldmsd) on all nodes
    ser[1-1122],sergw[1-18],serrano-login[1-6],seradmin[1-6] ldmsd
    ## Run LDMS aggregators (ldmsaggd) on all admin nodes
    seradmin[1-6] ldmsaggd=BOOTNODELIST:%n:CLIENTOFLIST


The next file contains the ldmsd-related genders definitions. For administrative convenience they are not included in the default /etc/genders file on serrano. 

**::: /etc/sysconfig/ldms.d/ClusterGenders/genders.serrano :::**

    # LDMS related attributes for libgenders support
    # 'man ldms-genders' is the authoritative source for LDMS genders attrs info
    
    # Run data collectors (ldmsd) on all nodes
    # commenting out the next line will make ldmsd exit on start
    # except on aggregator (admin) nodes.
    # This is defined in /etc/genders so leave it commented out here.
    # The nodeup script needs the 'ldmsd' and 'ldmsaggd' attributes to be in /etc/genders 
    # but does not need to see any other ldmsd attributes.
    # Compute nodes are ser#, lustre gateways are sergw#, and the
    # other node names are self explanatory.
    #ser[1-1122],sergw[1-18],serrano-login[1-6],seradmin[1-6] ldmsd
    
    # 60 second sampling
    ser[1-1122],sergw[1-18],seradmin[1-6] ldmsd_interval_default=60000000,ldmsd_offset_default=0
    
    # Data collectors listen on rdma transport unless testing ethernet sockets.
    ser[1-1122],sergw[1-18],seradmin[1-6],serrano-login[1-6],serln[1-6] ldmsd_port=411
    ser[1-1122],sergw[1-18],serrano-login[1-6],serln[1-6] ldmsd_xprt=rdma
    #ser[1-1122],sergw[1-18],serrano-login[1-6],serln[1-6] ldmsd_xprt=sock
    # The admin nodes are ldmsd aggregators and listen on TCP sockets
    # to service remote level 2 aggregators.
    seradmin[1-6] ldmsd_xprt=sock
    
    # Define the hostname needed for the data collectors transport.
    ser[1-1122],sergw[1-18],seradmin[1-6] ldmsd_host=%n-ib0
    # Login nodes need specific lines because of the external hostname renaming we
    # do at startup.
    serrano-login[1-6],serln[1-6] ldmsd_host=%n-ib0
    # if we switch to tcp socket, the hostname
    #ser[1-1122],sergw[1-18],seradmin[1-6] ldmsd_host=%n
    #serrano-login[1-6],serln[1-6] ldmsd_host=%n
    
    # Define data collection plugins that ldmsd will use.
    # Some collectors are not used on some nodes.
    ser[1-1122],serrano-login[1-6] ldmsd_metric_plugins=jobid:meminfo:vmstat:procnfs:lustre2_client:procstat:procnetdev:opa2
    seradmin[1-6] ldmsd_metric_plugins=meminfo:vmstat:procstat:procnetdev:opa2
    sergw[1-18] ldmsd_metric_plugins=meminfo:vmstat:procstat:procnetdev:opa2:sysclassib
    
    # configuration of jobid plugin names file created by the slurm prolog.
    ser[1-1122]  ldmsd_jobid=file//var/run/ldms.jobinfo
    
    # meminfo plugin settings
    # this may need tailored schema names on other systems
    ser[1-1122],sergw[1-18],serrano-login[1-6],seradmin[1-6] ldmsd_meminfo=with_jobid/1
    
    # vmstat plugin settings
    ser[1-1122],sergw[1-18],serrano-login[1-6],seradmin[1-6] ldmsd_vmstat=with_jobid/1
    
    # procnfs plugin settings
    ser[1-1122],sergw[1-18],serrano-login[1-6],seradmin[1-6] ldmsd_procnfs=with_jobid/1
    
    # 
    # lustre2_client plugin settings
    # we have to list the filesystem mounts...
    ser[1-1122],serrano-login[1-6] ldmsd_lustre2_client=llite/fscratch&gscratch:with_jobid/1
    
    # procstatutil2 plugin settings
    # we have to list the maximum cpu count (or hyperthread count) seen on any node type.
    # Nodes without hyperthreading will end up with columns of zeroed data unless
    # an alternate schema name is specified.
    ser[1-1122],sergw[1-18],serrano-login[1-6],seradmin[1-6] ldmsd_procstat=maxcpu/32:with_jobid/1
    
    # procnetdev plugin settings
    # we have to list the expected ethernet device names.
    ser[1-1122]        ldmsd_procnetdev=with_jobid/1:ifaces/eth0&eth2&ib0&ib1
    serrano-login[1-6] ldmsd_procnetdev=with_jobid/1:ifaces/eth0&eth2&ib0&ib1
    seradmin[1-6]      ldmsd_procnetdev=with_jobid/1:ifaces/eth0&eth2&ib0&ib1
    sergw[1-18]        ldmsd_procnetdev=with_jobid/1:ifaces/eth0&eth2&ib0&ib1
    
    # opa2 and sysclassib plugin settings.
    # we have to list the expected fast device names.
    ser[1-1122],serrano-login[1-6],seradmin[1-6] ldmsd_opa2=with_jobid/1:ports/hfil_0.1
    sergw[1-18] ldmsd_sysclassib=with_jobid/1:ports/mlx5_0.1:schema/gw_sysclassib
    
    # LDMS component id groups. These ranges are not randomly chosen. They have to
    # be layed out in a manner such that all nodes on all clusters in a given
    # network domain, i.e. SRN, have unique non-overlapping ids. It is a bit
    # like IP subnet design. This benefits downstream data analytics and does not
    # directly affect data collection.
    ser[1-1122]    ldmsd_idbase=300000
    seradmin[1-6]   ldmsd_idbase=310000
    serrano-login[1-6] ldmsd_idbase=320000
    sergw[1-18]   ldmsd_idbase=330000
    # A better non-legacy practice is to
    # define component_ids as an integer (8 bytes) with subsections as follows:
    #  high bytes 1,2 network number 
    #  byte 3 cluster number,
    #  byte 4 component type,
    #  low bytes 5-8 site device number.
    # Where
    #   network numbers assigned by community registry (maybe recycle ipv4 class B)
    #   cluster number assigned by owner.
    #   type (0: compute, 1 admin, 2 login, 3 gateway, 4 top of cluster, 5-255 tbd)
    #   device number assigned by owner
    
    # Define the 'level 1' LDMS aggregators.
    # %n in ldmsagdd means aggregate yourself (avoidable if using an L2 aggregator).
    # L1 aggregators use sockets transport rather than rdma to provide data to L2 clients.
    #
    # The 'level 1' aggregators within the cluster will report their aggregated
    # data to the milly server (L2) using a pull model. milly is connected to the cluster
    # over the Capviz internal HPC storage VLAN.
    # The next line is uncommented in /etc/genders for nodeup use.
    # seradmin[1-6] ldmsaggd=BOOTNODELIST:%n:CLIENTOFLIST 
    
    # next line says we expect milly as an L2 aggregator. No effect within serrano.
    seradmin[1-6] ldmsaggd_clientof=milly
    # Data collection once per minute at 1.3 seconds after the minute mark.
    # This assumes node level collection takes no more than 1.2 seconds.
    # If a node is missing, retry connecting every 30 seconds.
    seradmin[1-6] ldmsaggd_interval_default=60000000,ldmsaggd_offset_default=130000,ldmsaggd_event_thds=8,ldmsaggd_conn_retry=30000000
    # 2G reserved for set transportation memory; vast overestimate of actual need.
    seradmin[1-6] ldmsaggd_mem_res=2G
    #seradmin[1-6] ldmsd_dbg=DEBUG
    seradmin[1-6] ldmsd_dbg=ERROR
    # use flatfile store for easy access to individual metrics 
    seradmin[1-6] ldmsd_store_plugins=store_flatfile
    # flatfile data grows on terabyte local flash.
    seradmin[1-6] ldmsd_store_flatfile=path//localdisk/ldms/
    # for the moment, only storing meminfo and procstat (cpu data) to flash
    seradmin[1-6] ldmsd_exclude_schemas_store_flatfile=slurmjobid:vmstat:procnfs:procnetdev:sysclassib:lustre2_client

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

Both store_csv and store_flatfile output can be read by a splunk input tool. In both cases, a shell script may also be used to filter the data into a format that makes the data smaller or more useful as needed. Serrano uses flatfile only for splunk.

    # everything after the tail -F is an approximation that will be fixed soon
    tail -F .../meminfo/Active | ...

## Flat file roll over

Presently the flat file store does not support rollover directly by ldmsd. They can be rolled using logrotate. Prerotate should use "systemctl stop ldmsd@agg.service" and postrotate should restart it. At lower sampling frequencies, data loss may be avoid by carefully scheduling logrotate with cron.

## Milly example

Milly is a second-level (L2) ldmsd aggregation and storage host for serrano. It has a different set of administrators than serrano, and they have only read access to the genders.serrano file and the serrano /etc/genders file. The ldmsd instance ldmsd@serrano.service is used to manage the archiving of serrano data.

The configuration of the LDMSD storage for serrano on milly is kept in a separate file milly.genders.serrano, and three files are listed in the ldmsd.serrano.conf on milly. The systemd launch script assembles these into a single file. 

    LDMS_GENDERS="/serrano/etc/genders /ovis/ClusterGenders/genders.serrano /ovis/ClusterGenders/milly.genders.serrano"

The content of genders and genders.serrano may vary with administrative activity, and the milly team receives notice when this occurs so they can restart the L2 daemon. 

The setup in milly.genders.serrano does not vary for other clusters in LDMS version 3 and later because ${VARIABLES} are substituted by either LDMS or the systemd script as required. The milly.genders.serrano is actually a symbolic link
to milly.genders.capviz file which works for any of the clusters due to common administrative choices. If only a single cluster is monitored from the L2 host, then variables need not be used.

**::: /etc/sysconfig/ldms.d/ClusterGenders/milly.genders.serrano :::**

    # These are the genders specific to milly gathering from
    # the top level aggregator(s) within ${LDMSCLUSTER}
    #
    # Milly is aggregatinging ${LDMSCLUSTER} 1st level aggregators
    # master list of port values is in /projects_srn/ovis/ClusterGenders/README.txt
    milly ldmsaggd=AGGCLIENTOFLIST
    # chadmin[1-12] ldmsaggd_clientof=milly ## taken care of in genders.${LDMSCLUSTER}
    milly ldmsd_port=${CAPVIZ_AGG_PORT}

    # memory size
    milly ldmsaggd_mem_res=200M
    # threads
    milly ldmsaggd_event_thds=8

    # milly aggregation schedule:
    # offset should be bigger than admin L1 agg offset. offsets must be coordinated
    # across all clusters to avoid NIC traffic jam if nic is slow.
    milly ldmsaggd_interval_default=${CAPVIZ_AGG_INTERVAL},ldmsaggd_offset_default=${CAPVIZ_AGG_OFFSET}

    # stores
    milly ldmsd_store_plugins=store_csv
    # csv controls
    # midnight rollover; any file older than 25 hours can be moved
    # without bothering ldmsd.
    milly ldmsd_store_csv=altheader/1:rolltype/2:rollover/0:path//mprojects/ovis/ClusterData/${LDMSCLUSTER}:create_gid/1001010666:create_perm/640
    # schemas to ignore
    # milly ldmsd_exclude_schemas_store_csv=
    # schemas to store
    #milly ldmsd_schemas_store_csv=jobid:meminfo:vmstat:procnfs:lustre2_client:procstat:procnetdev:sysclassib:gw_sysclassib
    milly ldmsd_schemas_store_csv=gw_procnetdev:gw_sysclassib:jobid:Lustre_Client:meminfo:opa2:procnetdev:procnfs:procstat:sysclassib:vmstat

    # logging controls
    #milly ldmsd_dbg=DEBUG
    milly ldmsd_dbg=WARNING
    milly ldmsd_log=/var/log/ldms-clusters

A common location to define values needed by all the aggregators on host milly is the ldmsd.all_instances.conf file.  This piece of bash script prevents conflicts in the timing and port number configuration if it is properly maintained. On L2 hosts serving at most one cluster, this file is unneeded.

**::: /etc/sysconfig/ldms.d/ldmsd.all_instances.conf :::**

    #
    # This contains logic common to all aggregators that tweaks by target.
    # Ports on milly need to be consistently defined.
    #

    # In order of who goes first_
    clusterlist="skybridge chama serrano solo uno ghost doom eclipse hazel cts1x"

    # The encapsulating script can define ALL_PICKY=1 to turn
    # unknown cluster name warnings into exit errors.

    # archiving cluster ldmsds start at 413
    case $LDMSCLUSTER in 
    milly)
    	export MILLY_PORT=411
    	;;
    agg)
    	export MILLY_AGG_PORT=412
    	;;
    solo)
    	export CAPVIZ_AGG_PORT=413
    	;;
    chama)
    	export CAPVIZ_AGG_PORT=414
    	;;
    skybridge)
    	export CAPVIZ_AGG_PORT=415
    	;;
    serrano)
    	export CAPVIZ_AGG_PORT=416
    	;;
    uno)
    	export CAPVIZ_AGG_PORT=417
    	;;
    ghost)
    	export CAPVIZ_AGG_PORT=418
    	;;
    cts1x)
    	export CAPVIZ_AGG_PORT=419
    	;;
    doom)
    	export CAPVIZ_AGG_PORT=420
    	;;
    eclipse)
    	export CAPVIZ_AGG_PORT=421
    	;;
    hazel)
    	export CAPVIZ_AGG_PORT=422
    	;;
    *)
    	if test -n "$ALL_PICKY"; then
    		echo "PORT: unset for $LDMSCLUSTER in ldmsd.all_instances.conf"
    		exit 1
    	fi
    esac


    # Timing on a shared network link needs to be consistent and noncontending.
    # The current schedule is 2 second gap between clusters
    base_interval=60000000
    # max offset is 29999999
    case $LDMSCLUSTER in
    solo)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=8200000
    	;;
    chama)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=4200000
    	;;
    skybridge)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=2200000
    	;;
    serrano)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=6200000
    	;;
    uno)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=10200000
    	;;
    ghost)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=12200000
    	;;
    cts1x)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=18200000
    	;;
    doom)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=14200000
    	;;
    eclipse)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=16200000
    	;;
    hazel)
    	export CAPVIZ_AGG_INTERVAL=$base_interval
    	export CAPVIZ_AGG_OFFSET=16200000
    	;;
    *)
    	if test -n "$ALL_PICKY"; then
    		echo "TIMING: unset for $LDMSCLUSTER in ldmsd.all_instances.conf"
    		exit 1
    	fi
    esac

## Csv archive

CSV stores are usually rolled over periodically (or by size) and migrated in some way to archive systems for analysis work later. The manual page details options for renaming closed files at rollover time. There are also the create_ options allowing files to be accessed by analysts and administrators without elevated privileges. For example files to be readable by group with number 1000666 while still being written will need an adjustment: ldmsd_store_csv=create_gid/100666:create_perm/0740.

