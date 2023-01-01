FROM rocker/r-ubuntu
#-------------------------- Dependencies -------------------------#
RUN apt-get update && apt-get install -y --no-install-recommends samtools curl libssl-dev libxml2-dev libcurl4-openssl-dev \
  fastqc unzip figlet git git-lfs python3-pip \
  && apt-get install -y cutadapt default-jdk && pip install --no-cache-dir pandas numpy plotly plotly-express scikit-learn tqdm IPython pysam \
  requests multiqc && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.10 /usr/bin/python
RUN R -e "install.packages(c('gsalib', 'ggplot2', 'reshape', 'gplots', 'tidyverse'))"

RUN wget -O bowtie.zip https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.5/bowtie2-2.4.5-linux-x86_64.zip/download \
  && unzip bowtie.zip && mv bowtie2-2.4.5-linux-x86_64/bowtie* /usr/bin && rm -rf bowtie*

RUN wget -O bismark.tar.gz https://github.com/FelixKrueger/Bismark/archive/0.22.3.tar.gz && \ 
  tar xvzf bismark.tar.gz && rm -rf Bismark-0.22.3/*.* Bismark-0.22.3/travis_files \ 
  && mv Bismark-0.22.3/* /usr/bin && rm -rf Bismark* bismark*

RUN curl -fsSL https://github.com/FelixKrueger/TrimGalore/archive/0.6.6.tar.gz -o trim_galore.tar.gz \
  && tar xvzf trim_galore.tar.gz && mv /TrimGalore-0.6.6/trim_galore /usr/bin && rm -rf trim* Trim*

RUN git clone https://github.com/bio15anu/revelio.git && chmod 777 revelio/revelio.py && mv revelio/revelio.py /usr/bin/revelio \
  && rm -rf revelio

RUN git clone https://github.com/broadinstitute/gatk.git && cd gatk && ./gradlew localJar \ 
  && mv gatk /usr/bin/ && mv build/libs/* /usr/bin && cd .. && rm -rf gatk

RUN apt purge -y git git-lfs curl && apt-get -y autoremove \
  && apt-get -y autoclean && rm -rf /tmp/*

COPY scr /usr/bin/
