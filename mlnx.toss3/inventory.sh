# this dumps the file lists and dependency lists
# for the generated rpms
x=$(basename $(pwd))
for i in ./ovis/Tars/ovis-3.*/$x/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qp --requires $i; echo; done > plist
for i in ./ovis/Tars/ovis-3.*/$x/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qpl $i; echo; done > rlist
