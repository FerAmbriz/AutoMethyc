# docker
We created a docker container with all the necessary dependencies to run
the program in order to provide a portable and self-sufficient
container. To install it, you need to have docker installed and then
download the docker image.

``` {.bash language="bash" caption="Download docker container"}
docker pull ambrizbiotech/automethyc
```

Then clone the repository and move to \$PATH the script:
\"automethyc_docker\" for greater simplicity when running the docker
container, being able to use absolute and relative paths.

``` {.bash language="bash" caption="Moving docker container automount script AutoMethyc"}
git clone https://github.com/FerAmbriz/AutoMethyc.git && cd AutoMethyc/scr
sudo mv automethyc_docker /usr/bin/
```
