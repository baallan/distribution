## Installation Guidelines for RPM users
See the section for your platform below.
The features included depend on the platform capabilities. Older platforms do not support some features, so these features are not packaged.
Custom builds from source to enable these features are possible but are not detailed here.

## TOSS 3

Supported features: LDMS, Baler, SOS database, LDMS SOS storage plugin, genders, Infinband, RDMA, Lustre, Slurm jobid collection, Python library wrappers.

Unsupported features: SOS Python interfaces. (Cython lacking)

Relocations available (specify identical relocations to all packages when installing):
/var, /etc, /usr. --relocate is supported and --prefix is not.

Recommended rpms for compute nodes:
* ovis
* ovis-initscripts-base
* ovis-initscripts-systemd
* ovis-python2

Recommended additional rpms for login nodes:
* ovis-devel
* ovis-test
* ovis-doc

Recommended additional rpms for storage hosts:
* ovis-sosdb

## TOSS 2

Supported features: LDMS, SOS database, LDMS SOS storage plugin, genders, Infinband, RDMA, Lustre, Slurm jobid collection.

Unsupported features: Baler, SOS Python interfaces, Python library wrappers. (Python 2.7, Cython lacking)

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
* ovis-sosdb

## CLE6

Stable RPMS have not been released yet.

## RHEL7

Supported features: LDMS, Baler, SOS database, LDMS SOS storage plugin, Python library wrappers.

Unsupported features: genders, Infinband, RDMA, Lustre, Slurm jobid collection.

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
