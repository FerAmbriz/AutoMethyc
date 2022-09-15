import sys
import requests
import io
import csv
import pandas as pd

bed_file = sys.argv[1]
ref = sys.argv[2]
output = sys.argv[3]

url = 'https://genome.ucsc.edu/cgi-bin/hgTables?hgsid=1442153227_FWCo6wJtrFjEzVt07A5mEs5LeL3m'
session = requests.Session()

params = {
        'hgsid': '1442153227_FWCo6wJtrFjEzVt07A5mEs5LeL3m',
        'jsh_pageVertPos': '0',
        'clade': 'mammal',
        'org': 'Human',
        'db': ref,
        'hgta_group': 'regulation',
        'hgta_track': 'cpgIslandExt',
        'hgta_table': 'cpgIslandExt',
        'hgta_regionType': 'genome',
        'hgta_outputType': 'primaryTable',
        'boolshad.sendToGalaxy': '0',
        'boolshad.sendToGreat': '0',
        'boolshad.sendToGenomeSpace': '0',
        'hgta_outFileName': '',
        'hgta_compressType': 'none',
        'hgta_doTopSubmit': 'get output'
}

response = session.post(url, data=params)
df = pd.read_csv(io.StringIO(response.text), sep='\t')

start = list(df.chromStart)

bed = pd.read_csv(bed_file)

df_bd = pd.DataFrame()
lst = []
site = []
typ = []

for loci in list(bed.End):
    df_i = df[df['chromStart'] == min(start, key=lambda x:abs(x-loci))]

    distance = abs(int(df_i.chromStart) - int(loci))
    lst.append(distance)
    site.append(loci)

    if loci in list(range(int(df_i.chromStart), int(df_i.chromEnd), 1)):
        typ.append('cpg island')
    elif distance < 2000:
        typ.append('cpg shore')
    elif 2000 <= distance < 4000:
        typ.append('cpg shelf')
    else:
        typ.append('cpg inter CGI')
    df_bd = pd.concat([df_bd, df_i], ignore_index=True)

df_bd['Original_Site'] = site
df_bd['Distance_StartCpG'] = lst
df_bd['Type'] = typ

df_bd.to_csv(output+'/StatusCpG.csv')
