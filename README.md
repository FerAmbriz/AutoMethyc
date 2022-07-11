# AutoMethyc
AutoMethyc is a pipeline automated which aims for simplicity and practicality in methylation analysis.
## Install
### Install with Docker
We created a [docker container](https://hub.docker.com/r/ambrizbiotech/automethyc) with all the necessary dependencies to run the program in order to provide a portable and self-sufficient container. To install it you need to have [docker installed](https://docs.docker.com/engine/install/) and then download the docker image.
```
docker pull ambrizbiotech/automethyc
```
### Install in PATH
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
The bedGraph file must contain the regions of interest, in order to filter non-specific sequencing products or regions of non-interest. The file format is comma separated values (CSV) with the chromosome, start, end and gene to which each site belongs
```
Chr,Start,End,Gene
chr17,41277106,41277106,BRCA1
chr17,41277115,41277115,BRCA1
```

## Usage
The usage varies depending on the version used during the installation (with docker or in the $PATH)
### Docker version
With the docker version is recommended to run the docker container in the background so that the execution does not break when leaving the container, in addition to linking and mounting a volume to work with the files of the machine. And finally the program is executed with AutoMethyc followed by the input parameters
```
docker run -it -d -v [/home]:[/home] ambrizbiotech/automethyc AutoMethyc \
    -i [fastq_folder] -o [Output_folder] -r [ref_folder] -f [bedGraph.csv]
```
### Installed version in PATH
With the version installed in the PATH it is simply executed with AutoMethyc followed by the input parameters
```
AutoMethyc -i [fastq_folder] -o [Output_folder] -r [ref_folder] -f [bedGraph.csv]
```
## Optional arguments
```
-t --threads    Number of threads. By default use 4
```
## Output
### Bismark folder
Contains all Bismark values
* 02
* 03
* 04
* 05
* 06
### CSV folder
* Oncoprint.csv
* merge.csv
* Filtrado.csv
* 
### HTML folder
* Automethyc_report.html
* multiqc
* Bismark


