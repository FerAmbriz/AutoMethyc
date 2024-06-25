import pandas as pd
from tqdm import tqdm

onum = [3, 4, 5]
path_metrics = '/home/ferambriz/Projects/AutoMethycTest/metrics_test/output_metrics'
path_execution_time = '/home/ferambriz/Projects/AutoMethycTest/metrics_test'

#kbmemused

for o in onum:
    for j in list(range(1,10)):
        print(f'{path_metrics}/estadisticas_memoria_{o}_rep_{j}.txt')
        df = pd.read_csv(f'{path_metrics}/estadisticas_memoria_{o}_rep_{j}.txt', sep = '\t', header = None)
        df.drop([0], inplace = True)
        df = pd.DataFrame(df[0])
        #reemplazar cualquier cantidad de espacios consecutivos (dos o más) con un solo espacio:
        #df[0] = df[0].str.replace(r'\s{2,}', ' ')
        df = df[0].str.split(expand=True)
        print(df)
        #df_0 = df[0].str.split(' ', expand=True)
        #df_0.drop(1, inplace = True)

        df = df[[0, 1, 4]]
        df.columns = ['Date', 'Time','Memory']

        df = df[(df['Date'] != 'Average:') & (df['Date']!= 'End')]
        df['Date'] = pd.to_datetime(df['Date'], format='%H:%M:%S')

        df.loc[df['Time'] == 'PM', 'Date'] = (pd.to_datetime(df.loc[df['Time'] == 'PM', 'Date'], format='%H:%M:%S') + pd.Timedelta(hours=12)).dt.strftime('%H:%M:%S')
        df['Date'] = pd.to_datetime(df['Date']).apply(lambda x: x.replace(year=2024, month=6, day=24))

        #df['Date'] = df['Date'].apply(lambda x: x.replace(year=2024, month=6, day=24))

        print(df.head())

        df_2 = pd.read_csv(f'{path_execution_time}/output_{o}_rep_{j}/execution_time.txt', sep = '\t', header = None)
        df_2 = df_2[0].str.split('at: ', expand=True)

        df_2.columns = ['Command', 'Date']
        df_2['Date'] = pd.to_datetime(df_2['Date'], format='%H:%M:%S')
        df_2['Date'] = df_2['Date'].apply(lambda x: x.replace(year=2024, month=6, day=24))

        print(df_2.head())

        k = 0; lst = []
        while k < len(df_2) - 1:
            start = df_2['Date'][k]; end = df_2['Date'][k+1]
            for i,z in zip(df.Date, df.Memory):
                if start <= i <= end:
                    c = df_2['Command'][k]
                    lst.append([start, end, i, c, z])
            k+=1

        df_final = pd.DataFrame(lst)
        df_final.columns = ['Start', 'End', 'Second', 'Command', 'Memory']

        #1GB 1024 * 1024 MB = 1048576
        df_final = df_final[df_final['Memory']!= 'kbmemused']
        df_final['Memory'] = list(map(float, df_final['Memory']))

        df_final['Memory'] = df_final['Memory']/1048576
        print(df_final)
        df_final.to_csv(f'{path_metrics}/Match_Test_{o}_rep_{j}.tsv', sep = '\t', index = False)
