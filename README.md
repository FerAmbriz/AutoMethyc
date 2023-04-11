# AutoMethyc
<p align="center">
  <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/AutoMethyc.png" width="250px" height="auto">
</p>

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
The bedGraph file must contain the regions of interest, in order to filter non-specific sequencing products or regions of non-interest. The file format is comma separated values (CSV) with the chromosome, start, end and gene to which each site belongs.
```
Chr,Start,End,Gene
chr17,41277106,41277106,BRCA1
chr17,41277115,41277115,BRCA1
```

## Usage
The usage varies depending on the version used during the installation (with docker or in the $PATH)
### Docker version
With the docker version is recommended to run the docker container in the background so that the execution does not break when leaving the container, moreover to linking and mounting a volume to work with the files of the machine, for this, the volume is mounted in the directory with the files of the user(s) (usually "/home"). And finally the program is executed with AutoMethyc followed by the input parameters.
```
docker run -it -d -v [/home]:[/home] ambrizbiotech/automethyc AutoMethyc \
    -i [fastq_folder] -o [Output_folder] -r [ref_folder] -f [bedGraph.csv] [optional arguments]
```
The output when executing this command is the "container ID" that will be running in the background. To see the execution progress use:
```
docker logs "container ID"
```
### Installed version in PATH
With the version installed in the PATH it is simply executed with AutoMethyc followed by the input parameters
```
AutoMethyc -i [fastq_folder] -o [Output_folder] -r [ref_folder] -f [bedGraph.csv] [optional arguments]
```
## Optional arguments
```
-t --threads    Number of threads. By default use 4
-n --normal     Folder with fastq of normals
```
## Output
### Bisulfite_genome folder
It converts the reference genome into bisulfite and places it in the same folder where the reference genome is located, so that this conversion is done only once.
### Bismark folder
* `02_fastq_trimmed` fastqc output.
* `03_aligned` Ouput of running bismark.
    - `*bt2.bam` All alignments plus methylation call strings.
    - `*report.txt` Alignment and methylation summary.
* `04_deduplicated` Output of deduplicate_bismark. Contain the deduplicate the Bismark alignment BAM file.
* `05_bismark_extractor` Output of bismark_methylation_extractor.
* `06_bedGraph` Output of bismark_methylation_extractor.
### CSV folder
* `Count.csv` Count of regions of interest presents in the samples.
* `Filtered.csv` Merge filtered by regions of interest.
* `merge.csv` Merge of COV files generated by Bismark.
* `Oncoprint.csv` Matrix of percentage of methylation present in each sample by site.
* `OncoprintPromedio.csv` Matrix of mean percentage of methylation present in each gene.
* `OncoprintRellenado.csv` Matrix of percentage of methylation present in each sample by site with null values replaced by 0.
* `CountUF.csv` Count of regions before and after filtering.
* `NotLoc.csv` Count of regions not present in the sample, but present in the bedGraph.

with normals samples
* `OncoprintNorm.csv` Matrix of z-score of methylation present in each site per sample.
* `OncoprintMeanNorm.csv` Mean z-score matrix of methylation present at each site corresponding to one gene per sample.
* `PCA_vectors.csv` PCA vectors grouped by sample type (patient or normal) at each site.

### HTML folder
* `AutoMethyc_Report.html` Report generated by AutoMethyc.
* `multiqc_report.html` Report generated by multiqc.
* `Bismark_report` Folder with reports generated per sample by Bismark.
## HTML report
With the html report, it is planned to give preliminary results that facilitate its general visualization and interpretation.
<img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/Report1.png" width="800px" height="auto">
<img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/Report2.png" width="800px" height="auto">
