This is an rpm recipe for use with TOSS Linux version 3 or RHEL 7.

It provides a module to add cython 0.28.5
support via /opt/cython to the stock python 2.7 in /usr.

To install, create the typical rpmbuild environment and (after installing the dependencies):
```
  wget https://github.com/cython/cython/archive/0.28.5/cython-0.28.5.tar.gz && \
  mkdir -p ~/rpmbuild/SPECS ~/rpmbuild/SOURCES && \
  cp toss-python2-Cython.spec ~/rpmbuild/SPECS && \
  cp cython-0.28.5.tar.gz ~/rpmbuild/SOURCES && \
  cp module.toss-cython ~/rpmbuild/SOURCES && \
  (cd ~/rpmbuild/SPECS && rpmbuild -ba toss-python2-Cython.spec)
```
When successful, you can yum install the resulting rpm.
In the TOSS 3 modules environment, 
```
 module load cython/0.28.5/py2.7
```
In a redhat 7 environment,
  cp enable /opt/cython/0.28.5/enable

RPM Dependencies:
```
	gcc
	rpm-build
	python-devel
	python-setuptools
	python2-cython
```
