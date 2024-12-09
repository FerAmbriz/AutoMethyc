# Variant calling in germline

For variant calling, the BAM file generated with Bismark [@krueger2011] is sorted using SAMtools [@samtools], with MD and NM tags calculated and the BAM indexed. Next, Revelio [@nunn2022manipulating] is used for bisulfite-influenced base masking. A read group is added using SAMtools before performing the variant calling with HaplotypeCaller [@poplin2017scaling]. The output is saved in VCF/*_mask_haplotype2.vcf. For proper interpretation and further analysis, we recommend consulting their official documentation.
