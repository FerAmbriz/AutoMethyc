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
Format of 'CSV/count_depth\_\[depth (default=20)\]\_pass.csv

| ID     | unfiltered | filtered | depth_mean | depth_std  |
|--------|------------|----------|------------|------------|
| ISD202 | 672        | 347      | 572.08     | 723.23447  |
| ISD203 | 490        | 225      | 709.924528 | 935.77306  |


To simplify data analysis, we merge the COV files with the methylation
percentages of each sample into a single file called:
'CSV/raw_data.csv', however, if you want to know more about the files
generated in the 'Bismark' folder, we recommend reading their
documentation. 
Format of 'CSV/raw_data.csv'

| ID     | Type  | Chr  | Start     | End       | Met_perc | Cyt_Met | Cyt_NoMet | Depth |
|--------|-------|------|-----------|-----------|----------|---------|-----------|-------|
| ISD202 | cases | chr3 | 37034307  | 37034307  | 100.0    | 2383    | 0         | 2383  |
| ISD202 | cases | chr3 | 37034316  | 37034316  | 0.463548 | 11      | 2362      | 2373  |


## Matrix construction

From the filtered and annotated regions, a matrix of the regions is
constructed to optimize the normalization of the data.
Format of 'CSV/matrix_filtered_target.csv'

| ID     | -  | -  | ISD202   | ISD203   | ISD203   |
|--------|----|----|----------|----------|----------|
| Type   | -  | -  | controls | controls | cases    |
| Chr    | Start | Gene | -  | -  | -  |
| chr10  | 89619506 | KLLN | 98.65 | 97.50 | 97.95 |
| chr10  | 89619510 | KLLN | 98.92 | 97.19 | 99.18 |


Subsequently, the mean per gene is calculated in a matrix
Format of 'CSV/matrix_mean_gene.csv'

| Gene | ISD202   | ISD203   | ISD203   |
|------|----------|----------|----------|
| Type | controls | controls | cases    |
| KLLN | 96.76    | 96.66    | 98.65    |
| ATM  | 0.29     | 0.10     | 0.85     |

## Normalization

Normalization is calculated from the mean and standard deviation of the
normals provided, following equation 2.
$$Z_{ij} = \frac {x_{ij}-\overline{x_{j}}}{S_{j}}$$

Format of 'CSV/matrix_filtered_target_normalized.csv'

| ID     | Type     | chr7:6048966 | chr2:47596942 | chr11:108093572 |
|--------|----------|--------------|---------------|-----------------|
| ISD202 | controls | -0.707107    | -0.539522     | 0.723362        |
| ISD203 | cases    | 0.478456     | 3.377785      | -0.707107       |


However, the long format of the normalized matrix is also performed in:
Format of 'CSV/filtered_target_normalized.csv'

| ID     | Type     | variable    | value    |
|--------|----------|-------------|----------|
| ISD202 | controls | chr7:6048966 | -0.707107 |
| ISD203 | cases    | chr7:6048966 | 0.478456 |

Subsequently, the mean per gene is calculated in a matrix and the long
format is also performed. 
'CSV/mean_gene_normalized.csv'

| ID     | Type     | MSH2     | BRIP1    |
|--------|----------|----------|----------|
| ISD202 | controls | -0.707107 | -0.707107 |
| ISD203 | cases    | 3.421513 | 3.421513 |


Format of 'CSV/mean_gene_normalized.csv'

| ID     | Type     | variable | value    |
|--------|----------|----------|----------|
| ISD202 | controls | MSH2     | 0.707107 |
| ISD203 | cases    | MSH2     | 3.421513 |

