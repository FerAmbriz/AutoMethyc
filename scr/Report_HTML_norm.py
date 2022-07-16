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


intput_folder = sys.argv[1]
Output = sys.argv[2]

Oncoprint_All = intput_folder+'/CSV/OncoprintRellenado.csv'
Oncoprint_mean = intput_folder+'/CSV/OncoprintPromedio.csv'
Count = intput_folder+'/CSV/Count.csv'
NotLoc = intput_folder+'/CSV/NotLoc.csv'
OncoprintNorm = intput_folder+'/CSV/OncoprintNorm.csv'
OncoprintMeanNorm = intput_folder+'/CSV/OncoprintMeanNorm.csv'
PCA_data = intput_folder+'/CSV/PCA_vectors.csv'


print('#-------------------Plotting-------------------------')

#------------------------All_sites ------------------
df = pd.read_csv(Oncoprint_All)
df = df.drop(['Unnamed: 1'], axis=1)
df = df.drop(df.index[[0,1]])
df = df.rename(columns = {'Sample':'Start'})
df = df.set_index('Start')

fig_all = px.imshow(df, aspect="auto", template= "plotly_dark")
fig_all.update_layout(paper_bgcolor="#1c1f27")

#--------------------------Mean-----------------------

df = pd.read_csv(Oncoprint_mean)
df = df.set_index('Gen')
df = df.drop(['Sample'], axis=1)
df = df.drop(df.index[[0]])

fig_mean= px.imshow(df, aspect="auto", template= "plotly_dark")
fig_mean.update_layout(paper_bgcolor="#1c1f27")
#-------------------------Count-----------------------

df = pd.read_csv(Count)
up = max(df.Sample)
rng = up-7

for i in range(rng):
    df = df.replace({i : '<'+str(rng)})

values = df['Sample'].value_counts().to_list()
labels= df['Sample'].value_counts()
labels = labels.index.values

# donut pie chart 2 columns
fig_samples = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])


# Cobertura
fig_samples.add_trace(go.Pie(labels=labels, values=values, hole=.3, name="Coverage"),
              1, 1)
# Profundiad
fig_samples.add_trace(go.Pie(labels=['<20k', '20k-25k', '>25k'], values=[30,200,70], hole=.3, name="Profundiad"),
              1, 2)

fig_samples.update_layout(
    title_text="Characteristics of the samples", template= "plotly_dark",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='CVR', x=0.20, y=0.5, font_size=20, showarrow=False),
                 dict(text='DPT', x=0.80, y=0.5, font_size=20, showarrow=False)])

fig_samples.update_layout(paper_bgcolor="#1c1f27")

df.columns = ['ID' , 'Count']
df['Status'] = ['In_Loc'] * len(df)


df2 = pd.read_csv(NotLoc)
df2 = pd.DataFrame(df2['ID'].value_counts()).reset_index()
df2.columns = ['ID' , 'Count']
df2['Status'] = ['NotLoc'] * len(df2)

df = pd.concat([df, df2])

fig_chr = px.bar(df, x="ID", y="Count", color="Status", title="Coverage Status", template= "plotly_dark")

fig_chr.update_layout(paper_bgcolor="#1c1f27")


#---------------------------Norm all----------------------

df = pd.read_csv(OncoprintNorm)
df = df.drop(df.index[[0,1]])
df = df.rename(columns = {'Unnamed: 1':'ID'})

df = df.set_index('ID')
df = df.drop(['Start'], axis=1)
fig_norm_all = px.imshow(df.T, aspect="auto", template= "plotly_dark")
fig_norm_all.update_layout(paper_bgcolor="#1c1f27")


#-------------------------Norm mean-------------------
df = pd.read_csv(OncoprintMeanNorm)
df = df.drop(['Status'], axis=1)
df = df.rename(columns = {'Unnamed: 1':'ID'})
df = df.set_index('ID')

fig_mean_norm= px.imshow(df.T, aspect="auto", template= "plotly_dark")
fig_mean_norm.update_layout(paper_bgcolor="#1c1f27")

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
        This program ...
        <h2 id="Samples"> Characteristics of samples </h2>
        CVR is coverage and DPT is depth
        
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
    </body>
</html>'''


html_string_body = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0; background:#2e3444; color:white; }</style>
    </head>
    <body>
        <h2 id="Mean"> Heatmap mean per Gene </h2>
    </body>
</html>'''


html_string_init_norm = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0; background:#2e3444; color:white; }</style>
    </head>
    <body>
        <h2 id="all_norm"> Heatmap all sites normalized </h2>
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
    f.write(fig_samples.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_chr.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_spec1)
    f.write(fig_all.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_body)
    f.write(fig_mean.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_init_norm)
    f.write(fig_norm_all.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string__mean_norm)
    f.write(fig_mean_norm.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string__PCA)
    f.write(fig_pca.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_fooder)

