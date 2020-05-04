Summary: Package that installs Ovis LDMS
Name: ovis_ldms
Version: 4.3.4
Release: 1.1%{?dist}
License: GPLv2+
Requires: ovis-papi
Requires: ovis-ldms
Requires: ovis-ldms-initscripts-base
Requires: ovis-ldms-initscripts-systemd
Requires: ovis-llnl-lustre

%description
This bundles ldms with hpc-orientged samplers for TOSS3


%changelog
* Wed Apr 15 2020 Benjamin Allan <baallan@sandia.gov> 0.1
- revised package dependencies
