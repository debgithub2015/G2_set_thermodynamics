#!/bin/bash

dir=/deac/thonhauserGrp/chakrad/calculations/database-calc/G2-2_set


for folder in $dir/*/;do
echo $folder
Zval=`echo "${folder##*/}"| cut -d '_' -f3`
echo $Zval
rm -rf $folder/*.txt
cd $folder/
echo 'system' $Zval > $folder/results_energy.txt
#for i in 'LiH' 'BeH' 'CH' 'CH2_s3B1d' 'CH2_s1A1d' 'CH3' 'CH4' 'NH' 'NH2' 'NH3' 'OH' 'H2O' 'HF' 'SiH2_s1A1d' 'SiH2_s3B1d' 'SiH3' 'SiH4' 'PH2' 'PH3' 'SH2' 'HCl' 'Li2' 'LiF' 'C2H2' 'C2H4' 'C2H6' 'CN' 'HCN' 'CO' 'HCO' 'H2CO' 'CH3OH' 'N2' 'N2H4' 'NO' 'O2' 'H2O2' 'F2' 'CO2' 'Na2' 'Si2' 'P2' 'S2' 'Cl2' 'NaCl' 'SiO' 'CS' 'SO' 'ClO' 'ClF' 'Si2H6' 'CH3Cl' 'CH3SH'  'HOCl' 'SO2' 'H' 'Li' 'Be' 'C' 'N' 'O' 'F' 'Na' 'P' 'Si' 'S' 'Cl' ;do
for i in *; do
if [[ -d  "$i" ]]; then
cd $i/
converge=`cat *.out | grep -i 'END of BFGS' | tail -1 | awk '{print }'`
echo $i
#final_enthalpy=`cat *.out|grep -i 'Final enthalpy' |tail -1| awk '{printf "%4.10f", $4*13.605698065894}'`
#final_energy=`cat *.out|grep -i '!' |tail -1| awk '{printf "%4.10f", $5*13.605698065894}'`
final_energy=`cat *.out|grep -i 'Final energy' |tail -1| awk '{printf "%4.10f", $4*13.605698065894}'`
mag=`cat *.out| grep -i 'total magnetization' | tail -1| awk '{print $4}'`
#volume=`cat *.out| grep -i 'new unit-cell volume' |tail -1| awk '{printf "%4.10f",  $8}'`
#alat_old=`cat *.out | grep -i 'CELL_PARAMETERS' | tail -1 | awk '{print $3}'` 
#len=${#alat_old}; 
#alat=`echo ${alat_old:0:len-1}`
#alat=`cat *.out | grep -A1 'CELL_PARAMETERS' | tail -1 | awk '{printf "%4.10f", $1}'` 
#c_cell_param=`cat *.out | grep -A3 'CELL_PARAMETERS' | tail -1 | awk '{printf "%4.10f", $3}'` 
#c_lat=`cat *.out | grep -A3 'CELL_PARAMETERS' | tail -1 | awk '{printf "%4.10f", $3}'` 
#c_lat=`echo $alat $c_cell_param | awk '{printf "%4.10f",$1*$2*0.52917721}'` 
#alat=`echo $alat | awk '{printf "%4.10f",$1*0.52917721}'`
#echo $i $converge >>  $folder/results_energy.txt
#echo $final_enthalpy $alat $c_lat $volume >> $folder/results_energy.txt
echo $i $final_energy $mag >> $folder/results_energy.txt
cd ../
fi
done
cd ../
done
