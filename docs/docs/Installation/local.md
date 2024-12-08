## Local installation

Local installation requires installing all dependencies in \$PATH

**Dependencies**

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

-   UnZip v6.0

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

And then move the files from the scr folder to the \$PATH

``` {.bash language="bash" caption="Moving the scripts"}
git clone https://github.com/FerAmbriz/AutoMethyc.git && cd AutoMethyc/scr
sudo mv * /usr/bin/
```
