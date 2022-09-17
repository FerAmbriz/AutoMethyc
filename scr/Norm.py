#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import sys

all_sites = pd.read_csv(sys.argv[1])
onco_mean = pd.read_csv(sys.argv[2])
output = sys.argv[3]

def normalizado (df,columna):
    site = list(df[columna])
    site.pop(0)
    site.pop(0)

    df_controles = df.T
    df_controles = df_controles[df_controles[0]== 'Normal']
    df_controles = df_controles.drop([0,1], axis=1)

    #Cambiar a valores numericos con lo que se va a hacer la media y std
    columns = df_controles.columns.values
    df_controles[columns] = df_controles[columns].apply(pd.to_numeric, errors='coerce', axis=1)

    df = df.T
    # Delete rows
    df = df.drop(df.index[[0,1]])
    typ = list(df[0])

    # Delete columns
    df = df.drop([0,1], axis=1)
    columns = df.columns.values
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce', axis=1)
    ID = df.index.values

    df_norm = pd.DataFrame()
    j = 2
    n_col = len(columns) + 2

    while j < n_col:
        x = list(df_controles[j])
        s = np.std(x)
        m = np.mean(x)

        final = []
        x = list(df[j])

        for i in x:
            norm = (i-m)/s
            final.append(norm)
        df_norm[j] = final
        j = j + 1
    df_norm.columns = site
    df_norm.insert(0,'ID', ID)
    df_norm.insert(1,'Type', typ)
    return df_norm

all_norm = normalizado(all_sites, 'Sample')
all_norm.to_csv(output + '/OncoprintNorm.csv')

mean_norm = normalizado(onco_mean, 'Gen')
mean_norm.to_csv(output + '/OncoprintMeanNorm.csv')

