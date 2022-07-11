# AutoMethyc
AutoMethyc is a pipeline automated which aims for simplicity and practicality in methylation analysis.

## Install with Docker
We created a [docker container](https://hub.docker.com/r/ambrizbiotech/automethyc) with all the necessary dependencies to run the program. To install it you need to have [docker installed](https://docs.docker.com/engine/install/) and then download the docker image.
```
docker pull ambrizbiotech/automethyc
```
## Install in PATH
For this installation option is necessary to install all the dependencies.
### Dependencies
* Bowtie2 v2.4.5 http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#building-from-source
* Samtools v1.15.1-12 http://www.htslib.org/
* Bismark v0.23.0 https://www.bioinformatics.babraham.ac.uk/projects/bismark/
* Anaconda3 v4.12.0 https://www.anaconda.com/ with python v3.9.12
* fastqc v0.11.9 https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
* TrimGalore v0.6.6 https://github.com/FelixKrueger/TrimGalore

And then move the files from the `scr` folder to the $PATH
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
