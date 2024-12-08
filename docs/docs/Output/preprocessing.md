# Preprocessing

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

| Chr   | Start     | End       | Gene     | Strand | AccessName    |
|-------|-----------|-----------|----------|--------|---------------|
| chr7  | 6048904   | 6048904   | AIMP2    | +      | NM_0013266*   |
| chr3  | 37034316  | 37034316  | EPM2AIP1 | -      | NM_014805.4   |


Considering the BED with genes

| Chr   | Start     | End       | Gene  |
|-------|-----------|-----------|-------|
| chr10 | 89619506  | 89619580  | KLLN  |
| chr11 | 22647545  | 22647849  | FANCF |

## Filter target

Once the previously mentioned 'CSV/raw_data' is obtained, it will be
filtered by the regions specified in the BED file o and the
corresponding gene of each site previously annotated in
'CSV/annotated_regions.csv' will be added and saved as:
'filtered_target.csv'

Format of 'CSV/filtered_target.csv'

| ID     | Type  | Chr  | Start     | End       | Met_perc | Cyt_Met | Cyt_NoMet | Depth | Gene |
|--------|-------|------|-----------|-----------|----------|---------|-----------|-------|------|
| ISD202 | cases | chr3 | 37034307  | 37034307  | 100.0    | 2383    | 0         | 2383  | MLH1 |
| ISD202 | cases | chr3 | 37034316  | 37034316  | 0.463548 | 11      | 2362      | 2373  | MLH1 |




In addition, a total count of the sites is made after filtering
(targets)

Format of 'CSV/count_targets.csv
| ID     | Value |
|--------|-------|
| ISD202 | 337   |
| ISD203 | 283   |


## CGI mapping

The CGI region mapping makes a request to the UCSC genome browser
[@karolchik2004ucsc] and classifies each site according to distance from
the nearest CpG island.


The output of this mapping will be saved in: 'CSV/cgi_features.csv' with
the information of the nearest CpG island and the mapped site.
Format of 'CSV/cgi_features.csv'

| bin   | chrom | chromStart | chromEnd | ... | Site     | DistCpGIsland | Type       |
|-------|-------|------------|----------|-----|----------|---------------|------------|
| 1268  | chr10 | 89621772   | 89624128 | ... | 89619506 | 2266          | CpG shelf  |
| 631   | chr7  | 6048396    | 6049255  | ... | 6048968  | -             | CpG island |
