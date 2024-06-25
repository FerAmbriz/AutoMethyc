import pandas as pd

onum = [3, 4, 5]
path_metrics = '/home/ferambriz/Projects/AutoMethycTest/metrics_test/output_metrics'
path_execution_time = '/home/ferambriz/Projects/AutoMethycTest/metrics_test'

for o in onum:
    df_db = pd.DataFrame()
    for j in list(range(1,10)):
        print(f'{path_metrics}/Grouped_{o}_rep_{j}.tsv')
        df = pd.read_csv(f'{path_metrics}/Grouped_{o}_rep_{j}.tsv', sep = '\t')
        df.columns = ['Command', 'ram_mean', 'ram_std', 'execution']
        df.drop([0,1], inplace = True)

        #print(df)
        df['Group'] = 'Group_' + str(o) + '_rep_' + str(j)
        df_db = pd.concat([df_db, df])
    #print(df_db)
    df_db['ram_mean'] = list(map(float, df_db['ram_mean']))
    df_db['execution'] = list(map(float, df_db['execution']))


    df_db_grouped = df_db.groupby(by = ['Command']).agg(['mean', 'std'])
    print(df_db_grouped)
    df_db_grouped.to_csv(f'{path_metrics}/Metrics_gloabal_{o}.tsv', sep = '\t')
