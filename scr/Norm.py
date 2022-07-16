import pandas as pd
import numpy as np
import sys

onco_all = sys.argv[1]
onco_mean = sys.argv[2]
output = sys.argv[3]

#-----------------------------Read Input---------------------------

all_sites = pd.read_csv(onco_all)
oncomean = pd.read_csv(onco_mean)

#-------------------------------All_sites------------------------

df_controles = all_sites.T
df_controles = df_controles[df_controles[0]== 'Normal']
df_controles = df_controles.drop([0,1], axis=1)

#Cambiar a valores numericos con lo que se va a hacer la media y std
columns = df_controles.columns.values
df_controles[columns] = df_controles[columns].apply(pd.to_numeric, errors='coerce', axis=1)

# Stat
mean = np.array(df_controles.mean())
std = np.array(df_controles.std())

all_sites = all_sites.rename(columns = {'Sample':'Start', 'Unnamed: 1': 'Gen'})

#Multindice en la columna
Status = list(all_sites.iloc[0])
Status.pop(0)
Status.pop(0)
columns = list(all_sites.columns.values)
columns.pop(0)
columns.pop(0)

arrays = [Status, columns]

tuples = list(zip(*arrays))

index_columns = pd.MultiIndex.from_tuples(tuples, names=["Staus", "ID"])

#Multindice en las filas
all_sites = all_sites.drop(all_sites.index[[0,1]])

Start = list(all_sites.Start)
Gen = list(all_sites.Gen)

all_sites = np.array(all_sites.set_index(['Start', 'Gen']))


arrays = [Start, Gen]
tuples = list(zip(*arrays))

index_rows = pd.MultiIndex.from_tuples(tuples, names=["Start", "Gen"])

# Multindixado
all_sites= pd.DataFrame(np.array(all_sites), index=index_rows, columns=index_columns)

#change input to numeric
columns = all_sites.columns.values
all_sites[columns] = all_sites[columns].apply(pd.to_numeric, errors='coerce', axis=1)

norm = (all_sites.T - mean)/std
norm.to_csv(output+'/OncoprintNorm.csv')

#-----------------------------Mean--------------------------

#Transponer la matriz y filtrar los datos
df_controles = oncomean.T
df_controles = df_controles[df_controles[0]== 'Normal']
df_controles = df_controles.drop([0], axis=1)

columns = df_controles.columns.values
df_controles[columns] = df_controles[columns].apply(pd.to_numeric, errors='coerce', axis=1)

mean = np.array(df_controles.mean())
std = np.array(df_controles.std())

Status = list(oncomean.iloc[0])
Status.pop(0)
Status.pop(0)
columns = list(oncomean.columns.values)
columns.pop(0)
columns.pop(0)

arrays = [Status, columns]

tuples = list(zip(*arrays))

index_columns = pd.MultiIndex.from_tuples(tuples, names=["Status", "ID"])

oncomean = oncomean.drop(oncomean.index[[0]])
Gen = list(oncomean.Gen)
oncomean = oncomean.drop(['Sample', 'Gen'], axis=1)

oncomean = pd.DataFrame(np.array(oncomean), index = Gen, columns=index_columns)

columns = oncomean.columns.values
oncomean[columns] = oncomean[columns].apply(pd.to_numeric, errors='coerce', axis=1)

norm = (oncomean.T - mean)/std

norm.to_csv(output+'/OncoprintMeanNorm.csv')
