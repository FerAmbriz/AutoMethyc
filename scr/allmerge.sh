#!/bin/bash

input_cov=$1
output=$2

array=($(ls $input_cov/*.cov))
tLen=${#array[@]}

ID=${array[0]%.*}
ID=${ID##*/}

python merge1.py ${array[0]} $ID $output 

echo 'done merge' ${array[0]}

for (( i=1; i<${tLen}; i=i+1));
do

ID=${array[i]%.*}
ID=${ID##*/}

python merge2.py ${array[$i]} $ID $output

echo 'done merge' ${array[$i]} 
done

python Construct.py $output

echo '#---------------- Done merge -------------------#'

