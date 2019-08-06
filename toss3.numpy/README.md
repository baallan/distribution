This is an rpm recipe for use with TOSS Linux version 3 or RHEL 7.

It provides a module to add numpy 1.14 (less f2py)
support via /opt/[cython,numpy] to the stock python 2.7 in /usr.

It requires Cython 0.28.5 for TOSS also be installed.

To install, create the typical rpmbuild environment and (after installing the python2-cython in /opt):
```
 wget https://github.com/numpy/numpy/releases/download/v1.14.6/numpy-1.14.6.tar.gz && \
 mkdir -p ~/rpmbuild/SPECS ~/rpmbuild/SOURCES  && \
 cp toss-python2-numpy.spec ~/rpmbuild/SPECS && \
 cp numpy-1.14.6.tar.gz ~/rpmbuild/SOURCES && \
 cp module.toss-numpy ~/rpmbuild/SOURCES && \
 (cd ~/rpmbuild/SPECS && rpmbuild -ba toss-python2-numpy.spec)
```
When successful, you can yum install the resulting rpm.
Note: The build of numpy can take a really long time due to the tests
if numpy\_do\_test is enabled in the spec file.

In the TOSS 3 modules environment, 
```
 module load cython/0.28.5/py2.7
 module load numpy/1.14.6/py2.7 
```

RPM Dependencies:
```
	python-devel python-setuptools python2-cython gcc
	lapack-devel
	atlas-devel
	gcc
	rpm-build
```
