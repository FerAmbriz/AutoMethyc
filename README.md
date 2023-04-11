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
For this installation option is necessary to install all the dependencies detailed in greater detail in the [documentation](https://github.com/FerAmbriz/AutoMethyc/blob/master/AutoMethyc_Documentation.pdf)

Once the dependencies are installed, move the dependencies in the `scr` folder to the $PATH
```
git clone https://github.com/FerAmbriz/AutoMethyc.git
cd AutoMethyc/scr
sudo mv * /usr/bin/
```
## Usage
### Docker version
With the docker version is recommended to run the docker container in the background so that the execution does not break when leaving the container, moreover to linking and mounting a volume to work with the files of the machine, for this, the volume is mounted in the directory with the files of the user(s) (usually "/home"). And finally the program is executed with AutoMethyc followed by the input parameters.
```
docker run -v [/home]:[/home] -d ambrizbiotech/automethyc automethyc \
    -i [fastq_folder] -o [Output_folder] -r [genome reference file] [optional arguments]
```
The output when executing this command is the "container ID" that will be running in the background. To see the execution progress use:
```
docker logs "container ID"
```
### Installed version in PATH
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
