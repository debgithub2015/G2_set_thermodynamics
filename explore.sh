#! /bin/bash
rm -rf out.dat
for j in */;do
echo  $j >> out.dat
cd $j/
grep -i 'Final energy' *.out | wc -l >> ../out.dat
cd ../
done 
