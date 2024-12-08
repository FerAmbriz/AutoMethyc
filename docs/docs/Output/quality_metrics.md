# Quality metrics
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
