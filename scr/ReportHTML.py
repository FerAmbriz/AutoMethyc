import pandas as pd
import plotly.express as px
from IPython.display import HTML
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots


Oncoprint_All = sys.argv[1]
Oncoprint_mean = sys.argv[2]
Count = sys.argv[3]
NotLoc = sys.argv[4]
Output = sys.argv[5]

#--------------------All_sites---------------------
All = pd.read_csv(Oncoprint_All)
All = All.drop(['Gen'], axis =1)
All  = All.set_index('Start')

fig_all = px.imshow(All)

#---------------------Mean------------------------
mean = pd.read_csv(Oncoprint_mean)
mean = mean.drop(['Unnamed: 0', 'Gen'], axis=1)
fig_mean= px.imshow(mean)

#---------------------Count----------------------
count = pd.read_csv(Count) 
values = count['Sample'].value_counts().to_list()
labels= count['Sample'].value_counts()
labels = labels.index.values

fig_samples = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# Cobertura
fig_samples.add_trace(go.Pie(labels=labels, values=values, hole=.3, name="Coverage"),1, 1)

# Profundiad
fig_samples.add_trace(go.Pie(labels=['<20k', '20k-25k', '>25k'], values=[30,200,70], hole=.3, name="Profundiad"), 1, 2)

fig_samples.update_layout(
            title_text="Characteristics of the samples",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='CVR', x=0.20, y=0.5, font_size=20, showarrow=False),
                dict(text='DPT', x=0.80, y=0.5, font_size=20, showarrow=False)]
        )

count.columns = ['ID' , 'Count']
count['Status'] = ['In_Loc'] * len(count)


notloc = pd.read_csv(NotLoc)
notloc = pd.DataFrame(notloc['ID'].value_counts()).reset_index()
notloc.columns = ['ID' , 'Count']
notloc['Status'] = ['NotLoc'] * len(notloc)

merge = pd.concat([count, notloc])

fig_chr = px.bar(merge, x="ID", y="Count", color="Status", title="Coverage Status")


#--------------------------Report HTML--------------------

html_string_head = '''
<html>
    <head>
        <style>
         
         body{margin:0; background:whitesmoke;}

          /* ul {*/
            /*position: fixed;*/
            /*top: 0;*/
            /*width: 100%;}*/

         .active {
         background-color: #04AA6D;
         color: white;
         }

         li{
          float: left;
         }

         li a {
         display: block;
         color: white;
         padding: 8px 16px;
         background-color: #2d465e;
         text-decoration: none;
         }

         /* Change the link color on hover */
         li a:hover {
         background-color: #04aa6d;
         color: white;
         }

         .head{
         margin-left: 5%;
         padding: 1px 16px;
         padding-top: 0%;
         height 500px;
         }

         .main{
         margin-left: 5%;
         padding: 1px 16px;
         height 500px;
         }
         
         ul.horizontal{
         list-style-type: none;
         margin: 0;
         padding: 0;
         overflow: hidden;
         background-color: #2d465e;
         }

         </style>
    <ul class="horizontal">
        <li><a style="background-color:#009DCF; color:white"> Report </a></li>
        <li><a href="#Home"> Home </a></li>
        <li><a href="#Samples" > Stastics </a></li>
        <li><a href="#All">Heatmap all</a></li>
        <li><a href="#Mean">Heatmap mean</a></li>
        <li class="rightli" style= "float:right"><a href="https://github.com/FerAmbriz/AutoMethyc">GitHub</a></li>
    </ul>

    </head>
    
    <div class="head">
        <h1 id="Home"> AutoMethyc </h1>
        This program ...
        <h2 id="Samples"> Characteristics of samples </h2>
        CVR is coverage and DPT is depth


     </div>
</html>
'''

html_string_spec1 = '''
<html>
    <head>
        <style>
        body{padding:0; background:whitesmoke;}
       </style>
    </head>
    <body>
    <div class="main">
           <h2 id="All"> Heatmap all sites </h2>
    </div>
    </body>
</html>
'''

html_string_body = '''
<html>
    <head>
        <style>body{ margin:0; background:whitesmoke;  }</style>
    </head>
    <body>
    <div class="main">
        <h2 id="Mean"> Heatmap mean per Gene </h2>
    </div>
    </body>
</html>
'''
html_string_fooder = '''
<html>
    <head>
        <style>body{ margin:0; background:whitesmoke;  }</style>
    </head>
    <body>
    <div class="main"> 
        <h3> Repository  </h4>
        This program is avalible in github
    </div>
    </body>
</html>
'''

# 3. Write the html string as an HTML file
with open(Output + '/Report.html', 'w') as f:
    f.write(html_string_head)
    f.write(fig_samples.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_chr.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_spec1)
    f.write(fig_all.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_body)
    f.write(fig_mean.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(html_string_fooder)

