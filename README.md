# AutoMethyc
This program ...

## Docker container
* https://hub.docker.com/r/ambrizbiotech/automethyc

## Install

### Dependencies
* Bowtie2 v2.4.5 http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#building-from-source
* Samtools v1.15.1-12 http://www.htslib.org/
* Bismark v0.23.0 https://www.bioinformatics.babraham.ac.uk/projects/bismark/
* Anaconda3 v4.12.0 https://www.anaconda.com/ with python v3.9.12
* fastqc v0.11.9 https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* TrimGalore v0.6.6 https://github.com/FelixKrueger/TrimGalore
```
git clone https://github.com/FerAmbriz/AutoMethyc.git
cd AutoMethyc/scr
sudo mv * /usr/bin/
```
## Format of bedGraph
```
Chr,Start,End,Gene
chr17,41277106,41277106,BRCA1
```

## Usage

### Docker version
```
docker run -it -d -v [/home]:[/home] ambrizbiotech/automethyc AutoMethyc \
    -i [fastq_folder] -o [Output_folder] -r [ref_folder] -f [bedGraph.csv]
```
### Installed version
```
AutoMethyc -i [fastq_folder] -o [Output_folder] -r [ref_folder] -f [bedGraph.csv]
```
