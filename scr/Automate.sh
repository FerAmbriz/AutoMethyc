#!/bin/bash

while [[ $# -gt 0 ]]; do
opt="$1"
shift;
current_arg="$1"
case "$opt" in
"-h"|"--help"      ) echo '''
AutoMet version 0.0.1-beta
	bash Automate.sh [options]
Options
	-i --input		Folder with fastq
	-o --output		Output location
	-r --ref		Folder with references
	-f --filtro		File with regions of interest
''';  exit 1;;
"-i"|"--input"      ) input="$1"; shift;;
"-o"|"--output"      ) output="$1"; shift;;
"-r"|"--ref"      ) ref="$1"; shift;;
"-f"|"--filtro"      ) filtro="$1"; shift;;
	esac
done
bash BuclePipeline.sh $input $output $ref

# descomprime y renombra los archivos por ID
bash rename.sh $output/results/06_bedGraph

# Construcción del merge
bash allmerge.sh $output/results/06_bedGraph $output

# Aplicacion de filtros
python FilterMigue.py $output/merge.csv $filtro $output

# Construcción del input de ComplexHeatmap
python Autoncoprint.py $output 
