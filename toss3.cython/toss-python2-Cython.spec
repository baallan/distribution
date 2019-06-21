%global srcname cython
%global upname Cython

%define pkgname python2-%{srcname}

Name:           %{pkgname}
Version:        0.28.5
Release:        1%{?dist}
Summary:        Language for writing Python extension modules

License:        ASL 2.0
URL:            http://www.cython.org
Source0:        https://github.com/cython/cython/archive/%{version}/%{srcname}-%{version}.tar.gz
Source1:	module.toss-cython

BuildRequires:  gcc

# override /usr in installation, but Prefix isn't working for this.
%define cy_root /opt/cython/%{version}
%define cy_bin %{cy_root}/bin
%define cy_sitepackages %{cy_root}/%{_lib}/python%{python2_version}/site-packages
%define cy_sitelib %{cy_root}/%{_lib}/python%{python2_version}/site-packages
%define moddir  /opt/modules/modulefiles/cython/%{version}


%global _description \
This is a development version of Pyrex, a language\
for writing Python extension modules.

%description %{_description}

# % package
Summary:        %{summary}
Obsoletes:      python2-Cython < 0.28.5
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Prefix: /

%description -n %{pkgname} %{_description}
Python 2 cython 0.28 for TOSS 3.

%prep
mkdir -p %{buildroot}%{cy_root}
%autosetup -n %{srcname}-%{version} -p1

%build
%py2_build

%install
mkdir -p %{buildroot}/%{moddir}
%{__install} -m 755 %{_sourcedir}/module.toss-cython %{buildroot}/%{moddir}

# % py2_install ; redefining the macro didn't work, so inline it here
CFLAGS="%{optflags}" %{__python} %{py_setup} %{?py_setup_args} install --prefix=%{cy_root} -O1 --skip-build --root %{buildroot}

# support forward compatibility with rhel 8
for bin in cython cythonize cygdb; do
  (cd %{buildroot}%{cy_bin}; ln -s ${bin} ${bin}-%{python2_version})
  (cd %{buildroot}%{cy_bin}; ln -s ${bin}-%{python2_version} ${bin}-2)
done
rm -rf %{buildroot}%{cy_root}%{cy_sitelib}/setuptools/tests

%files -n %{pkgname}
%license LICENSE.txt
%doc *.txt Demos Doc Tools
%{moddir}/*
%{cy_bin}/cython
%{cy_bin}/cython-2
%{cy_bin}/cython-%{python2_version}
%{cy_bin}/cygdb
%{cy_bin}/cygdb-2
%{cy_bin}/cygdb-%{python2_version}
%{cy_bin}/cythonize
%{cy_bin}/cythonize-2
%{cy_bin}/cythonize-%{python2_version}
%{cy_sitepackages}/%{upname}-*.egg-info/
%{cy_sitepackages}/%{upname}/
%{cy_sitepackages}/pyximport/
%{cy_sitepackages}/%{srcname}.py*

%changelog
* Thu Jun 20 2019 Ben Allan <baallan@sandia.gov>
Cython 0.28.5 for TOSS3 system python
