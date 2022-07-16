import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sys

input_df = sys.argv[1]
output = sys.argv[2]

df = pd.read_csv(input_df)
df = df.drop(df.index[[0,1]])
df = df.drop(['Unnamed: 1'], axis=1)
df = df.rename(columns = {'Start':'Type'})
df = df.fillna(0)

# Separcion por grupos
normals = df[df['Type'] == 'Normal']
normals = normals.set_index('Type')

samples = df[df['Type'] == 'Sample']
samples = samples.set_index('Type')

#indexado del df original 
df = df.set_index('Type')
columns = list(df.columns.values)

# lista con el nombre de las columnas
lst_normals = []
for i in columns:
    lst_normals.append(i+'_normal')

lst_samples = []
for i in columns:
    lst_samples.append(i+'_sample')

#union de ambas listas
lst = lst_normals + lst_samples

if min(len(normals), len(samples)) == len(samples):
    min_df = 'samples'
else:
    min_df = 'normals'

df_bd = pd.DataFrame(columns = lst)

# Construccion del df para input de PCA
for i in range(max(len(normals), len(samples))):
    if i < min(len(normals), len(samples)):
        n = list(normals.iloc[i])
        s = list(samples.iloc[i])
        row_i = n+s
        df_bd.loc[i]=row_i
    else:
        if min_df == 'samples':
            n = list(normals.iloc[i])
            s = ['NaN'] * len(lst_samples)
            row_i = n+s
            df_bd.loc[i]=row_i
        else:
            n = ['NaN'] * len(lst_normals)
            s = list(samples.iloc[i])
            row_i = n+s
            df_bd.loc[i]=row_i

df_bd.to_csv(output+"/PCA_vectors.csv")

def funcPCA(ubicacion):
    df = pd.read_csv(ubicacion, header = None)
    dfT = df.T
    dfT = dfT.set_index(0)
    dfT.columns = dfT.iloc[0]
    dfT = dfT.iloc[1: , :]
    
    y = dfT.index.values

    df = pd.read_csv(ubicacion)
    df = df.drop(['Unnamed: 0'], axis=1)
    dfT = df.T
    dfT = dfT.reset_index()
    dfT = dfT.drop(['index'], axis=1)

    dfT['Type'] = y
    
    lst = list(range(0,len(df),1))
    features = lst
    x = dfT.loc[:, features].values

    y = dfT.loc[:,['Type']].values# Standardizing the features

    x = np.nan_to_num(x)
    x = StandardScaler().fit_transform(x)

    pca = PCA()
    principalComponents = pca.fit_transform(x)

    dim = list(np.shape(principalComponents))
    dim = dim[1]

    lst2 = []
    for i in range(dim):
        lst2.append('PCA'+ str(i+1))

    principalDf = pd.DataFrame(data = principalComponents, columns = lst2)
    finalDf = pd.concat([principalDf, dfT[['Type']]], axis = 1)

    return finalDf

ubicacion_file = output+"/PCA_vectors.csv"

# Make PCA
finalDf = funcPCA(ubicacion_file)

finalDf.to_csv(output+"/PCA_vectors.csv")
