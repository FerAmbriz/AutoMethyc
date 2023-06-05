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

    #fig1 = px.imshow(df, labels=dict(x="ID"))
    arr = df.to_numpy()
    fig1 = go.Figure(data=go.Heatmap(
                   z=arr, colorscale='RdBu',
                   x=list(df.columns),
                   y=list(df.index.values) ))

    fig2 = go.Figure(data=[heatmap])

    fig = make_subplots(
        rows=1, cols=2,
        horizontal_spacing=0.05,
        column_widths=[0.9, 0.1], shared_yaxes=True)

    fig.add_trace(fig1.data[0], 1, 1)
    fig.add_trace(fig2.data[0], 1, 2)
    #fig.update_xaxes(ticks="inside")

    fig.update_xaxes(title_text="ID", row=1, col=1)
    fig.update_yaxes(title_text="site", row=1, col=1)

    fig.update_traces(showscale=False, row=1, col=2)
    #fig.update_traces(color_continuous_scale='RdBu_r', row=1, col=1)
    #print(fig.data)
    #fig[1,1].update_yaxes(title_text='site')

    return fig

def plot_mean(df):
    df = df.rename(columns = {'ID':'Gene'})
    df = df.set_index('Gene')
    df = df.drop(df.index[[0,1]])

    fig_mean= px.imshow(df, aspect="auto",  color_continuous_scale='RdBu_r')
    fig_mean.update_xaxes(title_text="ID")

    return fig_mean

def plot_count (df, df2):
    up = max(df.ID)
    rng = up-7

    for i in range(rng):
        df = df.replace({i : '<'+str(rng)})

    values = df['ID'].value_counts().to_list()
    labels= df['ID'].value_counts()
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

def plot_offtarget(df):
    df.columns = ['ID' , 'Count']
    df['Status'] = ['on-target'] * len(df)

#    df2 = pd.DataFrame(df2['ID'].value_counts()).reset_index()
#    df2.columns = ['ID' , 'Count']
#    df2['Status'] = ['off-target'] * len(df2)

    #df = pd.concat([df, df2])

    fig_chr = px.bar(df, x="ID", y="Count")

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
    fig_mean_norm.update_yaxes(title_text="Gene")

    return fig_mean_norm

def plot_manhattan (df):
    df = df.set_index('ID'); df = df.T
    df = pd.DataFrame(df.stack()).reset_index()
    df.columns = ['Site', 'ID', 'Z score']

    ID_normals = list(df[(df['Site']=='Type') & (df['Z score'] == 'Normal')] ['ID'])
    match_ID = lambda ID: 'Normal' if ID in ID_normals else 'Sample'

    df = df.drop(range(0,len(df[df['Site']=='Type'])))
    df['Type'] = list(map (match_ID, df['ID']))

    df [['Chr', 'SpecificSite']] = df['Site'].str.split(':',expand=True)

    df = sortOnco(df)
    manhattan = px.scatter(df, x="Site", y='Z score', color="Type")

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
        # STD zone
        go.Scatter(
            name='Upper normal',
            x=df_n['ID'],
            y=df_n['mean']+df_n['std'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower normal',
            x=df_n['ID'],
            y=df_n['mean']-df_n['std'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='#66A4F3',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='Upper sample',
            x=df_s['ID'],
            y=df_s['mean']+df_s['std'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower sample',
            x=df_s['ID'],
            y=df_s['mean']-df_s['std'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='#F36666',
            fill='tonexty',
            showlegend=False
        ),
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
        xaxis_title='site',
        hovermode="x")
    return fig

def boxplot_site(df):
    fig = px.box(df, x = 'Type' , y="value", labels={
                     "value": "z score"
                 })
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
        # STD zone
        go.Scatter(
            name='Upper normal',
            x=df_n['variable'],
            y=df_n['mean']+df_n['std'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower normal',
            x=df_n['variable'],
            y=df_n['mean']-df_n['std'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='#66A4F3',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='Upper sample',
            x=df_s['variable'],
            y=df_s['mean']+df_s['std'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower sample',
            x=df_s['variable'],
            y=df_s['mean']-df_s['std'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='#F36666',
            fill='tonexty',
            showlegend=False
        ),
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

    fig.update_layout(
        yaxis_title='z score',
        xaxis_title='site',
        hovermode="x"
    )
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

def custom_order_site(df, column):
    df_m = df[df['Statistical'] == 'mean']
    df_m = df_m.sort_values(by=['Sample','Normal'], ascending = False)
    orden_sites = list(df_m[column])
    df = df.set_index(column).loc[orden_sites].reset_index()
    return df

def make_merge_site(chrom, start):
    return chrom + ':' + str(start)

def plot_site_table(df, status):
    if status == 'percentage':
        df['variable'] = list(map(make_merge_site, df['Chr'], df['Start']))
        df = df[['ID', 'Type', 'variable', 'Met_perc']]
        df.columns = ['ID', 'Type', 'variable', 'value']

    df = df.set_index('ID')
    df = df.groupby(by=['variable', 'Type']).agg(['mean', 'std']).reset_index()
    df.columns = ['site', 'Type', 'mean', 'std']
    df = pd.melt(df, id_vars =['site', 'Type'], value_vars =['mean','std'])
    df.columns = ['Site', 'Type', 'Statistical', 'value']
    df = pd.pivot_table(df, index =['Site', 'Statistical'], columns =['Type']).reset_index()
    df.columns = ['Site', 'Statistical', 'Normal', 'Sample']
    df = df.sort_values(by=['Site','Statistical'], ascending = True)
    df = custom_order_site(df, 'Site')
    df = df.dropna()

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    #fill_color='gray',
                    align='left'),
        cells=dict(values=[df['Site'], df['Statistical'], df['Normal'], df['Sample']],
                   #fill_color='#E9E9E9',
                   align='left', height=30))
    ])
    fig.update_layout(
            height=300)
    return fig

def plot_site_table_samples(df):
    df['variable'] = list(map(make_merge_site, df['Chr'], df['Start']))
    df = df[['ID', 'Type', 'variable', 'Met_perc']]
    df.columns = ['ID', 'Type', 'variable', 'value']
    df = df.groupby(by=['variable', 'Type']).agg(['mean', 'std']).reset_index()
    df = pd.melt(df, id_vars =[ ('variable',''),  ('Type','')], value_vars =[('value', 'mean'),('value', 'std')])
    df.columns = ['Site', 'Type', 'x', 'Statistical', 'value']
    df = pd.pivot_table(df, index =['Site', 'Statistical'], columns =['Type']).reset_index()
    df.columns = ['Site', 'Statistical', 'Sample']
    def custom_order_site(df, column):
        df_m = df[df['Statistical'] == 'mean']
        df_m = df_m.sort_values(by=['Sample'], ascending = False)
        orden_sites = list(df_m[column])
        df = df.set_index(column).loc[orden_sites].reset_index()
        return df
    df = custom_order_site(df, 'Site')

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    #fill_color='gray',
                    align='left'),
        cells=dict(values=[df['Site'], df['Statistical'], df['Sample']],
                   #fill_color='#E9E9E9',
                   align='left', height=30))
    ])
    fig.update_layout(
            height=300)
    return fig

def plot_table_mean_gene(df, status):
    if status == 'zscore':
        df  = df.set_index('ID')
    else:
        df  = df.set_index('Gene'); df = df.T
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    df = df.groupby('Type').agg(['mean', 'std']).T
    df = df.reset_index(); df.columns = ['Gene', 'Statistical', 'Normal', 'Sample']
    df = custom_order_site(df, 'Gene')

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    #fill_color='gray',
                    align='left'),
        cells=dict(values=[df['Gene'], df['Statistical'], df['Normal'], df['Sample']],
                   #fill_color='#E9E9E9',
                   align='left', height=30))
    ])
    fig.update_layout(
            height=300)
    return fig

def plot_table_mean_gene_samples(df):
    df  = df.set_index('Gene'); df = df.T
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    df = df.groupby('Type').agg(['mean', 'std']).T
    df = df.reset_index(); df.columns = ['Gene', 'Statistical', 'Sample']

    def custom_order_site(df, column):
        df_m = df[df['Statistical'] == 'mean']
        df_m = df_m.sort_values(by=['Sample'], ascending = False)
        orden_sites = list(df_m[column])
        df = df.set_index(column).loc[orden_sites].reset_index()
        return df
    df = custom_order_site(df, 'Gene')

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    #fill_color='gray',
                    align='left'),
        cells=dict(values=[df['Gene'], df['Statistical'], df['Sample']],
                   #fill_color='#E9E9E9',
                   align='left', height=30))
    ])
    fig.update_layout(
            height=300)
    return fig

def plot_table_pca(df):
    df = df.sort_values(by=['PCA1', 'PCA2'], ascending = False)
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(['Type','PCA1', 'PCA2']),
                    #fill_color='gray',
                    align='left'),
        cells=dict(values=[df['Type'], df['PCA1'], df['PCA2']],
                   #fill_color='#E9E9E9',
                   align='left', height=30))
    ])
    fig.update_layout(
            height=300)
    return fig

def plot_donut_cgi(df):
    df = pd.DataFrame(df['Type'].value_counts()).reset_index()
    df.columns = ['Type', 'Frequency']
    fig = go.Figure(data=[go.Pie(labels=['CpG island', 'CpG shore', 'CpG shelf', 'CpG inter'], values=df['Frequency'], hole=.3)])
    fig.update_traces(marker=dict(colors=['blue', '#3efe00', 'red', '#00fec0']))
    fig.update_layout(height=400)
    return fig
