#!/usr/bin/env python3
#import os
#os.environ['OPENBLAS_NUM_THREADS'] = '1'
import datetime

def html_css ():
    html = '''
<html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/FerAmbriz/AutoMethyc/report/style.css">
        <link rel="icon" href="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/AutoMethyc.png?raw=true">
    </head>
    '''
    return html

def html_navbar_complete ():
    html = '''
    <ul class="vertical">
        <li><a href="#Home"><span> AutoMethyc </span></a></li>
        <li><a href="#Base"><span2> Base quality </span2></a></li>
        <li><a href="#Depth"><span2> Depth </span2></a></li>
        <li><a href="#Coverage"><span2> Coverage </span2></a></li>
        <li><a href="#CGI"><span2> CGI mapping </span2></a></li>
        <li>
        <a href="#Percentage"><span2> Methylation percentage </span2></a>
        <ul>
            <li style="padding-left: 30px;"><a href="#Detailed"><span3> Detailed </span3></a></li>
            <li style="padding-left: 30px;"><a href="#MeanSite"><span3> Mean by site </span3></a></li>
            <li style="padding-left: 30px;"><a href="#MeanGene"><span3> Mean by gene </span3></a></li>
            <li style="padding-left: 30px;"><a href="#Global"><span3> Global </span3></a></li>
        </ul>
        </li>
        <li>
        <a href="#Z-score"><span2> Normalized methylation </span2></a>
        <ul>
            <li style="padding-left: 30px;"><a href="#NormDetailed"><span3> Detailed normalization </span3></a></li>
            <li style="padding-left: 30px;"><a href="#NormManhattan"><span3> Normalization by sample and site </span3></a></li>
            <li style="padding-left: 30px;"><a href="#MeanSiteNorm"><span3>  Mean by site normalized </span3></a></li>
            <li style="padding-left: 30px;"><a href="#MeanGeneNorm"><span3> Mean by gene normalized </span3></a></li>
            <li style="padding-left: 30px;"><a href="#Volcano"><span3> Differential methylation </span3></a></li>
        </ul>
        </li>
        <li><a href="#pca"><span2> PCA </span2></a></li>
        <li><a href="#snv"><span2> Variant calling </span2></a><li>
        <li><a href="#about" style="background-color:#45B39D; border-radius: 0"><span2 style="background-color:#1c1f27; border-radius:10px" onmouseover="this.style.backgroundColor='rgba(255, 255, 255, 0.5)'; this.style.color='black';" onmouseout="this.style.backgroundColor='#1c1f27'; this.style.color='white';"> About </span2></a></li>
    </ul>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/FerAmbriz/AutoMethyc/report/animations.js"></script>
     '''
    return html

def html_navbar_sNorm ():
    html = '''
    <ul class="vertical">
        <li><a href="#Home"><span> AutoMethyc </span></a></li>
        <li><a href="#Base"><span2> Base quality </span2></a></li>
        <li><a href="#Depth"><span2> Depth </span2></a></li>
        <li><a href="#Coverage"><span2> Coverage </span2></a></li>
        <li><a href="#CGI"><span2> CGI mapping </span2></a></li>
        <li>
        <a href="#Percentage"><span2> Methylation percentage </span2></a>
        <ul>
            <li style="padding-left: 30px;"><a href="#Detailed"><span3> Detailed </span3></a></li>
            <li style="padding-left: 30px;"><a href="#MeanSite"><span3> Mean by site </span3></a></li>
            <li style="padding-left: 30px;"><a href="#MeanGene"><span3> Mean by gene </span3></a></li>
        </ul>
        </li>
        <li><a href="#snv"><span2> Variant calling </span2></a><li>
        <li><a href="#about" style="background-color:#45B39D; border-radius: 0"><span2 style="background-color:#1c1f27; border-radius:10px" onmouseover="this.style.backgroundColor='rgba(255, 255, 255, 0.5)'; this.style.color='black';" onmouseout="this.style.backgroundColor='#1c1f27'; this.style.color='white';"> About </span2></a></li>
    </ul>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/FerAmbriz/AutoMethyc/report/animations.js"></script>
     '''
    return html


def html_AutoMethyc (command):
    html = f'''
    <div class="main">
    <div id="Home">
        <h1 style="margin-bottom: 5px;"> AutoMethyc </h1>
        <hr style="margin-top: 0;">
        <div class="center">
            <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/AutoMethyc.png?raw=true" width="110" height="100">
        </div>
        AutoMethyc is an integrative pipeline to methylation analysis from raw sequences obtained from massive parallel bisulfite sequencing.
    <h2 style="margin-bottom: 5px;"> Parameters </h2>
    <hr>
        Command used and global parameters:
    <p style="color:white; background:#2E3440; padding: 15px; border-radius: 15px;"><code>{command}</code></p>
    '''
    return html

def html_base ():
    html = '''
    </div>
    <div id="Base">
        <h2 style="margin-bottom: 5px;"> Base quality </h2>
        <hr style="margin-top: 0;">
        Logarithmic ratio of Phred Q quality scores to base call error probabilities.
    '''
    return html

def html_depth ():
    html = '''
    </div>
    <div id="Depth">
        <h2 style="margin-bottom: 5px;"> Depth </h2>
        <hr>
        Count of filtered (off-targets) and unfiltered (on-targets) sites according to the depth threshold established for greater certainty in the analysis.
    '''
    return html

def html_coverage ():
    html = '''
    </div>
    <div id="Coverage">
        <h2 style="margin-bottom: 5px;"> Coverage </h2>
        <hr>
        Count of sites present in the regions of interest provided by BED file
    '''
    return html

def html_cgi():
    html = '''
    </div>
    <div id="CGI">
        <h2 style="margin-bottom: 5px;"> CGI mapping </h2>
        <hr>
        Mapped regions and their classification considering the nearest CpG island
         <div class="row">
            <div class="c">
                <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/IslaCpG.jpeg?raw=true" width="650" height="150">
            </div>
        </div>
    '''
    return html
def html_all():
    html = '''
    </div>
    <div id="Percentage">
        <h2 style="margin-bottom: 5px;"> Methylation percentage </h2>
        <hr>
        Methylation percentage considering the cytosines methylated and unmethylated for each site
    </div>
    <div id="Detailed">
        <h3 style="margin-bottom: 5px;"> Detailed </h3>
        Methylation percentage of each CpG site per patient. The sidebar on the right indicates the site's ranking after mapping. The bottom bar shows whether they are samples or normals.
    '''
    return html

def html_mean_site():
    html = '''
    </div>
    <div id="MeanSite">
        <h3 style="margin-bottom: 5px;"> Mean by site </h3>
        Average per site show the difference of methylation percentage in the different sites.
    '''
    return html


def html_mean_gene():
    html = '''
    </div>
    <div id="MeanGene">
        <h3 style="margin-bottom: 5px;"> Mean by gene </h3>
           Average percentage of methylation present in each gene of the sequenced region.
    '''
    return html

def html_boxplot():
    html = '''
    </div>
    <div id="Global">
        <h3 style="margin-bottom: 5px;"> Global </h3>
           Global distribution of methylation percentage
    '''
    return html

def html_norm():
    html = '''
    </div>
    <div id="Z-score">
        <h2 style="margin-bottom: 5px;"> Normalization </h1>
        <hr>
            Normalization was performed considering the mean and standard deviation of the controls using the Z-score
    </div>
    <div id="NormDetailed">
        <h3 style="margin-bottom: 5px;"> Detailed normalization </h3>
    '''
    return html

def html_norm_manhattan():
    html = '''
    </div>
    <div id="NormManhattan">
        <h3 style="margin-bottom: 5px;"> Normalization by sample and site </h3>
        Z-score by sample and site
        Graphical representation of z-score of each sample by site.
    '''
    return html

def html_mean_site_norm():
    html = '''
    </div>
    <div id="MeanSiteNorm">
        <h3 style="margin-bottom: 5px;">  Mean by site normalized  </h3>
        Mean normalization of each normalized site
    '''
    return html


def html_mean_gene_norm():
    html = '''
    </div>
    <div id="MeanGeneNorm">
        <h3 style="margin-bottom: 5px;">  Mean by gene normalized  </h3>
        Mean normalization of each normalized site belonging to each gene
    '''
    return html

def html_volcano():
    html = '''
    </div>
    <div id="Volcano">
        <h3 style="margin-bottom: 5px;">  Differential methylation  </h3>
        Differential methylation.
    '''
    return html

def html_pca():
    html = '''
    </div>
    <div id="pca">
        <h2 style="margin-bottom: 5px;"> PCA </h2>
        <hr>
            Principal component analysis (PCA) applied to each site of the normals and samples. Each point represents a normalized site according to the corresponding group (normal or sample).
    '''
    return html

def html_snv():
    html = '''
    </div>
    <div id="snv">
        <h2 style="margin-bottom: 5px;"> Variant calling </h2>
        <hr>
        Variant call count
    '''
    return html
date = datetime.datetime.now()
date = date.strftime("%H:%M at %d/%m/%Y.")
def html_fooder():
    html= f'''
    </div>
    <div id=about>
        <h3 style="margin-bottom: 5px;"> About  </h4>
        <hr>
            <p style="color: gray;">
                Analysis produced by <a href="https://github.com/FerAmbriz/AutoMethyc"> AutoMethyc </a> - an integrative pipeline to methylation analysis.
                <br> Data processed at {date}
            </p>
         <div class="row">
            <div class="center">
                <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/Escudo-UNAM.png?raw=true" width="65" height="75">
                <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/LN_FESI.jpg?raw=true" width="75" height="80">
            </div>
        </div>
    </div>
</html>
    '''
    return html
