import sys
import requests
import io
import csv
import pandas as pd

bed_file = sys.argv[1]
ref = sys.argv[2]
output = sys.argv[3]

# Web scrapping
url = 'https://genome.ucsc.edu/cgi-bin/hgTables?hgsid=1442153227_FWCo6wJtrFjEzVt07A5mEs5LeL3m'
session = requests.Session()

params = {
        'hgsid': '1442153227_FWCo6wJtrFjEzVt07A5mEs5LeL3m',
        'db': 'hg19',
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
db = pd.read_csv(io.StringIO(response.text), sep='\t')

bed = pd.read_csv(bed_file)

def distance (loci, db):
    dist = loci-db
    return abs(dist)

dist_min =  []
df_bd = pd.DataFrame()
original = []
typ = []

for crm, loci in zip(bed.Chr, bed.Start):
    db_i = db[db['chrom'] == crm]

    original = [loci] * len(db_i)
    all_dist = []

    for i,j in zip(db_i.chromStart, db_i.chromEnd):
        if distance(loci, i) < distance(loci, j):
            all_dist.append(distance(loci, i))
        else:
            all_dist.append(distance(loci, j))

    db_i['Site'] = original
    db_i['DistCpGIsland'] = all_dist

    db_i = db_i[db_i['DistCpGIsland'] == db_i['DistCpGIsland'].min()]

    df_bd = pd.concat([df_bd, db_i])

typ = []
dist = []
for loci, start, end, distance in zip(df_bd.Site, df_bd.chromStart, df_bd.chromEnd, df_bd.DistCpGIsland):
    if loci in list(range(start, end, 1)):
        typ.append('CpG island')
        dist.append('-')
    elif distance < 2000:
        typ.append('cpg shore')
        dist.append(distance)
    elif 2000 <= distance < 4000:
        typ.append('cpg shelf')
        dist.append(distance)
    else:
        typ.append('cpg inter CGI')
        dist.append(distance)

df_bd['Type'] = typ
df_bd['DistCpGIsland'] = dist

df_bd.to_csv(output+'/StatusCpG.csv')
