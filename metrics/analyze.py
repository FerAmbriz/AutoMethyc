import pandas as pd

df = pd.read_csv('estadisticas_memoria.txt', sep = '\t', header = None)
df.drop([0], inplace = True)
df = pd.DataFrame(df[0])
#df = df[0].str.split('     ', expand=True)

df_0 = df[0].str.split('    ', expand=True)
df_0.drop(1, inplace = True)

df_1 = pd.DataFrame(df_0[1])
df_1 = df_1[1].str.split('  ',  expand=True)

lst = []

for i,j in zip(df_1[0], df_1[1]):
    if not i:
        lst.append(j)
    else:
        lst.append(i)

df_0['a'] = lst

df = df_0[[0, 'a']]
df.columns = ['Date', 'Memory']

print(df)


df_2 = pd.read_csv('/home/lab13/Documents/FernandoAmbriz/example/output/execution_time.txt', sep = '\t', header = None)

df_2 = df_2[0].str.split('at: ', expand=True)
df_2.columns = ['Command', 'Date']
print(df_2.head())
