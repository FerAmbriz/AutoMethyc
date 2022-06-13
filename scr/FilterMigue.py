#----------------------------libraries--------------------------
#libreria para ejecutar desde la terminal
import sys

import pandas as pd
import numpy as np
from tqdm import trange as tr
from tqdm import tqdm as td

# 1 = Merge.csv
# 2 = Filtro.csv
# 3 = [Output]

# Server
# cd /data/Lab13
#docker run --rm -v $(pwd):/data -it continuumio/anaconda3
#cd /data/FernandoAmbriz/FilterMigue
# python FilterMigue.py Merge.csv Filtro.csv /data/FernandoAmbriz/FilterMigue

print ('')
print ('#-----------------Init Filter -------------------#')
print ('')
#----------------------------Data------------------------------
df = pd.read_csv(sys.argv[1])
dfF = pd.read_csv(sys.argv[2])
OutputFilter = sys.argv[3]

print("Done read csv")
#----------------------------Func------------------------------

def Genloc (u):
	list  = []

	x = df[u].array 
	f = dfF[u].array 
	for i in tr(np.size(x)):
		if x[i] in f:
			start = df.iloc[i][u]
			gen =np.array(dfF.loc[dfF[u] == start])
			gen = gen.flatten().tolist()
			gen = gen[3]
			list.append(gen)
		else:
			list.append(0)
	return list

#-------------------------Extrac----------------------------
FiltroPos = dfF['Start'].array
FiltroChr = dfF['Chr'].array

dataPos = df['Start'].array 
dataChr = df['Chr'].array

print("Done data extraction")
#------------------------Constr---------------------------
print("")
print("#--------------Applying filters--------------#")

df['Gen'] = Genloc('Start')
print("Done FiltroGen")
print("")
print("Done construction df filtered")
print("")

df_filtrado =  df[df['Gen'] != 0]
df_filtrado.to_csv(OutputFilter+"/FiltradoMergue.csv")

ID = df_filtrado['Sample'].value_counts()
ID = pd.DataFrame(ID)
ID.to_csv(OutputFilter+"/FiltradoMergueCount.csv")

#-----------------------NotLoc--------------------------
def GenNotloc (df):
	list = []
	list2 = []
	list3 = []
	x = df['Start'].array 
	f = dfF['Start'].array
	for i in range(np.size(f)):
		if f[i] in x:
			list.append(0)
			list2.append(0)
			list3.append(0)
		else:
			start = dfF.iloc[i]['Start']
			gen = dfF.iloc[i]['Gene']
			chr = dfF.iloc[i]['Chr']
			list.append(start)
			list2.append(gen)
			list3.append(chr)
	return list, list2, list3

#Lista de ID
group = ID.index.values
group = group.tolist()

list = []
list2 = []
list3 = []
list4 = []

print("#-----------Applying filters NotLoc-----------#")

for i in td(group):
	df_gr = df[df['Sample']== i]
	
	x,y,z = GenNotloc(df_gr)

	j=0
	while j < len(x):
		list.append(i)
		j = j+1
	
	list2.extend(z)
	list3.extend(x)
	list4.extend(y)

df_bd = pd.DataFrame()
df_bd['ID'] = list
df_bd['Chr'] = list2
df_bd['Start'] = list3
df_bd['Gen'] = list4

df_NotLoc = df_bd[df_bd['Start'] != 0]
df_NotLoc.to_csv(OutputFilter+"/NotLoc.csv")

print("")
print("Output: " + OutputFilter)
print("""
		(1) FiltradoMergue.csv
		(2) FiltradoMergueCount.csv
		(3) NotLoc.csv
		""")

