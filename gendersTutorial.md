## Controlling LDMSD with libgenders

[This is a work in progress page]

Genders support is useful whether configuring LDMSD for a workstation or an entire cluster.
This is a simple getting-started tutorial for LDMS 3.4.6 and later.

## Compiling genders support in ldmsd 

If not building one of the supported HPC rpm configurations, you can enable genders support by including

    --enable-libgenders --enable-genderssystemd

in your configure options. If boost or libgenders are not installed in the normal locations, you
will also need to specify --with-boost=<location> and/or --with-libgenders=<location>.
The needed package files for genders are available in EPEL and other repositories or you can
install from source with https://github.com/chaos/genders.

## Using genders files with ldmsd

By default, the libgenders-based LDMS systemd script ldmsd.service uses /etc/sysconfig/ldms.d/ClusterGenders/genders.local.
Systemd can manage additional instances where each has a distinct name %I.
The ldmsd@%I.service by default uses /etc/sysconfig/ldms.d/ClusterGenders/genders.%I.
(Here %I is an arbitrary daemon instance name).
The file /etc/sysconfig/ldms.d/ldmsd.local.conf can override the name of the genders file to use.
Similarly, the file /etc/sysconfig/ldms.d/ldmsd.%I.conf can override the name of the genders file used by instance %I.
The LDMS_GENDERS setting in the .conf files overrides the default.

The genders file format is a simple text database associating attributes (with or without explicit values) to hostnames. See ldmsd-genders(8) and ldms-attributes(5) manual pages for details.

## Configuring data collection by example: the local workstation daemon data collector on a host named twain

This is annotated with comments (# explaining the next line in each case).


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

## Checking the result 

Substitute the path value of conf= here if you used another location in your .conf file.

     ldms_ls -h localhost -p 411 -x sock -a ovis -A conf=/etc/sysconfig/ldms.d/ClusterSecrets/ldmsauth.conf

A bare ldms_ls with no options may work if you have changed none of the defaults in your options.
If you see no output or an error from ldms_ls, check the log file defined with ldmsd_log.


TODO:
1 define genders.agg and start ldmsd@agg.service
3 define cluster version
5 demonstrate where var files go
6 test 


