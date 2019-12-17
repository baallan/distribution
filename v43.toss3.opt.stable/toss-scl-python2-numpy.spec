%global srcname numpy
%global upname Numpy

%global _scl_prefix /opt/ovis
%{!?scl:%global pkg_name %{name}}
%global scl_name_prefix sandia-
%global scl_name_base ovis_python2_
%global scl_name_version 4.3
%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}
%global nfsmountable 1
%{?scl:%scl_package %{srcname}}

Name:           %{?scl_prefix}%{srcname}
Version:        1.14.6
Release:        1%{?dist}
Summary:        A fast multidimensional array facility for Python

# we need the path to include cython from the required package, or numpy may use the system cython
# incorrectly.
%define cy_root /opt/ovis/%{scl}/root/usr
%define cy_bin %{cy_root}/bin
%define cy_sitepackages %{cy_root}/%{_lib}/python%{python2_version}/site-packages


# Everything is BSD except for class SafeEval in numpy/lib/utils.py which is Python
License:        BSD and Python
URL:            http://www.numpy.org/
Source0:        https://github.com/numpy/numpy/releases/download/v1.14.6/numpy-1.14.6.tar.gz 

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{scl}-cython
BuildRequires:  python-devel python-setuptools gcc
BuildRequires:  lapack-devel
BuildRequires:  atlas-devel
BuildRequires: scl-utils-build
%{?scl:Requires: %scl_runtime}


%define numpy_root %{cy_root}
%define numpy_sitepackages %{numpy_root}/%{_lib}/python%{python2_version}/site-packages
%define numpy_do_test 0


%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation.

Summary:        A fast multidimensional array facility for Python

%prep
mkdir -p %{buildroot}%{numpy_root}
%setup -q -n %{srcname}-%{version}%{?relc}

# workaround for rhbz#849713
# http://mail.scipy.org/pipermail/numpy-discussion/2012-July/063530.html
rm numpy/distutils/command/__init__.py && touch numpy/distutils/command/__init__.py


%build
env ATLAS=%{_libdir} \
    PATH=%{cy_bin}:$PATH \
    PYTHONPATH=%{cy_sitepackages}:$PYTHONPATH \
    FFTW=%{_libdir} BLAS=%{_libdir} \
    BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python2} setup.py build

%install
env ATLAS=%{_libdir} \
    PATH=%{cy_bin}:$PATH \
    PYTHONPATH=%{cy_sitepackages}:$PYTHONPATH \
    FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python2} setup.py install --prefix=%{numpy_root} --root %{buildroot}

rm -rf %{buildroot}/%{numpy_sitepackages}/numpy/f2py
rm -rf %{buildroot}/%{numpy_root}/bin

%check
%if %{numpy_do_test}
  NTEST="numpy.test(verbose=2)"
%endif
pushd doc &> /dev/null
PATH="%{buildroot}%{_bindir}:${PATH}" PYTHONPATH="%{buildroot}%{numpy_sitepackages}:%{cy_sitepackages}" %{__python2} -c "import pkg_resources, numpy ; $NTEST" \
# don't remove this comment
popd &> /dev/null

%files
%license LICENSE.txt
%doc THANKS.txt site.cfg.example
%dir %{numpy_sitepackages}/%{srcname}
%{numpy_sitepackages}/%{srcname}/*.py*
%{numpy_sitepackages}/%{srcname}/core
%{numpy_sitepackages}/%{srcname}/distutils
%{numpy_sitepackages}/%{srcname}/doc
%{numpy_sitepackages}/%{srcname}/fft
%{numpy_sitepackages}/%{srcname}/lib
%{numpy_sitepackages}/%{srcname}/linalg
%{numpy_sitepackages}/%{srcname}/ma
%{numpy_sitepackages}/%{srcname}/random
%{numpy_sitepackages}/%{srcname}/testing
%{numpy_sitepackages}/%{srcname}/tests
%{numpy_sitepackages}/%{srcname}/compat
%{numpy_sitepackages}/%{srcname}/matrixlib
%{numpy_sitepackages}/%{srcname}/polynomial
%{numpy_sitepackages}/%{srcname}-*.egg-info
%exclude %{numpy_sitepackages}/%{srcname}/LICENSE.txt

%changelog
* Mon Dec 16 2019 Ben Allan <baallan@sandia.gov> - 1.14.6-1
- package modern numpy for toss3 software collection as module
