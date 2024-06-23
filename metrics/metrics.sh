#!/bin/bash

echo "Start test at: $(date +'%H:%M:%S')" >> estadisticas_memoria.txt
path='/home/lab13/Documents/FernandoAmbriz/example'

#1725
veces=2000
sar -r 1 $veces  > estadisticas_memoria.txt &

automethyc_docker -i $path/FastqSamples -n $path/FastqNormals -r /home/lab13/Referencia/ucsc.hg19.fasta -b $path/BedGraph_chr2.csv -o $path/output

echo done
