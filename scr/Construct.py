import pandas as pd
import sys

Output=sys.argv[1]

df = pd.read_csv(Output+'/merge.csv')

df_bd = pd.DataFrame()
df_bd['Sample']=df['ID']
df_bd['Status']=df['Status']
df_bd['Chr']=df['0']
df_bd['Start']=df['1']
df_bd['End']=df['2']
df_bd['Met_perc']=df['3']
df_bd['Cyt_Met']= df['4']
df_bd['Cyt_NoMet']=df['5']

df_bd = df_bd.set_index('Sample')

df_bd.to_csv(Output+'/merge.csv')
