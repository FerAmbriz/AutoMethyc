#!/bin/bash

input=$1
output=$2
dep=$3

gzip -d $input/*.gz

echo 'filtered,unfiltered,depth_mean' > $output/CountUF_depth.csv
echo '---INPUT----'
echo $(ls $input)

for i in $input/*.cov;
do
	x=${i%.*}
	x=${x##*/}
	
	python /usr/bin/Depth.py $i $output $dep $x

done
