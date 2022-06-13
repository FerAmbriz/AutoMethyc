import sys
import pandas as pd

print('#--------------Construct merge to filter--------------#')
#------------------Input--------------------

# Path df iterado por bash
df_i=pd.read_csv(sys.argv[1], sep='\t', header=None)
ID_input = sys.argv[2]
Output = sys.argv[3]
#-------------------------------------------


ID=len(df_i)
i=0
list=[]
while i < ID:
	list.append(ID_input)
	i=i+1

df_i['ID']=list
df_i.to_csv(Output+'/merge.csv')
#dfmer= pd.merge(df, df_i, how="outer")
#print(dfmer)
