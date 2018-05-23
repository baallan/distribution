## Installation Guidelines for RPM users
See the section for your platform below.
The features included depend on the platform capabilities. Older platforms do not support some features, so these features are not packaged.
Custom builds from source to enable these features are possible but are not detailed here.

## TOSS 3

Supported features: LDMS, libgenders, Omnipath, Infiniband, and Cray RDMA, Lustre, jobid collection, Python library wrappers.

Unsupported features: SOS, Baler. 

Relocations available (specify identical relocations to all packages when installing):
/var, /etc, /usr. --relocate is supported and --prefix is not.

Recommended rpms for compute nodes:
* ovis
* ovis-initscripts-base
* ovis-initscripts-systemd
* ovis-python2 (optional)

Recommended additional rpms for login nodes:
* ovis-devel
* ovis-test
* ovis-doc

Recommended additional rpms for storage hosts:
* none

Recommended for analytical environments:
* ovis-python2


## TOSS 2

Supported features: LDMS, libgenders, Infinband, RDMA, Lustre, jobid collection.

Unsupported features: Baler, SOS, Python library wrappers. (Python 2.7 lacking)

Relocations available (specify identical relocations to all packages when installing):
/var, /etc, /usr. --relocate is supported and --prefix is not.

Recommended rpms for compute nodes:
* ovis
* ovis-initscripts-base
* ovis-initscripts-sysv
* ovis-python2

Recommended additional rpms for login nodes:
* ovis-devel
* ovis-test
* ovis-doc

Recommended additional rpms for storage hosts:
* none

## CLE6

Stable RPMS have not been released yet.

## RHEL7

Supported features: LDMS, Baler, SOS database, LDMS SOS storage plugin, Python library wrappers.

Unsupported features: genders, Infinband, RDMA, Lustre, jobid collection.

Relocations available (but not recommended) when not using yum are:
/var, /etc, /usr. --relocate is supported and --prefix is not.

Recommended rpms for workstations:
* ovis
* ovis-initscripts-base
* ovis-initscripts-systemd
* ovis-python2
* ovis-devel
* ovis-test
* ovis-doc
* ovis-sosdb

## RHEL6

Stable RPMS have not been released yet.
