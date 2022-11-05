#!/bin/python3

import pandas as pd
import numpy as np
import plotly.express as px
from IPython.display import HTML
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

def sortOnco (df):
    numero_chr = []
    letra_chr = []

    numeros = list(range(1,500, 1))
    numeros = list(map(str,numeros))

    for i in df.Chr:
        if i.removeprefix('chr') in numeros:
            numero_chr.append(int(i.removeprefix('chr')))
            letra_chr.append('NaN')
        else:
            letra_chr.append(i.removeprefix('chr'))
            numero_chr.append(500)

    df ['C'] = numero_chr
    df ['S'] = letra_chr

    df = df.sort_values(['C', 'S'])
    df = df.drop(['C', 'S'], axis = 1)

    return df

def split_base(s):
    lst = list(map(int, s.split('-')))
    m = (int(sum(lst)/len(lst)))
    return m

def plot_fastqc (df):
    df['Mean'] = list(map(float, df.Mean))
    df['#Base'] = list(map(split_base, df['#Base']))
    df['#Base'] = list(map(int, list(df['#Base'])))
    df = df.rename(columns = {'#Base':'Position (pb)', 'Mean': 'Phred Score'})

    fig_fastqc = px.line(df, x="Position (pb)", y="Phred Score", color='ID')
    fig_fastqc.add_hrect(y0=28, y1=42, line_width=0, fillcolor="green", opacity=0.2)
    fig_fastqc.add_hrect(y0=20, y1=28, line_width=0, fillcolor="yellow", opacity=0.2)
    fig_fastqc.add_hrect(y0=0, y1=20, line_width=0, fillcolor="red", opacity=0.2)
    fig_fastqc.update_layout(showlegend=False)

    return fig_fastqc

def plot_depth (df):
    longitud_inicial = len(df)
    longitud_final = longitud_inicial * 2

    lst =[]
    typ = []
    ID = []

    for i, j, z in zip(df.filtered, df.unfiltered, df.ID):
        lst.append(i)
        typ.append('on-target')
        lst.append(j)
        typ.append('off-target')
        lI = [z] * 2
        ID = ID + lI

    while longitud_inicial < longitud_final:
        df.loc[len(df.index)] = ['NaN'] * len (df.columns)
        longitud_inicial = longitud_inicial + 1

    df['Count'] = lst
    df['Type'] = typ
    df['ID'] = ID

    fig_depth = px.bar(df, x="ID", y="Count", color="Type")

    return fig_depth

def discrete_colorscale(bvals, colors):
    if len(bvals) != len(colors)+1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values

    dcolorscale = [] #discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    return dcolorscale

def plot_all (sites_bed, df):
    df = df.drop(['Unnamed: 2'], axis=1)
    df = df.drop(df.index[[0,1]])
    df = df.rename(columns = {'Unnamed: 1':'Start', 'Sample':'Chr'})

    df = sortOnco(df)

    lst = []
    site = []
    for j in df.Start:
        for i,k,c in zip(sites_bed.Site, sites_bed.Type, sites_bed.chrom):
            if int(j) == int(i):
                lst.append(k)
                site.append(str(c) + ':' + str(i))

    # Remplazar los valores
    lst = list(map(lambda x: x.replace('CpG island', '0'), lst))
    lst = list(map(lambda x: x.replace('CpG shore', '1'), lst))
    lst = list(map(lambda x: x.replace('CpG shelf', '2'), lst))
    lst = list(map(lambda x: x.replace('CpG inter CGI', '3'), lst))

    merge = []

    for i,j in zip(df.Chr, df.Start):
        merge.append(str(i) + ':' + str(j))

    df['SiteCpG'] = merge
    df = df.set_index('SiteCpG')
    df = df.drop(['Chr', 'Start'], axis=1)

    df_annot = pd.DataFrame({'SiteCpG': site, 'Type':lst})
    df_annot = df_annot.set_index('SiteCpG')

    # Make array
    z = np.array([list(df_annot.Type)]).T

    bvals = [0, 1, 2, 3 ,4]
    colors = ['blue', '#3efe00', 'red', '#00fec0']

    x = list(range(len(list(df_annot['Type'].value_counts()))+1))
    dcolorsc = discrete_colorscale(x, colors[0:len(list(df_annot['Type'].value_counts()))])

    heatmap = go.Heatmap(z=z, colorscale = dcolorsc,
                    colorbar = dict(thickness=10,
                                tickvals=[0.2, 1, 1.7, 2.2],
                                ticktext=['a', 'b', 'c' ,'d']), x = ['CGI'], y = list(df.index)
                    )

    fig1 = px.imshow(df,  color_continuous_scale='RdBu_r')
    fig2 = go.Figure(data=[heatmap])

    fig = make_subplots(
        rows=1, cols=2,
        horizontal_spacing=0.05,
        column_widths=[0.9, 0.1], shared_yaxes=True)

    fig.add_trace(fig1.data[0], 1, 1)
    fig.add_trace(fig2.data[0], 1, 2)

    return fig

def plot_mean(df):
    df = df.rename(columns = {'Sample':'Gene'})
    df = df.set_index('Gene')
    df = df.drop(df.index[[0,1]])

    fig_mean= px.imshow(df, aspect="auto",  color_continuous_scale='RdBu_r')

    return fig_mean

def plot_count (df, df2):
    up = max(df.Sample)
    rng = up-7

    for i in range(rng):
        df = df.replace({i : '<'+str(rng)})

    values = df['Sample'].value_counts().to_list()
    labels= df['Sample'].value_counts()
    labels = labels.index.values

    values2 = df2['Filter'].value_counts().to_list()
    labels2= df2['Filter'].value_counts()
    labels2=labels2.index.values

    # donut pie chart 2 columns
    fig_samples = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    # Cobertura
    fig_samples.add_trace(go.Pie(labels=labels, values=values, hole=.3, name="Coverage"),
              1, 1)
    # Profundiad
    fig_samples.add_trace(go.Pie(labels=labels2, values=values2, hole=.3, name="Filtered"),
              1, 2)

    fig_samples.update_layout(
        title_text="Statistics", template= "plotly",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='CVR', x=0.20, y=0.5, font_size=20, showarrow=False),
                 dict(text='FTR', x=0.80, y=0.5, font_size=20, showarrow=False)])

    return fig_samples

def plot_offtarget(df, df2):
    df.columns = ['ID' , 'Count']
    df['Status'] = ['on-target'] * len(df)

    df2 = pd.DataFrame(df2['ID'].value_counts()).reset_index()
    df2.columns = ['ID' , 'Count']
    df2['Status'] = ['off-target'] * len(df2)

    df = pd.concat([df, df2])

    fig_chr = px.bar(df, x="ID", y="Count", color="Status", title="Coverage Status")

    return fig_chr

def plot_norm(df):
    df = df.set_index('ID')
    df = df.drop(['Type'], axis=1)
    df = df.T.reset_index()
    df [['Chr', 'SpecificSite']] = df['index'].str.split(':',expand=True)

    df = sortOnco(df)

    df = df.drop(['Chr', 'SpecificSite'], axis = 1)
    df.rename(columns = {'index':'SiteCpG'}, inplace = True)
    df = df.set_index('SiteCpG')

    fig_norm_all = px.imshow(df, aspect="auto", color_continuous_scale='RdBu_r')

    return fig_norm_all

def plot_mean_norm (df):
    df = df.drop(['Type'], axis=1)
    df = df.set_index('ID')

    fig_mean_norm= px.imshow(df.T, aspect="auto",  color_continuous_scale='RdBu_r')

    return fig_mean_norm

def plot_manhattan (df):
    df = df.set_index('ID')
    df = df.T
    df = pd.DataFrame(df.stack()).reset_index()
    df.columns = ['Site', 'ID', 'Z score']
    df [['Chr', 'SpecificSite']] = df['Site'].str.split(':',expand=True)

    df = sortOnco(df)

    manhattan = px.scatter(df, x="Site", y='Z score', color="ID")

    return manhattan

def plot_pca(finalDf):
    finalDf = finalDf.drop(['Unnamed: 0'], axis=1)

    # match columns
    ptr_norm = list(finalDf.Type)
    r = re.compile(".*normal")
    ptr_norm_m = list(filter(r.match, ptr_norm))

    ptr_sample = list(finalDf.Type)
    r = re.compile(".*sample")
    ptr_sample_m = list(filter(r.match, ptr_sample))

    for i in ptr_norm_m:
        finalDf['Type'] = finalDf['Type'].replace([i],'normal')
    for i in ptr_sample:
        finalDf['Type'] = finalDf['Type'].replace([i],'sample')

    fig_pca = px.scatter(finalDf, x='PCA1', y='PCA2',
        color=finalDf['Type'], opacity=0.7,
        labels={'0': 'PC 1', '1': 'PC 2'})

    return fig_pca
