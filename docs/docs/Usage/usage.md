# Usage
## Command to run
We provide a series of default values for simplicity when running with a
single command where the only mandatory parameters are the directory
path where all the files with FASTQ (\*.f\*), the genome reference file
and the output directory.

``` {.bash language="bash" caption="Running automethyc"}
automethyc -i [fastq_folder] -o [Output_folder] -r [reference genome file] [optional arguments]
```

On the other hand, greater flexibility is offered when running the
program by establishing default parameters that can be modified by the
user.

``` {.bash language="bash" caption="Optional arguments"}
-t --threads      # Number of threads (default=4)
-n --normal       # Folder with fastq of normals (default=False)
-g --genome       # Genome used for request in UCSC (default=hg19)
-b --bed          # File with regions of interest (default=False)
-d --depth        # Minimum depth to consider (default=20)
-q --quality      # Minimum quality (default=30)    
-c --combinations # Number of outliers considered to combinations in the evaluation for logistic 
                  # regression (default=10)
-rb --run_background    # Run on background
--read            # Read type in fastq (default=Paired)
```

In case you are using the version installed with docker, you have to
mount the volume (-v) in the corresponding directory and run it in the
background (-d) to avoid breaking the process in long execution times.
For this, we provide an automount script with the possibility of using
relative and absolute paths.

``` {.bash language="bash" caption="Running automethyc in docker container"}
automethyc_docker -i [fastq_folder] -o [Output_folder] -r [reference genome file] [optional arguments]
```

## Format of bed file

The BED file must contain the regions of interest, to filter nonspecific
sequencing products or regions of noninterest. The file format is comma
separated values (CSV) with the chromosome, start and end, presenting
different formats for greater versatility.


| Chr   | Start     | End       |
|-------|-----------|-----------|
| chr10 | 89619506  | 89619580  |
| chr11 | 22647545  | 22647849  |

Or with gene

| Chr   | Start     | End       | Gene  |
|-------|-----------|-----------|-------|
| chr10 | 89619506  | 89619580  | KLLN  |
| chr11 | 22647545  | 22647849  | FANCF |


## Example usage

In this trial, we conducted a comprehensive analysis of 10 samples (5
cases and 5 controls) from these previously generated datasets. The raw
fastq files for bioinformatic analysis are accessible at SRR25023301,
SRR25023302, SRR25023303, SRR25023304, SRR25023305 for cases and
SRR25023039, SRR25023040, SRR25023041, SRR25023042, SRR25023043 for
controls [@RuizDeLaCruz2024].

``` {.bash language="bash" caption="Example usage"}
git clone https://github.com/FerAmbriz/AutoMethycTest.git
cd AutoMethycTest && mkdir output
automethyc_docker -i cases -n controls -r [hg19_reference_genome_file] -b BedGraph331.csv -o output
```
