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
