# AutoMethyc
<p align="center">
  <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/AutoMethyc.png" width="200px" height="auto">
</p>

AutoMethyc is an integrative pipeline to methylation analysis from massive parallel bisulfite sequencing. This pipeline provide and comparative approach and integrative analysis from several algorhitms to detect level of methylation, detection of variants, hierarchical grouping and plots. The output of this algorithms are provided in csv file (raw data) and an interactive plots (html).

Overview of the Authometyc

workflow image


## Requeriment

To run Authometyc algorithms, you need:
a) Fastq files (control and samples)
b) Bed (optional)
c) Reference genome (humans and other species)

## Install

Automethyc can be created in two forms. We recommend use docker 

### Install with Docker (recommended)

Pull the authometyc image in docker hub [docker container](https://hub.docker.com/r/ambrizbiotech/automethyc) which containt all dependices to run the algorithm. To install it you need to have [docker installed](https://docs.docker.com/engine/install/) and then download the docker image.

```
docker pull ambrizbiotech/automethyc
```
### Local installation

For this option, it is necessary to install all dependencies, see [documentation](https://github.com/FerAmbriz/AutoMethyc/blob/master/Documentation.pdf)

Once the dependencies are installed, move the dependencies in the `scr` folder to the $PATH
```
git clone https://github.com/FerAmbriz/AutoMethyc.git
cd AutoMethyc/scr
sudo mv * /usr/bin/
```

## Usage
### Docker version

Before run AutoMethyc, you need to have the fastq file and reference genome in a separete directory and mount the volume with the option (-v). The algorhitm is run in background (-d) to avoid breaking the process. For this, we provide an automount script with the possibility of using relative and absolute path
```
automethyc_docker -i [fastq_folder] -o [Output_folder] -r [reference genome file] [optional arguments]
```
The output when executing this command is the "container ID" that will be running in the background. To see the execution progress use:
```
docker logs "container ID"
```
### Local installation
With the version installed in the PATH it is simply executed with AutoMethyc followed by the input parameters
```
automethyc -i [fastq_folder] -o [Output_folder] -r [genome reference file] [optional arguments]
```
## Optional arguments
```
  	-t --threads		Number of threads (default=4)
	-n --normal		Folder with fastq of normals (default=False)
	-g --genome		Genome used for request in UCSC (default=hg19)
		other genomes:
			{hg38, hg19, hg18, hg17, hg16, mm39, mm10, mm9, mm8, mm7}
	-b --bed		File with regions of interest (default=False)
	-d --depth		Minimum depth to consider (default=20)
	-q --quality		Minimum quality (default=30)
	--read		Read type in fastq (default=Paired)
```
## Output
The output is organized in 4 folders (Bismark, CSV, HTML, VCF). However, the explanation in more detail is found in the documentation to be able to carry an adequate interpretation of the results, but we provide a HTML report generated with the summary of the data in an interactive form, named `[Output]/HTML/AutoMethyc_Report.html`
## Example
```
git clone https://github.com/FerAmbriz/AutoMethycTest.git
cd AutoMethycTest && mkdir output
automethyc_docker -i cases -n controls -r [hg19_reference_genome_file] -b BedGraph331.csv -o output
```
The example output is in: [sourceforge](https://sourceforge.net/projects/automethyc-test/files/AutoMethycOutputExample/)
