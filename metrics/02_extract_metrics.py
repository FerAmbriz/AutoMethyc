import pandas as pd

onum = [3, 4, 5]
path_metrics = '/home/ferambriz/Projects/AutoMethycTest/metrics_test/output_metrics'
path_execution_time = '/home/ferambriz/Projects/AutoMethycTest/metrics_test'

for o in onum:
    for j in list(range(1,10)):
        print(f'{path_metrics}/Match_Test_{o}_rep_{j}.tsv')
        df = pd.read_csv(f'{path_metrics}/Match_Test_{o}_rep_{j}.tsv', sep = '\t')
        df['Memory'] = list(map(float, df['Memory']))
        print(df)

        df_groupby = df.groupby(by=['Command']).agg(['mean', 'std', pd.Series.nunique])
        print(df_groupby)

        df_groupby.to_csv(f'{path_metrics}/Grouped_{o}_rep_{j}.tsv', sep = '\t')
