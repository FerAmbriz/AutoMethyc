import sys
import pandas as pd
import numpy as np

#--------------------Input---------------
# Path df iterado por bash
df_i=pd.read_csv(sys.argv[1], sep='\t', header=None)
# Output 1
Output=sys.argv[3]
df = pd.read_csv(Output+'/merge.csv')
ID_input = sys.argv[2]
status = sys.argv[4]

#----------------------------------------

ID = np.array([ID_input] * len(df_i))
stat = np.array([status] * len(df_i))

ID_i = np.array(df['ID'])
stat_i = np.array(df['Status'])

# Borrar columnas
df.drop(['ID', 'Unnamed: 0', 'Status'], axis = 'columns', inplace=True)

#rename columns
df.columns = list(range(0, len(df.columns), 1))
df_i.columns = list(range(0, len(df.columns), 1))

# Unir dataframes
df =pd.concat([df, df_i])
#Unir listas
z = np.append(ID_i,ID)
df['ID']=z
s = np.append(stat_i,stat)
df['Status'] = s

df.to_csv(Output+'/merge.csv')

