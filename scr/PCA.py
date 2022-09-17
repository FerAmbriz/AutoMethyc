import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import sys

input_df = sys.argv[1]
output = sys.argv[2]

df = pd.read_csv(input_df)
#df = df.drop(df.index[[0,1]])
df = df.drop(['Unnamed: 0', 'ID'], axis=1)
df = df.fillna(0)
df.replace(['inf', '-inf'], 0, inplace=True)
df.replace([np.inf, -np.inf], 0, inplace=True)

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
df_bd = df_bd.T

def funcPCA(df):
    df.replace(['inf', '-inf'], 0, inplace=True)
    df.replace([np.inf, -np.inf], 0, inplace=True)

    x = np.array(df)
    x = x.astype(float)

    #typ = ['Normal'] * len(normals.T)
    #typ = typ + ['Sample'] * len(samples.T)
    df['Type'] = lst

    pca = PCA()
    principalComponents = pca.fit_transform(x)

    dim = list(np.shape(principalComponents))
    dim = dim[1]

    lst2 = []
    for i in range(dim):
        lst2.append('PCA'+ str(i+1))

    principalDf = pd.DataFrame(data = principalComponents, columns = lst2)
    principalDf['Type'] = lst

    return principalDf


# Make PCA
finalDf = funcPCA(df_bd)

finalDf.to_csv(output+"/PCA_vectors.csv")
