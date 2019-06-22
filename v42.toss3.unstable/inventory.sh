# this dumps the file lists and dependency lists
# for the generated rpms
x=$(basename $(pwd))
for i in ./sos/Tars/sosdb-4.*/$x/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qp --requires $i; echo; done > sosdeps
for i in ./sos/Tars/sosdb-4.*/$x/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qpl $i; echo; done > sosfiles
for i in ./ovis/Tars/ovis-4.*/$x/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qp --requires $i; echo; done > ovisdeps
for i in ./ovis/Tars/ovis-4.*/$x/RPMS/x86_64/*rpm; do echo $i; echo $i; rpm -qpl $i; echo; done > ovisfiles
