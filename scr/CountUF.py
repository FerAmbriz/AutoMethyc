import sys
import pandas as pd

merge_int = sys.argv[1]
filtered = sys.argv[2]
output = sys.argv[3]

df = pd.read_csv(merge_int)
df2 = pd.read_csv(filtered)

sites = pd.DataFrame(df['Sample'].value_counts())
sites.columns=['UnFiltered']

sites2 = pd.DataFrame(df2['Sample'].value_counts())
sites2.columns=['Filtered']

merge = pd.concat([sites, sites2], axis=1, sort=False)

#sacar la diferencia
df = merge.assign(Filter = merge['UnFiltered'] - merge['Filtered'])

#Redondear valores
for i in df.Filter:
    if i > 1000:
        df['Filter'] = df['Filter'].replace({ i : '>1000' })
    elif 1000 >= i >= 200:
        df['Filter'] = df['Filter'].replace({ i : '1000-200' })
    elif i < 200:
        df['Filter'] = df['Filter'].replace({ i : '<200' })
df.to_csv(output+'/CountUF.csv')
