This is an rpm recipe for use with TOSS linux version 3.

It provides a module to add numpy 1.14 (less f2py)
support via /opt/numpy to the stock python 2.7 in /usr.

It requires Cython 0.28.5 for TOSS also be installed.

To install, create the typical rpmbuild environment and (after installing the toss3 cython in /opt):

 wget https://github.com/numpy/numpy/releases/download/v1.14.6/numpy-1.14.6.tar.gz
 cp toss-python2-numpy.spec ~/rpmbuild/SPECS
 cp numpy-1.14.6.tar.gz ~/rpmbuild/SOURCES
 cp module.toss-numpy ~/rpmbuild/SOURCES
 cd ~/rpmbuild/SPECS
 rpmbuild -ba toss-python2-numpy.spec

When successful, you can yum install the resulting rpm.

In the TOSS 3 modules environment, 
 module load cython
 module load numpy

