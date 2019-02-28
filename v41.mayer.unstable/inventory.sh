# this dumps the file lists and dependency lists
# for the generated rpms
for i in ./ovis/Tars/ovis-4.*/v41.mayer.unstable/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qp --requires $i; echo; done > plist
for i in ./ovis/Tars/ovis-4.*/v41.mayer.unstable/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qpl $i; echo; done > rlist
