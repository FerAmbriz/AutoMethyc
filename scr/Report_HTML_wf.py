#!/usr/bin/env python
# coding: utf-8

# # Rerport HTML

import pandas as pd
import plotly.express as px
from IPython.display import HTML
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots


Oncoprint_All = sys.argv[1]
Count = sys.argv[2]
Output = sys.argv[3]

print('#-------------------Plotting-------------------------')

#------------------------All_sites ------------------
df = pd.read_csv(Oncoprint_All)
df['Unnamed: 1'] = df['Unnamed: 1'].fillna('Start')
df.columns = df.iloc[0]
df = df.drop(df.index[[0,1,2]])
df = df.drop(['Sample'], axis=1)
df = df.set_index('Start')

fig_all = px.imshow(df, aspect="auto", template= "plotly_dark")
fig_all.update_layout(paper_bgcolor="#1c1f27")

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
    <li><a href="#about">About</a></li>
</ul> 
 
 <div class="main">
           <h1 id="Home"> AutoMethyc </h1>
           <h2> Version without normal samples </h2>
        AutoMethyc is a pipeline automated which aims for simplicity and practicality in methylation analysis.
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
    f.write(html_string_fooder)
