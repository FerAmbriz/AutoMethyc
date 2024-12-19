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
