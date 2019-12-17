# Set topdir to be builddir/rpm
# note this is intentionally ignored by rpmbuild. must use
# commandline syntax in makefile.am to get this effect.
#% define _topdir %(echo $PWD)/toss
# do not set unfascist build
#%-define _unpackaged_files_terminate_build 0
#%-define _missing_doc_files_terminate_build 0

%global srcname sosdb

%global _scl_prefix /opt/ovis
%{!?scl:%global pkg_name %{name}}
%global scl_name_prefix sandia-
%global scl_name_base ovis_
%global scl_name_version 4.3.3
%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}

%{!?scl:%global pkg_name %{name}}
%global nfsmountable 1
%{?scl:%scl_package %{srcname} }

%define ldms_all System Environment/Libraries
%define build_timestamp %(date +"%Y%m%d_%H%M")
# % global __strip /bin/true
%global _enable_debug_package 0
%global _enable_debug_packages 0
%global debug_package %{nil}
%global __debug_install_post /bin/true
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /opt/python-2.7/bin/python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

# Main package
Summary: OVIS SOS Commands and Libraries
Name: %{?scl_prefix}sosdb
Version: 4.3.1
Release: 1.0%{?dist}
License: GPLv2 or BSD
Group: %{ldms_all}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: %{pkg_name}-%{version}.tar.gz
Requires: rpm >= 4.8.0
BuildRequires: scl-utils-build
BuildRequires: gcc glib2-devel
Requires: python2
Requires: python2-devel
Requires: sandia-ovis_python2_4.3-numpy
Requires: sandia-ovis_python2_4.3-cython
BuildRequires: python2-devel
BuildRequires: sandia-ovis_python2_4.3-numpy
BuildRequires: sandia-ovis_python2_4.3-cython
BuildRequires: doxygen
%{?scl:Requires: %scl_runtime}
Url: https://github.com/ovis-hpc/sos

%description
This package provides the OVIS sosdb commands and libraries for rhel7.


%prep
%setup -q -n %{pkg_name}-%{version}

%dump

%build
echo bTMPPATH %{_tmppath}
rm -rf $RPM_BUILD_ROOT
echo bBUILDROOT $RPM_BUILD_ROOT
echo using $(which cython)
export CFLAGS=" %{optflags} -O1 -g"
%configure --prefix=%{?scl_prefix:%_scl_root}/usr \
--disable-static \
--enable-python \
--enable-doc \
--enable-doc-html \
--enable-doc-man \
--enable-doc-graph

make V=1 %{?_smp_mflags}

%install
echo TMPPATH %{_tmppath}
echo BUILDROOT $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} V=1 install
ls %{buildroot}
mkdir -p %{buildroot}%{_prefix}

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/sos/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
#end core

# devel
%package devel
Summary: OVIS SOS DB devel package
Group: %{ldms_grp}
Requires: %{?scl_prefix}sosdb
%description devel
This is a development package of Scalable Object Store
Users who want to use sosdb from C must install this package.

%files devel
%defattr(-,root,root)
%{_includedir}/*/*.h
#end devel

%package doc
Summary: Documentation files for %{name}
Group: %{ldms_all}
%description doc
Doxygen files for ovis sosdb package.
%files doc
%defattr(-,root,root)
%{_mandir}/*/*
%{_datadir}/doc/%{pkg_name}
%docdir %{_datadir}/doc

%package python2
Summary: Python files for SOS DB
%description python2
Python files for ovis sosdb
# install needs
Requires: sosdb = %{version}
# build needs
BuildRequires: python python-devel sandia-ovis_python2_4.3-cython sandia-ovis_python2_4.3-numpy
%files python2
%defattr(-,root,root)
%{_prefix}/lib/python2.7/site-packages/sosdb
#end sosdb

%changelog
* Mon Dec 9 2019 Ben Allan <baallan@sandia.gov> 4.3.1-2
software collection initial packaging.
* Fri Jun 21 2019 Ben Allan <baallan@sandia.gov> 4.2.1-1
First packaging of stand-alone sos for TOSS 3. Not relocatable.

