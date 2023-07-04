# AutoMethyc
<p align="center">
  <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/AutoMethyc.png" width="200px" height="auto">
</p>

AutoMethyc is an integrative pipeline to methylation analysis from raw paired-end sequences obtained from massive parallel bisulfite sequencing.

## Install
### Install with Docker
We created a [docker container](https://hub.docker.com/r/ambrizbiotech/automethyc) with all the necessary dependencies to run the program in order to provide a portable and self-sufficient container. To install it you need to have [docker installed](https://docs.docker.com/engine/install/) and then download the docker image.
```
docker pull ambrizbiotech/automethyc
```
### Local installation
For this installation option is necessary to install all the dependencies detailed in greater detail in the [documentation](https://github.com/FerAmbriz/AutoMethyc/blob/master/Documentation.pdf)

Once the dependencies are installed, move the dependencies in the `scr` folder to the $PATH
```
git clone https://github.com/FerAmbriz/AutoMethyc.git
cd AutoMethyc/scr
sudo mv * /usr/bin/
```
## Usage
### Docker version
In case you are using the version installed with docker, you have to mount the volume (-v) in the corresponding directory and run it in the background (-d) to avoid breaking the process in long execution times. For this, we provide an automount script with the possibility of using relative and absolute path
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
wget -O example.zip https://sourceforge.net/projects/automethycexample/files/latest/download
unzip example.zip && cd example
mkdir output
automethyc_docker -i FastqNormals -n normals -r [hg19_reference_genome_file] -b BedGraph_chr2.csv -o output
```
