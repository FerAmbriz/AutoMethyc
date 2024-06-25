#!/bin/bash

path='/home/ferambriz/Projects/AutoMethycTest/metrics_test'
ref='/home/ferambriz/ref/Human-Hg19/ucsc.hg19.fasta'
output='/home/ferambriz/Projects/AutoMethycTest/metrics_test/output_metrics'

mkdir ${output} 

for i in {3..5};do
  figlet ===${i}===
  for j in {1..10};do
    mkdir ${path}/output_${i}_rep_${j}

    veces=3500
    sar -r 1 ${veces} > ${output}/estadisticas_memoria_${i}_rep_${j}.txt &

    automethyc -i ${path}/samples_${i} -n ${path}/normals_${i} -r ${ref} -b ${path}/BedGraph331.csv -o ${path}/output_${i}_rep_${j}

    wait
  done
done
