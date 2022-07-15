#!/bin/bash

input_cov=$1
output=$2
stat=$3

array=($(ls $input_cov/*.cov))
tLen=${#array[@]}

ID=${array[0]%.*}
ID=${ID##*/}

python /usr/bin/merge1.py ${array[0]} $ID $output $stat

echo 'done merge' ${array[0]}

for (( i=1; i<${tLen}; i=i+1));
do

ID=${array[i]%.*}
ID=${ID##*/}

python /usr/bin/merge2.py ${array[$i]} $ID $output $stat

echo 'done merge' ${array[$i]} 
done

python /usr/bin/Construct.py $output

echo '#---------------- Done merge -------------------#'

