Name:           numpy
Version:        1.14.6
Release:        1.2%{?dist}
Epoch:          1
Summary:        A fast multidimensional array facility for Python

# override /usr in installation, but Prefix isn't working for this with python macros
# we need the path to include cython from the required package, or numpy may use the system cython
# incorrectly.
%define cy_root /opt/cython/%{version}
%define cy_bin %{cy_root}/bin
%define cy_sitepackages %{cy_root}/%{_lib}/python%{python2_version}/site-packages

%define moddir /opt/modules/modulefiles/numpy/%{version}/
%define numpy_root /opt/numpy/%{version}
%define numpy_sitepackages %{numpy_root}/%{_lib}/python%{python2_version}/site-packages
%define moddir  /opt/modules/modulefiles/numpy/%{version}/
%define numpy_do_test 0

# Everything is BSD except for class SafeEval in numpy/lib/utils.py which is Python
License:        BSD and Python
URL:            http://www.numpy.org/
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        module.toss-numpy

BuildRequires:  python-devel python-setuptools python2-cython gcc
BuildRequires:  lapack-devel
BuildRequires:  atlas-devel

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation.

%package -n python2-numpy
Summary:        A fast multidimensional array facility for Python

%description -n python2-numpy
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. 

%prep
%setup -q -n %{name}-%{version}%{?relc}

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
mkdir -p %{buildroot}/%{moddir}
%{__install} -m 755 %{_sourcedir}/module.toss-numpy %{buildroot}/%{moddir}/py%{python2_version}

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

%files -n python2-numpy
%license LICENSE.txt
%doc THANKS.txt site.cfg.example
%dir %{numpy_sitepackages}/%{name}
%{moddir}/*
%{numpy_sitepackages}/%{name}/*.py*
%{numpy_sitepackages}/%{name}/core
%{numpy_sitepackages}/%{name}/distutils
%{numpy_sitepackages}/%{name}/doc
%{numpy_sitepackages}/%{name}/fft
%{numpy_sitepackages}/%{name}/lib
%{numpy_sitepackages}/%{name}/linalg
%{numpy_sitepackages}/%{name}/ma
%{numpy_sitepackages}/%{name}/random
%{numpy_sitepackages}/%{name}/testing
%{numpy_sitepackages}/%{name}/tests
%{numpy_sitepackages}/%{name}/compat
%{numpy_sitepackages}/%{name}/matrixlib
%{numpy_sitepackages}/%{name}/polynomial
%{numpy_sitepackages}/%{name}-*.egg-info
%exclude %{numpy_sitepackages}/%{name}/LICENSE.txt

%changelog
* Fri Jun 21 2019 Ben Allan <baallan@sandia.gov> - 1.14.6-1
- package modern numpy for toss3 system python as module
