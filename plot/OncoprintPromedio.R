# Input
args <- commandArgs(trailingOnly = TRUE)
input = args[1]
output = args[2]

# Libraries
library(tidyverse)
library(ggplot2)
library(ComplexHeatmap)
library(circlize)

df = read_csv(input)
df <- df[rowSums(is.na(df)) != ncol(df),]
mat <- df[, -c(1)]

mat=as.matrix(mat, )
rownames(mat) = mat[, 1]
mat = mat[, -c(1)]

class(mat) <- "numeric"

col_fun = colorRamp2(c(0, 50, 100), c("gray52", "green", "blue"))
ht1 = Heatmap(mat, name = "met", col_fun)

png(file=output,
width=1000, height=500, res=100)
ht1
dev.off()
