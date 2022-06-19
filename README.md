# AutoMethyc
This program ...

## Docker container
* https://hub.docker.com/r/ambrizbiotech/automethyc

## Install

### Dependencies
* Bowtie2 http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#building-from-source
* Bismark https://www.bioinformatics.babraham.ac.uk/projects/bismark/
* Anaconda3 https://www.anaconda.com/
* fastqc https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* TrimGalore https://github.com/FelixKrueger/TrimGalore
```
git clone

```
## Format of filter


## Usage
```
docker run -it -d -v [/home]:[/home] ambrizbiotech/automethyc AutoMethyc \
    -i [fastq_folder] -o [Output_folder] -r [ref_folder] -f [Filtro.csv]
```
