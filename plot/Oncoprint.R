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

# Extraer la columna Gen
gen = as.list(df$Gen)
# Cambiar su estructura a caracter
gen = as.character(gen)
# Eliminar la columna del gen
df <- df[, -c(2)]

mat=as.matrix(df)
rownames(mat) = mat[, 1]

mat = mat[, -c(1)]

col_fun = colorRamp2(c(0, 50, 100), c("gray52", "green", "blue"))
ht1 = Heatmap(mat, name = "met", col = col_fun, show_row_names = FALSE, right_annotation = rowAnnotation(Gen = gen), 
    row_order = order(as.numeric(gsub("row", "", rownames(mat)))))

png(file=output,
width=1000, height=500, res=100)
ht1
dev.off()
