# this dumps the file lists and dependency lists
# for the generated rpms
x=$(basename $(pwd))
PARTS="LDMS OVIS"
for p in $PARTS; do
	for r in $(find $p -name '*.rpm') ; do
		echo $r;
		echo $r;
		rpm -qp --requires $r;
	       	echo;
	done > deps.$p
	for r in $(find $p -name '*.rpm') ; do
		echo $r;
		echo $r;
		rpm -qpl $r;
	       	echo;
	done > list.$p
done

