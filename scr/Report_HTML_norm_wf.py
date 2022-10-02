#!/usr/bin/env python
# coding: utf-8

# # Rerport HTML

import pandas as pd
import plotly.express as px
from IPython.display import HTML
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import numpy as np

input_folder = sys.argv[1]
Output = sys.argv[2]

Oncoprint_All = input_folder+'/CSV/Oncoprint_wf.csv'
OncoprintNorm = input_folder+'/CSV/OncoprintNorm.csv'
PCA_data = input_folder+'/CSV/PCA_vectors.csv'
bed = input_folder+'/CSV/StatusCpG.csv'

print('#-------------------Plotting-------------------------')

#------------------------All_sites ------------------
sites_bed = pd.read_csv(bed)

df = pd.read_csv(Oncoprint_All)
df.columns = df.loc[0]
df = df.drop(['Sample'], axis=1)
df = df.drop(df.index[[0,1,2]])
df = df.rename(columns = {np.nan:'Start'})

lst = []
site = []
for j in df.Start:
    for i,k in zip(sites_bed.Site, sites_bed.Type):
        if int(j) == int(i):
            lst.append(k)
            site.append(i)

df = df.set_index('Start')

# Remplazar los valores
lst = list(map(lambda x: x.replace('CpG island', '0'), lst))
lst = list(map(lambda x: x.replace('CpG shore', '1'), lst))
lst = list(map(lambda x: x.replace('CpG shelf', '2'), lst))
lst = list(map(lambda x: x.replace('CpG inter CGI', '3'), lst))

df_annot = pd.DataFrame({'Site': site, 'Type':lst})
df_annot = df_annot.set_index('Site')

# Make array
z = np.array([list(df_annot.Type)]).T

def discrete_colorscale(bvals, colors):
    if len(bvals) != len(colors)+1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values

    dcolorscale = [] #discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    return dcolorscale

if len(list(df_annot['Type'].value_counts())) == 3:
    bvals = [0, 1, 2, 3]
    colors = ['blue', '#3efe00', 'red']
    dcolorsc = discrete_colorscale(bvals, colors)
    heatmap = go.Heatmap(z=z, colorscale = dcolorsc,
                     colorbar = dict(thickness=10,
                                     tickvals=[0.2, 1, 1.7],
                                     ticktext=['a', 'b', 'c']), x = ['Type'], y = list(df.index)
                    )
    fig1 = px.imshow(df, color_continuous_scale='RdBu_r')
    #ff.create_annotated_heatmap(z1, x.tolist(), y.tolist(),  colorscale='matter')
    fig2 = go.Figure(data=[heatmap])


    fig = make_subplots(
        rows=1, cols=2,
        horizontal_spacing=0.05,
        column_widths=[0.9, 0.1], shared_yaxes=True
    )

    fig.add_trace(fig1.data[0], 1, 1)
    fig.add_trace(fig2.data[0], 1, 2)


    fig.add_annotation(text='CpG island                CpG shore                CpG shelf',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.3,
                        y=-0.13,
                        borderwidth=1)

    fig.add_annotation(text='',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.28,
                        y=-0.126,
                        bgcolor=colors[0],
                        borderwidth=7)
    fig.add_annotation(text='',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.41,
                        y=-0.126,
                        bgcolor=colors[1],
                        borderwidth=7)
    fig.add_annotation(text='',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.525,
                        y=-0.126,
                        bgcolor=colors[2],
                        borderwidth=7)
else:
    bvals = [0, 1, 2, 3 ,4]
    colors = ['blue', '#3efe00', 'red', '#00fec0']
    x = list(range(len(list(df_annot['Type'].value_counts()))+1))
    dcolorsc = discrete_colorscale(x, colors[0:len(list(df_annot['Type'].value_counts()))])

    heatmap = go.Heatmap(z=z, colorscale = dcolorsc,
                     colorbar = dict(thickness=10,
                                     tickvals=[0.2, 1, 1.7, 2.2],
                                     ticktext=['a', 'b', 'c' ,'d']), x = ['Type'], y = list(df.index)
                    )
    fig1 = px.imshow(df, color_continuous_scale='RdBu_r')
    fig2 = go.Figure(data=[heatmap])


    fig = make_subplots(
        rows=1, cols=2,
        horizontal_spacing=0.05,
        column_widths=[0.9, 0.1], shared_yaxes=True
    )

    fig.add_trace(fig1.data[0], 1, 1)
    fig.add_trace(fig2.data[0], 1, 2)


    fig.add_annotation(text='CpG island                CpG shore                CpG shelf                CpG inter CGI',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.3,
                        y=-0.13,
                        borderwidth=1)

    fig.add_annotation(text='',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.28,
                        y=-0.126,
                        bgcolor=colors[0],
                        borderwidth=7)
    fig.add_annotation(text='',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.41,
                        y=-0.126,
                        bgcolor=colors[1],
                        borderwidth=7)
    fig.add_annotation(text='',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.525,
                        y=-0.126,
                        bgcolor=colors[2],
                        borderwidth=7)
    fig.add_annotation(text='',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.64,
                        y=-0.126,
                        bgcolor=colors[3],
                        borderwidth=7)
fig_all = fig
fig_all.update_layout(paper_bgcolor="#1c1f27", template =  "plotly_dark")

#---------------------------Norm all----------------------

df = pd.read_csv(OncoprintNorm)

df = df.set_index('ID')
df = df.drop(['Type', 'Unnamed: 0'], axis=1)

fig_norm_all = px.imshow(df.T, aspect="auto", template= "plotly_dark")
fig_norm_all.update_layout(paper_bgcolor="#1c1f27")


#------------------------PCA----------------------

finalDf = pd.read_csv(PCA_data)
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

fig_pca = px.scatter(finalDf, x='PCA1', y='PCA2', template= "plotly_dark",
        color=finalDf['Type'], opacity=0.7,
        labels={'0': 'PC 1', '1': 'PC 2'})
fig_pca.update_layout(paper_bgcolor="#1c1f27")

#-----------------------------HTML-------------------------
html_string_head = '''
<html>
    <head>
        <style>
        body{ margin:0; background:#2e3444; color:white; }
         .active {
  background-color: #04AA6D;
  color: white;
}

 /* Vertical bar */
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  width: 13%;
  background-color: #1c1f27;
  height: 100%; /* Full height */
  position: fixed; /* Make it stick, even on scroll */
  overflow: auto; /* Enable scrolling if the sidenav has too much content */
}

li a {
  display: block;
  color: #ffffff;
  padding: 8px 16px;
  text-decoration: none;
}

/* Change the link color on hover */
li a:hover {
  background-color: #04aa6d;
  color: white;
}

.main{
margin-left: 15%;
padding: 1px 16px;
height 500px;

}
        
        </style>
    </head>
    <body>  
    
<ul class="vertical">
    <li><a style="background-color:#009DCF; color:white"> AutoMethyc </a></li>
    <li><a href="#Home"> Home </a></li>
    <li><a href="#Samples" > Stastics </a></li>
    <li><a href="#All">Heatmap all</a></li>
    <li><a href="#Mean">Heatmap mean</a></li>
    <li><a href="#all_norm">All sites normalized</a></li>
    <li><a href="#Mean_norm">Mean per gene normalized</a></li>
    <li><a href="#pca">PCA</a></li>
    <li><a href="#about"> About</a></li>
</ul> 
 
 <div class="main">
           <h1 id="Home"> AutoMethyc </h1>
           <h2> Version with normal samples </h2>
        AutoMethyc is a pipeline automated which aims for simplicity and practcality in methylation analysis.
        <h2 id="Samples"> Statistics </h2>
        The statistics of the samples consist of classifying the coverage (CVR) of the samples given the bedGraph and the average coverage of the samples, in addition to plotting the count of regions present in the bedGraph (In_loc) and those not present (Not_loc). In addition to evaluating the filter count (FTR) to visualize the number of filtered regions.
 </div">  

    </body>
</html>'''

html_string_spec1 = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0; background:#2e3444; color:white; }</style>
    </head>
    <body>
        <h2 id="All"> Heatmap all sites </h2>
        Heatmap of the percentage of methylation present at each site present in the bedGraph per sample
    </body>
</html>'''




html_string_init_norm = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0; background:#2e3444; color:white; }

         .fraction {
         display: inline-block;
         vertical-align: middle; 
         margin: 0 0.2em 0.4ex;
         text-align: center;
         }
         .fraction > span {
         display: block;
         padding-top: 0.15em;
         }
         .fraction span.fdn {border-top: thin solid white;}
         .fraction span.bar {display: none;}
        </style>
    </head>
    <body>
        <h1> Normalization </h1>
        Normalization was performed considering the mean and standard deviation of the controls, applying to each value:
        
        <div class style="text-align: center;">
        <i>N<sub>i</sub></i> = 
        <div class="fraction">
        <span class="fup"> x<sub>i</sub> - μ </span>
        <span class="bar">/</span>
        <span class="fdn"> σ </span>
        </div>
        </div>

        <h2 id="all_norm"> Heatmap all sites normalized </h2>
        Heatmap with all sites normalized based on the mean and standard deviation of the controls.
    </body>
</html>'''

html_string__mean_norm = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0; background:#2e3444; color:white; }</style>
    </head>
    <body>
        <h2 id="Mean_norm"> Heatmap mean per gene normalized </h2>
        Heatmap with the mean of each normalized site belonging to each gene
    </body>
</html>'''

html_string__PCA = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0; background:#2e3444; color:white; }</style>
    </head>
    <body>
        <h2 id="pca"> PCA </h2>
        Principal component analysis (PCA) applied to each site of the normals and samples. Each point represents a normalized site according to the corresponding group (normal or sample). To view which region is view the file "PCA_vectors.csv" in [Output]/CSV
    </body>
</html>'''



html_string_fooder = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0; background:#2e3444; color:white; }</style>
    </head>
    <body>
        <h3 id="about"> Repository  </h4>
        This program is avalible in <td><a href="https://github.com/FerAmbriz/AutoMethyc"> AutoMethyc </a></td>
        
    </body>
</html>'''


# 3. Write the html string as an HTML file
with open(Output + '/AutoMethyc_Report.html', 'w') as f:
    f.write(html_string_head)
    f.write(html_string_spec1)
    f.write(fig_all.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_init_norm)
    f.write(fig_norm_all.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string__PCA)
    f.write(fig_pca.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_fooder)
