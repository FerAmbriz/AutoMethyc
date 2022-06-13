#!/bin/bash

input=$1
output=$2
ref=$3
filtro=$4

#bash Automate.sh ../example/fastq/ .. ../example/ref/ ../example/Filtro2.csv

bash BuclePipeline.sh $input $output $ref

# descomprime y renombra los archivos por ID
bash rename.sh $output/results/06_bedGraph

# Construcción del merge
bash allmerge.sh $output/results/06_bedGraph $output

# Aplicacion de filtros
python FilterMigue.py $output/merge.csv $filtro $output

# Construcción del input de ComplexHeatmap
python Autoncoprint.py $output 
