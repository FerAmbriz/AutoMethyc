AutoMethyc documentation
========================

AutoMethyc is a practical integrative analysis of methylation data from massive parallel bisulfite sequencing optimized for performance in massive data analysis.

Installation
--------

We created a docker container with all the necessary dependencies to run the program in order to provide a portable and self-sufficient container. To install it, you need to have docker installed and then download the docker image.

::

   docker pull ambrizbiotech/automethyc

Then clone the repository and move to \$PATH the script: "automethyc_docker" for greater simplicity when running the docker container, being able to use absolute and relative paths.


Project layout
--------------

::

   mkdocs.yml    # The configuration file.
   docs/
       index.md  # The documentation homepage.
       ...       # Other markdown pages, images and other files.
