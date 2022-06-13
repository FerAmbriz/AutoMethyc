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
#----------------------------------------
ID=len(df_i)
i=0
list=[]

while i < ID:
	list.append(ID_input)
	i=i+1
list = np.array(list)

ID_i = np.array(df['ID'])
# Borrar columnas
df.drop(['ID', 'Unnamed: 0'], axis = 'columns', inplace=True)

#rename columns
df.columns = [0,1,2,3,4,5]
df_i.columns = [0,1,2,3,4,5]

# Unir dataframes
df =pd.concat([df, df_i])
z = np.append(ID_i,list)
df['ID']=z

df.to_csv(Output+'/merge.csv')

