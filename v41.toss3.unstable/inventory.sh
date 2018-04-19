# this dumps the file lists and dependency lists
# for the generated rpms
ver=4.1.0
for i in ./ovis/Tars/ovis-$ver/v41.toss3.unstable/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qp --requires $i; echo; done > plist
for i in ./ovis/Tars/ovis-$ver/v41.toss3.unstable/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qpl $i; echo; done > rlist
