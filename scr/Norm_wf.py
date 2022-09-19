#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import sys

df = pd.read_csv(sys.argv[1], header = None)
output = sys.argv[2]

df = df.fillna(0)
df.columns = df.iloc[1, :]
df = df.drop(df.index[[0,1]])
df = df.rename(columns={0:'Start'})

def normalizado (df,columna):
    site = list(df[columna])
    site.pop(0)
    site.pop(0)

    df_controles = df.T
    df_controles = df_controles[df_controles[2]== 'Normal']
    df_controles = df_controles.drop([2,3], axis=1)

    #Cambiar a valores numericos con lo que se va a hacer la media y std
    columns = df_controles.columns.values
    df_controles[columns] = df_controles[columns].apply(pd.to_numeric, errors='coerce', axis=1)

    df = df.T
    # Delete rows
    df = df.drop(df.index[[0,1]])
    typ = list(df[2])

    # Delete columns
    df = df.drop([2,3], axis=1)
    columns = df.columns.values
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce', axis=1)
    ID = df.index.values


    df_norm = pd.DataFrame()
    j = 4
    n_col = len(columns) + 4

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
norm = normalizado(df, 'Start')
norm.to_csv(output+'/OncoprintNorm.csv')
