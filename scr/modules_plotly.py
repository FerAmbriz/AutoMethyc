#!/usr/bin/env python3
#import os
#os.environ['OPENBLAS_NUM_THREADS'] = '1'


import pandas as pd
import numpy as np
import plotly.express as px
from IPython.display import HTML
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from multiprocessing import Pool
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

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

def plot_depth (df, status):
    longitud_inicial = len(df)
    longitud_final = longitud_inicial * 2

    lst =[]; typ = []; ID = []; clase = []

    for i, j, z, c in zip(df.filtered, df.unfiltered, df.ID, df.group):
        lst.append(i); typ.append('high-depth')
        lst.append(j); typ.append('low-depth')
        ID = ID + [z] * 2; clase = clase + [c] * 2


    while longitud_inicial < longitud_final:
        df.loc[len(df.index)] = ['NaN'] * len (df.columns)
        longitud_inicial = longitud_inicial + 1

    df['Count'] = lst; df['Type'] = typ; df['ID'] = ID; df['Group'] = clase

    #fig_depth = px.bar(df, x="ID", y="Count", color="Type", facet_col="Group")
    if status == 'True':
        fig1 = px.bar(df[df['Group'] == 'normal'], x="ID", y="Count", color="Type",
                  color_discrete_map={'high-depth': '#45B39D',
                                      'low-depth': '#EC7063'
                                      })

        fig2 = px.bar(df[df['Group'] == 'sample'], x="ID", y="Count", color="Type")

        fig = make_subplots(rows=1, cols=2)

        for trace in fig1['data']:
            fig.add_trace(trace, row=1, col=1)

        for trace in fig2['data']:
            fig.add_trace(trace, row=1, col=2)

        fig.update_xaxes(title_text="normal", row=1, col=1)
        fig.update_xaxes(title_text="sample", row=1, col=2)
    else:
         fig = px.bar(df, x="ID", y="Count", color="Type")
    return fig

def discrete_colorscale(bvals, colors):
    if len(bvals) != len(colors)+1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values

    dcolorscale = [] #discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    return dcolorscale

def ordered_cluster_euclidean(df):
    #================ rows ===================#
    distancias = pdist(df.values, 'euclidean')
    enlaces = linkage(distancias, method='average')
    # Crear un dendrograma y obtener el orden de las hojas
    dendro = dendrogram(enlaces)
    orden_optimo = dendro['leaves']
    # Ordenar las filas 
    df_ordenado = df.iloc[orden_optimo, :]

    #=============== columns =================#
    df_transpuesto = df_ordenado.T

    distancias = pdist(df_transpuesto.values, 'euclidean')
    enlaces = linkage(distancias, method='average')
    dendro = dendrogram(enlaces)
    orden_optimo = dendro['leaves']

    # Ordenar las columnas
    df_transpuesto_ordenado = df_transpuesto.iloc[orden_optimo, :]
    df_columnas_ordenadas = df_transpuesto_ordenado.T
    return df_columnas_ordenadas

def plot_all (sites_bed, df, group):
    df = sortOnco(df)

    lst_merge = []
    for i,j in zip(df.Chr, df.Start):
        lst_merge.append(str(i) + ':' + str(j))

    df['SiteCpG'] = lst_merge
    df = df.set_index('SiteCpG')
    start = list(df['Start'])
    df = df.drop(['Chr', 'Start'], axis=1)
    df.replace({'NaN':0, np.nan:0}, inplace = True); df = df.astype(float)
    df = ordered_cluster_euclidean(df)

    lst = []; site = []
    for j in start:
        for i,k,c in zip(sites_bed.Site, sites_bed.Type, sites_bed.chrom):
            if int(j) == int(i):
                lst.append(k)
                site.append(str(c) + ':' + str(i))

    # Remplazar los valores
    lst = list(map(lambda x: x.replace('CpG island', '0'), lst))
    lst = list(map(lambda x: x.replace('CpG shore', '1'), lst))
    lst = list(map(lambda x: x.replace('CpG shelf', '2'), lst))
    lst = list(map(lambda x: x.replace('CpG inter CGI', '3'), lst))

    df_annot = pd.DataFrame({'SiteCpG': site, 'Type':lst})
    df_annot = df_annot.set_index('SiteCpG')

    # Make array
    z = np.array([list(df_annot.Type)]).T

    bvals = [0, 1, 2, 3 ,4]
    colors = ['#219518', '#955D14', '#1D9BD6', '#3D58AB']

    x = list(range(len(list(df_annot['Type'].value_counts()))+1))
    dcolorsc = discrete_colorscale(x, colors[0:len(list(df_annot['Type'].value_counts()))])

    heatmap = go.Heatmap(z=z, colorscale = dcolorsc,
                    colorbar = dict(thickness=10,
                                tickvals=[0.2, 1, 1.7, 2.2],
                                ticktext=['a', 'b', 'c' ,'d']), x = ['CGI'], y = list(df.index)
                    )

    #fig1 = px.imshow(df, labels=dict(x="ID"))
    arr = df.to_numpy()
    fig1 = go.Figure(data=go.Heatmap(
                   z=arr, colorscale='RdBu_r',
                   x=list(df.columns),
                   y=list(df.index.values) ))

    fig2 = go.Figure(data=[heatmap])

    colorscale = [[0, '#1f77b4'], [1, '#d62728']]
    fig3 = go.Figure(data=go.Heatmap(
                   z= group.to_numpy().T,
                   x= group.index,
                   y=['Group'],
                   hoverongaps = False, colorscale=colorscale))

    fig = make_subplots(
        rows=2, cols=2,
        horizontal_spacing=0.05, vertical_spacing=0.05,
        column_widths=[0.95, 0.05], row_heights =[0.9, 0.1], shared_yaxes=True, shared_xaxes = True)

    fig.add_trace(fig1.data[0], 1, 1)
    fig.add_trace(fig2.data[0], 1, 2)
    fig.add_trace(fig3.data[0], 2, 1)

    #fig.update_xaxes(ticks="inside")

    fig.update_xaxes(title_text="ID", row=2, col=1)
    fig.update_yaxes(title_text="CpG site", row=1, col=1)

    fig.update_traces(showscale=False, row=1, col=2)
    fig.update_traces(showscale=False, row=2, col=1)
    #fig.update_traces(color_continuous_scale='RdBu_r', row=1, col=1)
    #print(fig.data)
    #fig[1,1].update_yaxes(title_text='site')

    return fig

def plot_mean(df):
    df = df.rename(columns = {'ID':'Gene'})
    df = df.set_index('Gene')

    group = pd.DataFrame(df.iloc[0])
    group['Type'] = group['Type'].replace({'Normal':0, 'Sample':1})

    df = df.drop(df.index[[0]])

    df.replace({'NaN':0, np.nan:0}, inplace = True); df = df.astype(float)
    df = ordered_cluster_euclidean(df)

    arr = df.to_numpy()
    fig_mean = go.Figure(data=go.Heatmap(
                   z=arr, colorscale='RdBu_r',
                   x=list(df.columns),
                   y=list(df.index.values) ))

    colorscale = [[0, '#1f77b4'], [1, '#d62728']]
    fig_annot = go.Figure(data=go.Heatmap(
                   z= group.to_numpy().T,
                   x= group.index,
                   y=['Group'],
                   hoverongaps = False, colorscale=colorscale))


    fig = make_subplots(
        rows=2, cols=1, vertical_spacing=0.05,
        row_heights =[0.9, 0.1], shared_xaxes = True)

    fig.add_trace(fig_mean.data[0], 1, 1)
    fig.add_trace(fig_annot.data[0], 2, 1)

    fig.update_traces(showscale=False, row=2, col=1)
    return fig

def plot_offtarget(on_targets, off_targets, status):
    on_targets.columns = ['ID' , 'Group', 'Count']
    on_targets['Status'] = ['on-target'] * len(on_targets)

    off_targets.columns = ['ID' , 'Group', 'Count']
    off_targets['Status'] = ['off-target'] * len(off_targets)

    df = pd.concat([on_targets, off_targets])
    df = df.replace({'Normal':'normal', 'Sample':'sample'})
    if status == 'True':
        fig1 = px.bar(df[df['Group'] == 'normal'], x="ID", y="Count", color="Status",
                  color_discrete_map={'on-target': '#45B39D',
                                      'off-target': '#EC7063'
                                      })

        fig2 = px.bar(df[df['Group'] == 'sample'], x="ID", y="Count", color="Status")

        fig_chr = make_subplots(rows=1, cols=2)

        for trace in fig1['data']:
            fig_chr.add_trace(trace, row=1, col=1)

        for trace in fig2['data']:
            fig_chr.add_trace(trace, row=1, col=2)

        fig_chr.update_xaxes(title_text="normal", row=1, col=1)
        fig_chr.update_xaxes(title_text="sample", row=1, col=2)

    else:
        fig_chr = px.bar(df, x="ID", y="Count", color='Status')

    return fig_chr

def plot_norm(df):
    df = df.set_index('ID')

    group = pd.DataFrame(df['Type'])
    group['Type'] = group['Type'].replace({'Normal':0, 'Sample':1})

    df = df.drop(['Type'], axis=1)
    df = df.T.reset_index()
    df [['Chr', 'SpecificSite']] = df['index'].str.split(':',expand=True)

    df = sortOnco(df)

    df = df.drop(['Chr', 'SpecificSite'], axis = 1)
    df.rename(columns = {'index':'CpG site'}, inplace = True)
    df = df.set_index('CpG site')

    df.replace({'NaN':0, np.nan:0, np.inf:0, -np.inf:0}, inplace = True); df = df.astype(float)
    df = ordered_cluster_euclidean(df)

    arr = df.to_numpy()
    fig_norm = go.Figure(data=go.Heatmap(
                   z=arr, colorscale='RdBu_r',
                   x=list(df.columns),
                   y=list(df.index.values) ))

    colorscale = [[0, '#1f77b4'], [1, '#d62728']]
    fig_annot = go.Figure(data=go.Heatmap(
                   z= group.to_numpy().T,
                   x= group.index,
                   y=['Group'],
                   hoverongaps = False, colorscale=colorscale))


    fig = make_subplots(
        rows=2, cols=1, vertical_spacing=0.05,
        row_heights =[0.9, 0.1], shared_xaxes = True)

    fig.add_trace(fig_norm.data[0], 1, 1)
    fig.add_trace(fig_annot.data[0], 2, 1)

    fig.update_traces(showscale=False, row=2, col=1)

    return fig

def plot_mean_norm (df):
    df = df.set_index('ID')
    group = pd.DataFrame(df['Type'])
    group['Type'] = group['Type'].replace({'Normal':0, 'Sample':1})

    df = df.drop(['Type'], axis=1)
    df = df.T

    df.replace({'NaN':0, np.nan:0, np.inf:0, -np.inf:0}, inplace = True); df = df.astype(float)
    df = ordered_cluster_euclidean(df)

    arr = df.to_numpy()
    fig_norm = go.Figure(data=go.Heatmap(
                   z=arr, colorscale='RdBu_r',
                   x=list(df.columns),
                   y=list(df.index.values) ))

    colorscale = [[0, '#1f77b4'], [1, '#d62728']]
    fig_annot = go.Figure(data=go.Heatmap(
                   z= group.to_numpy().T,
                   x= group.index,
                   y=['Group'],
                   hoverongaps = False, colorscale=colorscale))

    fig = make_subplots(
        rows=2, cols=1, vertical_spacing=0.05,
        row_heights =[0.9, 0.1], shared_xaxes = True)

    fig.add_trace(fig_norm.data[0], 1, 1)
    fig.add_trace(fig_annot.data[0], 2, 1)

    fig.update_traces(showscale=False, row=2, col=1)

    return fig

def plot_manhattan (df):
    df = df.set_index('ID'); df = df.T
    df = pd.DataFrame(df.stack()).reset_index()
    df.columns = ['Site', 'ID', 'Z score']

    ID_normals = list(df[(df['Site']=='Type') & (df['Z score'] == 'Normal')] ['ID'])
    match_ID = lambda ID: 'normal' if ID in ID_normals else 'sample'

    df = df.drop(range(0,len(df[df['Site']=='Type'])))
    df['Type'] = list(map (match_ID, df['ID']))

    df [['Chr', 'SpecificSite']] = df['Site'].str.split(':',expand=True)

    df = sortOnco(df)
    manhattan = px.scatter(df, x="Site", y='Z score', color="Type", opacity=0.7)

    manhattan.update_layout(yaxis_title='Z-score',
        xaxis_title='CpG site')

    return manhattan

def plot_pca(finalDf):
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

def merge_site(chrom, site):
    return chrom + ':' + site

def plot_site_percent(df):
    if 'Unnamed: 2' in list(df.columns):
        df = df.drop(['Unnamed: 2'], axis=1)
        df = df.drop([1])
        patients = pd.DataFrame(df.iloc[0])
        df = df.drop([0])


    else:
        df.columns = list(df.iloc[0])
        df = df.drop([0, 2])
        df.rename(columns = {np.nan:'Unnamed: 1'}, inplace = True)
        patients = pd.DataFrame(df.iloc[0])
        df = df.drop([1])

    patients = patients.drop(['ID', 'Unnamed: 1'])
    patients = patients.reset_index()
    patients.columns = ['index', 0]
    df['ID'] = list(map(merge_site, df['ID'], df['Unnamed: 1']))
    df = df.drop(['Unnamed: 1'], axis=1)

    columns = list(df.columns)
    columns.pop(0)
    df_melt = pd.melt(df, id_vars=['ID'], value_vars=columns)

    def match_type(ID):
        patients_i = patients[patients['index']==ID]
        return list(patients_i[0])[0]

    df_melt['Type'] = list(map(match_type, df_melt['variable']))

    df_melt['value'] = list(map(float, df_melt['value']))
    df_melt = df_melt.drop(['variable'], axis=1)

    m = df_melt.groupby(['ID', 'Type']).mean()
    m.columns = ['mean']

    s = df_melt.groupby(['ID', 'Type']).std()
    s.columns = ['std']

    df_final = pd.concat([m,s], axis=1).reset_index()
    df_s = df_final[df_final['Type'] == 'Sample']
    df_n = df_final[df_final['Type'] == 'Normal']

    fig = go.Figure([
        go.Scatter(
            name='normal',
            x=df_n['ID'],
            y=df_n['mean'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='sample',
            x=df_s['ID'],
            y=df_s['mean'],
            mode='lines',
            line=dict(color='red'),
        )
    ])

    fig.update_layout(
        yaxis_title='methylation %',
        xaxis_title='CpG site',
        hovermode="x")
    return fig

def boxplot_site(df):
    df['Type'] = df['Type'].replace({"Sample": "sample", "Normal": "normal"})
    fig = px.violin(df, x = 'Type' , y="Met_perc", points = "all", box = True, color = 'Type',
                 labels={"Met_perc": "methylation %"})
    #fig.add_trace(px.strip(df, x='Type', y='value', color='Type').data[0])
    return fig

def plot_site_norm(df):
    df = df.drop(['ID'], axis = 1)
    m = df.groupby(['variable', 'Type']).mean()
    m.columns = ['mean']

    s = df.groupby(['variable', 'Type']).std()
    s.columns = ['std']

    df_final = pd.concat([m,s], axis=1).reset_index()

    df_s = df_final[df_final['Type'] == 'Sample']
    df_n = df_final[df_final['Type'] == 'Normal']

    fig = go.Figure([

        go.Scatter(
            name='normal',
            x=df_n['variable'],
            y=df_n['mean'],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        go.Scatter(
            name='sample',
            x=df_s['variable'],
            y=df_s['mean'],
            mode='lines',
            line=dict(color='red'),
        )
    ])
    fig.update_layout(yaxis_title='Z-score',
        xaxis_title='CpG site')
    return fig

def plot_options(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    #fill_color='gray',
                    align='left'),
        cells=dict(values=[df.Parameter, df.Value],
                   #fill_color='#E9E9E9',
                   align='left', height=30))
    ])
    fig.update_layout(
            height=300)
    return fig

def plot_global_percent(df):
    df = df[['Type','Met_perc']]
    df = df.groupby('Type').agg(['mean', 'std'])
    df = df.reset_index()
    df.columns = ['Type', 'mean', 'std']

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    #fill_color='gray',
                    align='left'),
        cells=dict(values=[df['Type'], df['mean'], df['std']],
                   #fill_color='#E9E9E9',
                   align='left', height=30))
    ])
    fig.update_layout(
            height=300)
    return fig

def make_merge_site(chrom, start):
    return chrom + ':' + str(start)

def custom_order_site(df):
    df_m = df[df['Type'] == 'Sample']
    df_m = df_m.sort_values(by=['mean'], ascending = False)
    orden_sites = list(df_m['CpG site'])
    df = df.set_index('CpG site').loc[orden_sites].reset_index()
    return df

def custom_order_gene(df):
    df_m = df[df['Type'] == 'Sample']
    df_m = df_m.sort_values(by=['mean'], ascending = False)
    orden_sites = list(df_m['Gene'])
    df = df.set_index('Gene').loc[orden_sites].reset_index()
    return df

def plot_site_table(df, status, bed):
    def annot_gene(site_df):
        lst = list(bed[bed['Site'] == site_df]['Gene'])
        if len(lst) > 1:
            if lst[0] != lst[1]:
                lst[0] = f'{lst[0]}-{lst[1]}'
        else:
            lst[0] = f'{lst[0]}'
        return lst[0]

    if status == 'percentage':
        df['variable'] = list(map(make_merge_site, df['Chr'], df['Start']))
        df = df[['ID', 'Type', 'variable', 'Gene', 'Met_perc']]
        df.columns = ['ID', 'Type', 'variable', 'Gene', 'value']
    else:
        bed['Site'] = list(map(make_merge_site, bed['Chr'], bed['Start']))
        df['Gene'] = list(map(annot_gene, df['variable']))
    df = df.set_index('ID')
    df = df.groupby(by=['variable', 'Gene', 'Type',]).agg(['mean', 'std']).reset_index()
    df.columns = ['CpG site', 'Gene', 'Type', 'mean', 'std']
    df = custom_order_site(df); df = df.dropna()

    fig = go.Figure(go.Table(header=dict(values=list(df.columns), align="left"),
                cells=dict(
                    values=[df["CpG site"], df['Gene'],  df["Type"], df["mean"], df["std"]],
                    align="left", height=30)))
    fig.update_layout(updatemenus=[{
            "buttons": [
                {
                    "label": c,
                    "method": "update",
                    "args": [
                        { "cells": {
                            "values": df.T.values
                            if c == "All"
                                else df.loc[df["Type"].eq(c)].T.values
                            }
                        }
                    ],
                }
                for c in ["All"] + df["Type"].unique().tolist()
            ]
        }])
    fig.update_layout(height=300)
    return fig

def plot_table_mean_gene(df, status):
    if status == 'zscore':
        df = df[['variable', 'Type', 'value']]; df.columns = ['Gene', 'Type', 'value']
    else:
        df = df[['Gene','Met_perc', 'Type']]

    df = df.groupby(['Gene','Type']).agg(['mean', 'std']).reset_index()
    df.columns=['Gene', 'Type', 'mean', 'std']

    df = custom_order_gene(df); df = df.dropna()

    fig = go.Figure(go.Table(header=dict(values=list(df.columns), align="left"),
                cells=dict(
                    values=[df['Gene'],  df["Type"], df["mean"], df["std"]],
                    align="left", height=30)))
    fig.update_layout(updatemenus=[{
            "buttons": [
                {
                    "label": c,
                    "method": "update",
                    "args": [
                        { "cells": {
                            "values": df.T.values
                            if c == "All"
                                else df.loc[df["Type"].eq(c)].T.values
                            }
                        }
                    ],
                }
                for c in ["All"] + df["Type"].unique().tolist()
            ]
        }])
    fig.update_layout(height=300)

    return fig


def plot_table_pca(df, bed):
    bed['Site'] = list(map(make_merge_site, bed['Chr'], bed['Start']))
    def annot_gene(site_df):
        lst = list(bed[bed['Site']==site_df]['Gene'])
        if len(lst) > 1:
            if lst[0] != lst[1]:
                lst[0] = f'{lst[0]}-{lst[1]}'
        else:
            lst[0] = f'{lst[0]}'
        return lst[0]

    df[['CpG site', 'Type']] = df['Type'].str.split('_', expand=True)
    df['Gene'] = list(map(annot_gene, df['CpG site']))
    df = df[['CpG site', 'Gene', 'Type', 'PCA1','PCA2']]
    df = df.sort_values(by=['PCA1', 'PCA2'], ascending = False)

    fig = go.Figure(go.Table(header=dict(values=list(df.columns), align="left"),
                cells=dict(
                    values=[df["CpG site"], df['Gene'],  df["Type"], df["PCA1"], df["PCA2"]],
                    align="left", height=30)))
    fig.update_layout(updatemenus=[{
            "buttons": [
                {
                    "label": c,
                    "method": "update",
                    "args": [
                        { "cells": {
                            "values": df.T.values
                            if c == "All"
                                else df.loc[df["Type"].eq(c)].T.values
                            }
                        }
                    ],
                }
                for c in ["All"] + df["Type"].unique().tolist()
            ]
        }])
    fig.update_layout(height=300)
    return fig

def plot_donut_cgi(df):
    df = pd.DataFrame(df['Type'].value_counts()).reset_index()
    df.columns = ['Type', 'Frequency']
    fig = go.Figure(data=[go.Pie(labels=['CpG island', 'CpG shore', 'CpG shelf', 'CpG inter'], values=df['Frequency'], hole=.3)])
    fig.update_traces(marker=dict(colors=['219518', '#955D14', '#1D9BD6', '#3D58AB']))
    fig.update_layout(height=400)
    return fig

def plot_count_snv(df):
    fig  = px.bar(df, x = 'ID', y = 'Count', color = 'group')
    return fig
