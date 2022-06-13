#!/bin/bash

gzip -d $1/*.gz

array=($(ls $1/*.cov))
tLen=${#array[@]}

for (( i=0; i<${tLen}; i=i+1));
do
x=${array[$i]%_S*}
x=${x##*/}


prefix='one_mismatch.'

ID=${x/#$prefix}

mv ${array[$i]} $1/$ID.cov

done
