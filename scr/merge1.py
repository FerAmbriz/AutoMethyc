import sys
import pandas as pd

print('#--------------Construct merge to filter--------------#')
#------------------Input--------------------

# Path df iterado por bash
df_i=pd.read_csv(sys.argv[1], sep='\t', header=None)
ID_input = sys.argv[2]
Output = sys.argv[3]
status = sys.argv[4]
#-------------------------------------------

df_i['ID'] = [ID_input] * len(df_i)
df_i['Status'] = [status] * len(df_i)

df_i.to_csv(Output+'/merge.csv')
#dfmer= pd.merge(df, df_i, how="outer")
#print(dfmer)
