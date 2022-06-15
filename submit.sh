#! /bin/bash

for i in pbe pbesol vdw-df vdw-df-cx vdw-df-obk8 vdw-df2 "sla+pw+b86r+vdw2" rvv10 vdw-df3-opt1 vdw-df3-opt2; do
	echo $i
	python3.7 gen_in.py $i
	cd $i/;
	for j in */;do
		echo $j
        	cd $j/
        	pwd
		sbatch submit
		cd ../
		done
        cd ../
done
