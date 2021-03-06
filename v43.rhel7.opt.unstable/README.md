# Collection build notes:

The rpms here are NOT relocatable in any way, since they follow the 
Software Collections guidelines instead.

Daemons install to /opt/ovis/sandia-ovis\_4.3.3
and runtime files appear in /var/opt/ovis/sandia-ovis\_4.3.3/run

To Build ovis 4.3.3:
The ovis cython/numpy must be installed already.

./firecollection
and then install the resulting:
```
sandia-ovis_4.3.3-runtime
```

./firesos
and then install the resulting:
```
sandia-ovis_4.3.3-sosdb
sandia-ovis_4.3.3-sosdb-devel
sandia-ovis_4.3.3-sosdb-python2
```

./fireldms


# Installation:

If you have an RPM repository set up containing all the rpms 
generated by firecollection, firesos, and fireldms, you should
then be able to install convenience package:
```
sandia-ovis_4.3.3
with
yum install sandia-ovis_4.3.3
```

Then set up systemd links after rpm install:
```
scl register /opt/ovis/sandia-ovis_4.3.3
systemctl link /opt/ovis/sandia-ovis_4.3.3/root/usr/lib/systemd/system/sandia-ovis_4.3.3-ldmsd.service
systemctl link /opt/ovis/sandia-ovis_4.3.3/root/usr/lib/systemd/system/sandia-ovis_4.3.3-ldmsd@.service
```
but note on redhat 7, systemd is buggy and linking the ldmsd@.service will fail.
The workaround is:
```
(cd /etc/systemd/system && \
ln -s /opt/ovis/sandia-ovis_4.3.3/root/usr/lib/systemd/system/sandia-ovis_4.3.3-ldmsd@.service . && \
systemctl daemon-reload)
```
Then to get the daemon running, you will need to (per your site tastes) fix the authentication 
to be a real authentication secret file or a symbolic link, perhaps with a link:
```
cd /opt/ovis/sandia-ovis_4.3.3/root/etc/sysconfig/ldms.d/ClusterSecrets
ln -s /etc/sysconfig/ldms.d/ClusterSecrets/ldmsauth.conf .
ln -s ./ldmsauth.conf agg.ldmsauth.conf
```
and note that ldmsauth.conf must contain a valid secretword line and have permissions 600.


# Using ldmsd manually:

You will need to enable the collection.
```
scl --list ; should show sandia-ovis_4.3.3
scl enable sandia-ovis_4.3.3 bash ; start a shell with the ovis paths set
