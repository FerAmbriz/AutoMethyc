# AutoMethyc documentation

AutoMethyc is a practical integrative analysis of methylation data from
massive parallel bisulfite sequencing optimized for performance in
massive data analysis.

# Installation

## docker

We created a docker container with all the necessary dependencies to run
the program in order to provide a portable and self-sufficient
container. To install it, you need to have docker installed and then
download the docker image.

``` {.bash language="bash" caption="Download docker container"}
docker pull ambrizbiotech/automethyc
```

Then clone the repository and move to \$PATH the script:
\"automethyc_docker\" for greater simplicity when running the docker
container, being able to use absolute and relative paths.

``` {.bash language="bash" caption="Moving docker container automount script AutoMethyc"}
git clone https://github.com/FerAmbriz/AutoMethyc.git && cd AutoMethyc/scr
sudo mv automethyc_docker /usr/bin/
```

## Local installation

Local installation requires installing all dependencies in \$PATH

**Dependencies**

::: multicols
3

-   [Bowtie2
    v2.4.5](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#building-from-source)

-   [Samtools v1.15.1-12](http://www.htslib.org/)

-   [Bismark
    v0.23.0](https://www.bioinformatics.babraham.ac.uk/projects/bismark/)

-   [python v3.10.6](https://www.python.org/)

    -   [pandas v1.5.2](https://pandas.pydata.org/)

    -   [numpy v1.23.1](https://numpy.org/)

    -   [plotly v5.10.0](https://plotly.com/python/)

    -   [plotly-express
        v0.4.1](https://plotly.com/python/plotly-express/)

    -   [scikit-learn
        v1.1.2](https://scikit-learn.org/stable/index.html)

    -   [tqdm v4.64.1](https://pypi.org/project/tqdm/)

    -   [IPython v8.4.0](https://ipython.org/)

    -   [pysam v0.19.1](https://pysam.readthedocs.io/en/latest/api.html)

-   [fastqc
    v0.11.9](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

-   [TrimGalore v0.6.6](https://github.com/FelixKrueger/TrimGalore)

-   [figlet v2.2.5](http://www.figlet.org/)

-   [multiqc v1.13](https://multiqc.info/)

-   [git v2.34.1](https://git-scm.com/)

-   [wget v1.21.2](https://www.gnu.org/software/wget/)

-   [curl v7.81.0 ](https://curl.se/)

-   [UnZip v6.0]{style="color: customcolor"}

-   [cutadapt v3.5](https://curl.se/)

-   [java v11.0.18](https://www.java.com/en/download/)

-   [gatk v4.3.0.0](https://github.com/broadinstitute/gatk)

-   [R v4.1.2](https://www.r-project.org/)

    -   [gsalib
        v2.2.1](https://www.rdocumentation.org/packages/gsalib/versions/2.2.1)

    -   [ggplot2
        v3.4.2](https://www.rdocumentation.org/packages/ggplot2/versions/3.4.2)

    -   [reshape
        v0.8.9](https://www.rdocumentation.org/packages/reshape/versions/0.8.9)

    -   [gqplots
        v3.1.3](https://cran.r-project.org/web/packages/gplots/index.html)

    -   [tidyverse
        v2.0.0](https://www.rdocumentation.org/packages/tidyverse/versions/2.0.0)

    -   [pROC
        v1.18.5](https://cran.r-project.org/web/packages/pROC/index.html)

    -   [combiROC v 0.3.4](http://combiroc.eu/)

-   [revelio](https://github.com/bio15anu/revelio.git)
:::

And then move the files from the scr folder to the \$PATH

``` {.bash language="bash" caption="Moving the scripts"}
git clone https://github.com/FerAmbriz/AutoMethyc.git && cd AutoMethyc/scr
sudo mv * /usr/bin/
```

# Usage

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

    Chr     Start       End
  ------- ---------- ----------
   chr10   89619506   89619580
   chr11   22647545   22647849

  : With gene

    Chr     Start       End
  ------- ---------- ----------
   chr17   41277106   41277106
   chr17   41277115   41277115

  : With gene

    Chr     Start       End      Gene
  ------- ---------- ---------- -------
   chr10   89619506   89619580   KLLN
   chr11   22647545   22647849   FANCF

  : With gene

# Example usage

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

# Output and interpretation

The output is organized in 4 folders (Bismark, CSV, HTML, VCF).

## ID Assignment

For greater data cleanliness, the ID assignment will be the file name
considering the above to '%\_S\*'. For example: if the original name of
the file is: 'ISD202_S152_L001_R1_001.fastq.gz' its ID will be
\"ISD202\".

## Base call error probability

Base call error probability on logarithmic scale is calculated using
phred score wich are found in: 'CSV/fastqc_raw_data.csv' using FASTQC.

$$Q=-10log_{10} P$$

To improve this and remove low quality sequences trim galore is used
using a default Q\>30. The output is provided in
'CSV/quality_trimming_metrics.csv'

## Non conversion BS

In addition, an estimate of the conversion rate by Bisulfite is
incorporated in 'CSV/non_conversion_metrics.csv', where the metrics show
the equences removed because of apparent non-bisulfite conversion (at
least 3 non-CG calls per read).

## Alignment quality

To evaluate the alignment quality, information is extracted and compiled
into a file to facilitate subsequent reading and analysis of alignment
metrics, such as mapping efficiency, among others in the file
'CSV/quality_alignment_metrics.csv'

## Depth

Additionally, an additional depth filter is added that discards sites
with a depth less than established (by default \>20 readings), where the
metrics are compiled in 'CSV/count_depth_1\_pass.csv'

## Annotator

Regions unique to the raw_data will be annotated for their relationship
to their corresponding gene or regions specified in the BED file using a
request to UCSC genome browser [@karolchik2004ucsc].Therefore it is
important to specify the genome used (default=hg19) with '-g'.

``` {.python language="python" caption="Request UCSC"}
session = requests.Session()
params = {
        'hgsid': '1442153227_FWCo6wJtrFjEzVt07A5mEs5LeL3m',
        'db': genome,
        'hgta_group': 'genes',
        'hgta_track': 'refSeqComposite',
        'hgta_table': 'ncbiRefSeq',
        'hgta_regionType': 'genome',
        'hgta_outputType': 'primaryTable',
        'boolshad.sendToGalaxy': '0',
        'boolshad.sendToGreat': '0',
        'boolshad.sendToGenomeSpace': '0',
        'hgta_outFileName': '',
        'hgta_compressType': 'none',
        'hgta_doTopSubmit': 'get output'
    }
```

The output will be a file in 'CSV/annotated_regions.csv' containing the
annotated regions or in which case a BED file has been provided with the
specified gene it will simply save the BED file as well.

   Chr     Start       End        Gene     Strand    AccessName
  ------ ---------- ---------- ---------- -------- --------------
   chr7   6048904    6048904     AIMP2       \+     NM_0013266\*
   chr3   37034316   37034316   EPM2AIP1     \-     NM_014805.4

  : Considering the BED with genes

    Chr     Start       End      Gene
  ------- ---------- ---------- -------
   chr10   89619506   89619580   KLLN
   chr11   22647545   22647849   FANCF

  : Considering the BED with genes

## Filter target

Once the previously mentioned 'CSV/raw_data' is obtained, it will be
filtered by the regions specified in the BED file o and the
corresponding gene of each site previously annotated in
'CSV/annotated_regions.csv' will be added and saved as:
'filtered_target.csv'

     ID     Type    Chr     Start       End      Met_perc   Cyt_Met   Cyt_NoMet   Depth   Gene
  -------- ------- ------ ---------- ---------- ---------- --------- ----------- ------- ------
   ISD202   cases   chr3   37034307   37034307    100.0      2383         0       2383    MLH1
   ISD202   cases   chr3   37034316   37034316   0.463548     11        2362      2373    MLH1

  : Format of 'CSV/filtered_target.csv'

In addition, a total count of the sites is made after filtering
(targets)

     \-     ID
  -------- -----
   ISD202   337
   ISD203   283

  : Format of 'CSV/count_targets.csv

## CGI mapping

The CGI region mapping makes a request to the UCSC genome browser
[@karolchik2004ucsc] and classifies each site according to distance from
the nearest CpG island.


The output of this mapping will be saved in: 'CSV/cgi_features.csv' with
the information of the nearest CpG island and the mapped site.

   #bin   chrom   chromStart   chromEnd   \...     Site     DistCpGIsland      Type
  ------ ------- ------------ ---------- ------ ---------- --------------- ------------
   1268   chr10    89621772    89624128   \...   89619506       2266        CpG shelf
   631    chr7     6048396     6049255    \...   6048968         \-         CpG island

  : Format of 'CSV/cgi_features.csv'

## Methylation percentage

To calculate the percentage of methylation, the conversion of the
reference genome to bisulfite is carried out using
Bismark[@krueger2011], followed by the use of Trim galore, which
automates quality control and trimming of the adapter using Fastqc,
Trimmomatic [@bolger2014trimmomatic] and Cutadapt [@martin2011cutadapt].
The alignment to the reference genome is done with
bowtie2[@langmead2019scaling] and samtools[@samtools] to finally call
the percentage of methylation. Subsequently, filtering by depth (default
depth\>20) is performed to reduce sequencing errors, which are collected
for a data summary in 'CSV/count_depth\_\[depth
(default=20)\]\_pass.csv'.

     ID     unfiltered   filtered   depth_mean   depth_std     
  -------- ------------ ---------- ------------ ----------- -- --
   ISD202      672         347        572.08     723.23447     
   ISD203      490         225      709.924528   935.77306     

  : Format of 'CSV/count_depth\_\[depth (default=20)\]\_pass.csv

To simplify data analysis, we merge the COV files with the methylation
percentages of each sample into a single file called:
'CSV/raw_data.csv', however, if you want to know more about the files
generated in the 'Bismark' folder, we recommend reading their
documentation.

     ID     Type    Chr     Start       End      Met_perc   Cyt_Met   Cyt_NoMet   Depth
  -------- ------- ------ ---------- ---------- ---------- --------- ----------- -------
   ISD202   cases   chr3   37034307   37034307    100.0      2383         0       2383
   ISD202   cases   chr3   37034316   37034316   0.463548     11        2362      2373

  : Format of 'CSV/raw_data.csv'

## Matrix construction

From the filtered and annotated regions, a matrix of the regions is
constructed to optimize the normalization of the data.

  ------- ---------- ------ ---------- ---------- --------
    ID        \-       \-     ISD202     ISD203    ISD203
   Type       \-       \-    controls   controls   cases
    Chr     Start     Gene      \-         \-        \-
   chr10   89619506   KLLN    98.65      97.50     97.95
   chr10   89619510   KLLN    98.92      97.19     99.18
  ------- ---------- ------ ---------- ---------- --------

  : Format of 'CSV/matrix_filtered_target.csv'

Subsequently, the mean per gene is calculated in a matrix

  ------ ---------- ---------- --------
   Gene    ISD202     ISD203    ISD203
   Type   controls   controls   cases
   KLLN    96.76      96.66     98.65
   ATM      0.29       0.10      0.85
  ------ ---------- ---------- --------

  : Format of 'CSV/matrix_mean_gene.csv'

## Normalization

Normalization is calculated from the mean and standard deviation of the
normals provided, following equation 2.
$$Z_{ij} = \frac {x_{ij}-\overline{x_{j}}}{S_{j}}$$


The normalization output will be saved in:
'CSV/matrix_filtered_target_normalized.csv'

     ID       Type     chr7:6048966   chr2:47596942   chr11:108093572
  -------- ---------- -------------- --------------- -----------------
   ISD202   controls    -0.707107       -0.539522        0.723362
   ISD203    cases       0.478456       3.377785         -0.707107

  : Format of 'CSV/matrix_filtered_target_normalized.csv'

However, the long format of the normalized matrix is also performed in:

     ID       Type       variable       value
  -------- ---------- -------------- -----------
   ISD202   controls   chr7:6048966   -0.707107
   ISD203    cases     chr7:6048966   0.478456

  : Format of 'CSV/filtered_target_normalized.csv'

Subsequently, the mean per gene is calculated in a matrix and the long
format is also performed.

     ID       Type       MSH2       BRIP1
  -------- ---------- ---------- -----------
   ISD202   controls   -.707107   -0.707107
   ISD203    cases     3.421513   3.421513

  : 'CSV/mean_gene_normalized.csv'

     ID       Type     variable    value
  -------- ---------- ---------- ----------
   ISD202   controls     MSH2     0.707107
   ISD203    cases       MSH2     3.421513

  : 'CSV/mean_gene_normalized.csv'

## PCA

To reduce the dimensionality of the data, we did an analysis of
principal components, see the axes of greatest variation and see if
there is a differential grouping between the samples and normals. The
output is in 'CSV/pca_vectors.csv0


## ROC

For Receiver Operating Characteristic (ROC) analysis, the best
combination of sites that allows separation between controls and cases
is identified in an unsupervised manner, where possible combinations
between the sites with the highest number of outliers are performed,
followed by the prediction evaluation using a logistic regression model.
Finally, the ROC curve analysis is performed, evaluating the best
combination.

## Variant calling in germline

Regarding the variant calling, the bam generated with Bismark
[@krueger2011] is ordered with samtools[@samtools], as well as the tags
MD and NM are calculated and the bam index is created. Subsequently
revelio [@nunn2022manipulating] is used for bisulfite-influenced base
masking and with samtools [@samtools] it is added a read group for the
variant calling with HaplotypeCaller [@poplin2017scaling]. The output
will be laid out in 'VCF/\*\_mask_haplotype2.vcf', therefore, we
recommend reading their [[official
documentation]{style="color: blue"}](https://www.rdocumentation.org/packages/gsalib/versions/2.2.1)
for a correct interpretation and subsequent analysis.

## Differential methylation

Differential methylation was made on the comparison of cases and
controls, with a implementation of shapiro wilk test, and t-student or
The Mann-Whitney U test in each site.


## HTML report

For greater ease in the interpretation and visualization of general
data, we compile the information obtained in an interactive HTML report.

# Step-by-Step Execution

To implement the process step-by-step, first create an output folder
along with its subdirectories. Next, initiate the Bismark
implementation, specifying the type of sample. If you have both cases
and controls, run the implementation twice to accommodate your
requirements.

``` {.bash language="bash" caption="Bismark"}
bismark_rounded $input $output $ref_folder $thr $quality $read_fastq cases
```

Next, it filters out shallow sites in both cases and controls
(optional).

``` {.bash language="bash" caption="Depth"}
filter_depth $output/Bismark/cases/bedGraph $output/Bismark/cases $depth cases
```

Finally, merge all the files into one.

``` {.bash language="bash" caption="Merge"}
bindcov $output/Bismark/cases/bedGraph $output/Bismark/cases 'cases'
```

To create the final HTML report, we extract the metrics from FastQC and
Bismark and combine them into a single file.

``` {.bash language="bash" caption="FastQC"}
fastqc_extract $output/Bismark/cases/fastq_trimmed $output/Bismark/cases
extract_statistics_alignment $output/Bismark/cases/fastq_trimmed $output/Bismark/cases/aligned $output/Bismark/cases/deduplicated cases $output/Bismark/cases
```

Optionally, we run MultiQC to view the quality metrics in separate, more
detailed reports. However, AutoMethyc already provides the main quality
metrics in its report.

``` {.bash language="bash" caption="MultiQC"}
multiqc $output/Bismark/controls/fastq_trimmed/*
mv multiqc_report.html $output/HTML/multiqc_report_controls.html
```

If you ran the flow for the cases folder and then the controls, merge
them into a single file and save it in the 'output/CSV' directory.

``` {.bash language="bash" caption="Merge with awk"}
awk '(NR == 1) || (FNR > 1)' $output/Bismark/controls/raw_data.csv $output/Bismark/cases/raw_data.csv > $output/CSV/raw_data.csv

awk '(NR == 1) || (FNR > 1)' $output/Bismark/controls/count_depth_${depth}_pass.csv $output/Bismark/cases/count_depth_${depth}_pass.csv > $output/CSV/count_depth_${depth}_pass.csv

awk '(NR == 1) || (FNR > 1)' $output/Bismark/controls/fastqc_raw_data.csv $output/Bismark/cases/fastqc_raw_data.csv > $output/CSV/fastqc_raw_data.csv

awk '(NR == 1) || (FNR > 1)' $output/Bismark/controls/quality_trimming_metrics.csv $output/Bismark/cases/quality_trimming_metrics.csv > $output/CSV/quality_trimming_metrics.csv

awk '(NR == 1) || (FNR > 1)' $output/Bismark/controls/quality_alignment_metrics.csv $output/Bismark/cases/quality_alignment_metrics.csv > $output/CSV/quality_alignment_metrics.csv

awk '(NR == 1) || (FNR > 1)' $output/Bismark/controls/non_conversion_metrics.csv $output/Bismark/cases/non_conversion_metrics.csv > $output/CSV/non_conversion_metrics.csv

awk '(NR == 1) || (FNR > 1)' $output/Bismark/controls/duplicated_metrics.csv $output/Bismark/cases/duplicated_metrics.csv > $output/CSV/duplicated_metrics.csv
```

Annotation is performed by querying the genomes available in the UCSC
Genome Browser.

``` {.bash language="bash" caption="Annotation"}
region_annotator $filtro $genome $output/CSV $thr
```

Optionally, filter the regions of interest provided by the BED file.

``` {.bash language="bash" caption="Filter target"}
filter_target $output/CSV/raw_data.csv $output/CSV/annotated_regions.csv $output/CSV
```

To have greater control over the normalization process, matrices of the
sites of interest are constructed and then unpivoted.

``` {.bash language="bash" caption="Normalization"}
matrix_normalizer $output/CSV/matrix_filtered_target.csv $output/CSV/matrix_mean_gene.csv $output/CSV

make_vectors_pca $output/CSV/matrix_filtered_target_normalized.csv $output/CSV

unpivot_matrix_normalized $output/CSV/matrix_filtered_target_normalized.csv $output/CSV $output/CSV/matrix_mean_gene_normalized.csv
```

For island classification, mapping is performed based on the CpG islands
reported in the genomes available from the UCSC Genome Browser

``` {.bash language="bash" caption="CGI mapping"}
cgi_mapping $output/CSV/matrix_filtered_target.csv $genome $output/CSV
```

For multivariate analysis using PCA, vectors are extracted from the
normalized data.

``` {.bash language="bash" caption="PCA"}
make_vectors_pca $output/CSV/matrix_filtered_target_normalized.csv $output/CSV
```

A differential expression analysis is then performed using a volcano
plot.

``` {.bash language="bash" caption="Volcano"}
volcano $output/CSV/filtered_target_normalized.csv $output/CSV/
```

To identify the hypermethylated sites with the highest number of
samples, an unsupervised analysis was conducted to evaluate the top 10
sites with the most hypermethylated samples. A comparative analysis of
classification prediction using logistic regression was then performed.
The combination with the highest accuracy in the validation test
(defined by the 30% of data hidden from training) was subsequently
selected for combined ROC analysis.

``` {.bash language="bash" caption="Co methylation"}
co_methylation $output/CSV/matrix_filtered_target_normalized.csv $output/CSV/filtered_target_normalized.csv $output/CSV/ $combinations

Rscript /usr/bin/combi_roc.R $output/CSV
```

For single nucleotide variation (SNV) analysis, the base is masked using
Revelio, and the variants are called using HaplotypeCaller. The number
of identified variants is then counted, and if controls are used, they
are merged into a single file.

``` {.bash language="bash" caption="Revelio and HaplotypeCaller"}
revelio_haplotype $output/Bismark/cases/aligned $ref $output/VCF/cases $thr

snv_count $output/VCF/cases $output/VCF/cases cases
awk '(NR == 1) || (FNR > 1)' $output/VCF/controls/snv_count.csv $output/VCF/cases/snv_count.csv > $output/CSV/snv_count.csv
```

Finally, generate the HTML report, which provides an interactive summary
of the entire analysis.

``` {.bash language="bash" caption="HTML generation"}
html_report $output $output/HTML True $depth
```
