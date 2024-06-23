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

df = df[df['Date'] != 'Average:']

df['Date'] = pd.to_datetime(df['Date'], format='%H:%M:%S')
print(df)


df_2 = pd.read_csv('/home/lab13/Documents/FernandoAmbriz/example/output/execution_time.txt', sep = '\t', header = None)

df_2 = df_2[0].str.split('at: ', expand=True)
df_2.columns = ['Command', 'Date']

df_2['Date'] = pd.to_datetime(df_2['Date'], format='%H:%M:%S')

print(df_2.head())

k = 0; lst = []
while k < len(df_2) - 1:
    start = df_2['Date'][k]; end = df_2['Date'][k+1]
    for i,j in zip(df.Date, df.Memory):
        if start <= i <= end:
            c = df_2['Command'][k]
            lst.append([start, end, i, c, j])
    k+=1

df_final = pd.DataFrame(lst)
df_final.columns = ['Start', 'End', 'Second', 'Command', 'Memory']

print(df_final)
