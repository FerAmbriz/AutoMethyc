# AutoMet
This program ...

## Dependencies
* Bowtie2 http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#building-from-source
* Bismark https://www.bioinformatics.babraham.ac.uk/projects/bismark/
* Anaconda3 https://www.anaconda.com/
* fastqc https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* TrimGalore https://github.com/FelixKrueger/TrimGalore

## Docker container
* https://hub.docker.com/r/ambrizbiotech/automet

## Format of filter


## Usage
```

docker run -it -d -v $(pwd):/data ambrizbiotech/automet ls /data/Lab13/FernandoAmbriz/AutoMet/scr


cd
docker run -v $(pwd):/[home] -it ambrizbiotech/automet

git clone https://github.com/FerAmbriz/AutoMet.git
cd AutoMet/scr
bash Automate.sh -i ../example/fastq/ -o .. -r ../example/ref/ -f ../example/Filtro2.csv

docker run -it -d -v $(pwd):/data ambrizbiotech/automethyc AutoMethyc -i /data/Lab13/FernandoAmbriz/AutoMet/example/fastq -o /data/Lab13/FernandoAmbriz/AutoMet/Output -r /data/Lab13/FernandoAmbriz/AutoMet/example/ref -f /data/Lab13/FernandoAmbriz/AutoMet/example/Filtro2.csv



```
