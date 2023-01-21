#!/usr/bin/env python3
#import os
#os.environ['OPENBLAS_NUM_THREADS'] = '1'


def html_css ():
    html = '''
<html>
    <head>
        <style>
            body{ margin:0; background:white; color:black; font-family: Arial;}
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

            .column {
                float: left;
                }
            .center {
                margin: auto;
                width: 15%;
                }
            .c{
              width: 50%;
              display: block;
              margin: auto;
            }
        </style>
    </head>
    '''
    return html

def html_navbar_complete ():
    html = '''
    <body>
        <ul class="vertical">
            <li><a href="#Home" style="background-color:#009DCF; color:white"> AutoMethyc </a></li>
            <li><a href="#Base"> Base quality </a></li>
            <li><a href="#Depth"> Depth </a></li>
            <li><a href="#Samples" > Coverage </a></li>
            <li><a href="#All"> Heatmap all</a></li>
            <li><a href="#Mean"> Heatmap mean</a></li>
            <li><a href="#all_norm"> All sites normalized</a></li>
            <li><a href="#Mean_norm"> Mean per gene normalized</a></li>
            <li><a href="#pca"> PCA </a></li>
            <li><a href="#about"> About </a></li>
        </ul>
    </body>
    '''
    return html





def html_navbar_sFilt ():
    html = '''
    <body>
        <ul class="vertical">
            <li><a href="#Home" style="background-color:#009DCF; color:white"> AutoMethyc </a></li>
            <li><a href="#Base"> Base quality </a></li>
            <li><a href="#Depth"> Depth </a></li>
            <li><a href="#All"> Heatmap all</a></li>
            <li><a href="#all_norm"> All sites normalized</a></li>
            <li><a href="#pca"> PCA </a></li>
            <li><a href="#about"> About </a></li>
        </ul>
    </body>
    '''
    return html

def html_navbar_sNorm ():
    html = '''
    <body>
        <ul class="vertical">
            <li><a href="#Home" style="background-color:#009DCF; color:white"> AutoMethyc </a></li>
            <li><a href="#Base"> Base quality </a></li>
            <li><a href="#Depth"> Depth </a></li>
            <li><a href="#Samples" > Coverage </a></li>
            <li><a href="#All"> Heatmap all</a></li>
            <li><a href="#Mean"> Heatmap mean</a></li>
            <li><a href="#about"> About </a></li>
        </ul>
    </body>
    '''
    return html

def html_navbar_sNorm_sFilt ():
    html = '''
    <body>
        <ul class="vertical">
            <li><a href="#Home" style="background-color:#009DCF; color:white"> AutoMethyc </a></li>
            <li><a href="#Base"> Base quality </a></li>
            <li><a href="#Depth"> Depth </a></li>
            <li><a href="#All"> Heatmap all</a></li>
            <li><a href="#about"> About </a></li>
        </ul>
    </body>
    '''
    return html

def html_AutoMethyc ():
    html = '''
    <div class="main">
        <h1 id="Home"> AutoMethyc </h1>
            <h2> Version with normal samples </h2>
                AutoMethyc is a pipeline automated which aims for simplicity and practcality in methylation analysis.
    </div">
    '''
    return html

def html_base ():
    html = '''
    <body>
        <h2 id="Base" > Base quality </h2>
        Merge of fastqc
    </body>
    '''
    return html

def html_depth ():
    html = '''
    <body>
        <h2 id="Depth" > Depth </h2>
            Count of sites filtered and unfiltered variables by depth
    </body>
    '''
    return html

def html_coverage ():
    html = '''
    <body>
        <h2 id="Samples" > Coverage </h2>
            The statistics of the samples consist of classifying the coverage (CVR) of the samples given the bedGraph and the average coverage of the samples, in addition to plotting the count of regions present in the bedGraph (In_loc) and those not present (Not_loc). In addition to evaluating the filter count (FTR) to visualize the number of filtered regions.
    </body>
    '''
    return html

def html_all():
    html = '''
    <body>
        <h2 id="All"> Heatmap all sites </h2>
            Heatmap of the percentage of methylation present at each site present in the bedGraph per sample
         <div class="row">
            <div class="c">
                <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/IslaCpG.jpeg?raw=true" width="650" height="150">
            </div>
        </div>
    </body>
    '''
    return html

def html_mean():
    html = '''
    <body>
        <h2 id="Mean"> Heatmap mean per Gene </h2>
            Heatmap of the average percentage of methylation present in each site corresponding to its corresponding gene.
    </body>
    '''
    return html

def html_norm():
    html = '''
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
    '''
    return html

def html_mean_norm():
    html = '''
    <body>
        <h2 id="Mean_norm"> Heatmap mean per gene normalized </h2>
            Heatmap with the mean of each normalized site belonging to each gene
    </body>
    '''
    return html

def html_pca():
    html = '''
    <body>
        <h2 id="pca"> PCA </h2>
            Principal component analysis (PCA) applied to each site of the normals and samples. Each point represents a normalized site according to the corresponding group (normal or sample). To view which region is view the file "PCA_vectors.csv" in [Output]/CSV
    </body>
    '''
    return html

def html_fooder():
    html= '''
    <body>
        <h3 id="about"> Repository  </h4>
            This program is avalible in <td><a href="https://github.com/FerAmbriz/AutoMethyc"> AutoMethyc </a></td>
         <div class="row">
            <div class="center">
                <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/Escudo-UNAM.png?raw=true" width="65" height="75">
                <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/LN_FESI.jpg?raw=true" width="75" height="80">
            </div>
        </div>
    </body>
</html>
    '''
    return html
