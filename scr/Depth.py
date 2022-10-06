import sys
import pandas as pd

inp = sys.argv[1]
output = sys.argv[2]
dep = sys.argv[3]
ID = sys.argv[4]

cov  = pd.read_csv(inp, sep='\t', header = None)

unfiltered = len(cov)

cov['6'] = cov[[4,5]].sum(axis=1)

cov = cov[cov['6'] > int(dep)]
cov = cov.set_index(0)


filtered = unfiltered - len(cov)

depth_mean = cov['6'].mean()
depth_std = cov['6'].std()

df_i = pd.DataFrame({'ID' : [ID],
                     'unfiltered': [unfiltered],
                     'filtered': [filtered],
                     'depth_mean':[depth_mean],
                     'depth_std': [depth_std],
                     })

db = pd.read_csv(output + '/CountUF_depth.csv')
db_i = pd.concat([df_i, db])
db_i = db_i.set_index('ID')

cov.to_csv(inp,  header = None, sep='\t')
db_i.to_csv(output + '/CountUF_depth.csv')
