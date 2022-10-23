FROM continuumio/anaconda3
#-------------------------- Dependencies -------------------------#
RUN apt-get update && apt-get install -y samtools \
  fastqc cutadapt unzip figlet && pip install multiqc \
  && rm -rf /var/lib/apt/lists/*

RUN wget -O bowtie.zip https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.5/bowtie2-2.4.5-linux-x86_64.zip/download
RUN unzip bowtie.zip
RUN mv bowtie2-2.4.5-linux-x86_64/bowtie* /usr/bin
RUN rm -rf bowtie*

RUN wget -O bismark.tar.gz https://github.com/FelixKrueger/Bismark/archive/0.22.3.tar.gz && \ 
  tar xvzf bismark.tar.gz
RUN rm -rf Bismark-0.22.3/*.* Bismark-0.22.3/travis_files
RUN mv Bismark-0.22.3/* /usr/bin && rm -rf Bismark* bismark*

RUN curl -fsSL https://github.com/FelixKrueger/TrimGalore/archive/0.6.6.tar.gz -o trim_galore.tar.gz
RUN tar xvzf trim_galore.tar.gz
RUN mv /TrimGalore-0.6.6/trim_galore /usr/bin && rm -rf trim* Trim*

COPY scr/ /usr/bin
