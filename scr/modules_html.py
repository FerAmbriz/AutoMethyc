#!/usr/bin/env python3
#import os
#os.environ['OPENBLAS_NUM_THREADS'] = '1'
import datetime

def html_css ():
    html = '''
<html>
    <head>
        <style>
            body{ margin:0; background:white; color:black; font-family: Arial;}
            .active {
                background-color:#45B39D;
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
    border-radius: 10px;
}
li a span {
    display: block;
    padding: 16px 0px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}

/* Change the link color on hover */
li a span:hover {
    background-color: rgba(255, 255, 255, 0.5);
    color: black;
    border-radius: 10px;
}

li a span2 {
    display: block;
    padding: 10px 10px;
    font-size: 17px;
}

/* Change the link color on hover */
li a span2:hover {
    background-color: rgba(255, 255, 255, 0.5);
    color: black;
    border-radius: 10px;
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
            .vertical {display: flex;
    flex-direction: column;
    justify-content: space-between; /* Distribuye el espacio de manera uniforme entre los elementos */
    height: 100%; /* Ocupa todo el espacio vertical disponible */
}

.vertical li:last-child {
    margin-top: auto; /* Empuja el último elemento hacia abajo */
}

        </style>
        <link rel="icon" href="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/AutoMethyc.png?raw=true">
    </head>
    '''
    return html

def html_navbar_complete ():
    html = '''
    <ul class="vertical">
        <li><a href="#Home" color:white><span> AutoMethyc </span></a></li>
        <li><a href="#Base"><span2> Base quality </span2></a></li>
        <li><a href="#Depth"><span2> Depth </span2></a></li>
        <li><a href="#Samples"><span2> Coverage </span2></a></li>
        <li><a href="#cgi"><span2> CGI mapping </span2></a></li>
        <li><a href="#All"><span2> Methylation percentage </span2></a></li>
        <li><a href="#Mean"><span2> Mean methylation </span2></a></li>
        <li><a href="#all_norm"><span2> Normalized methylation </span2></a></li>
        <li><a href="#Mean_norm"><span2> Mean normalized </span2></a></li>
        <li><a href="#pca"><span2> PCA </span2></a></li>
        <li><a href="#snv"><span2> Variant calling </span2></a><li>
        <li><a href="#about" style="background-color:#45B39D; border-radius: 0"><span2 style="background-color:#1c1f27; border-radius:10px" onmouseover="this.style.backgroundColor='rgba(255, 255, 255, 0.5)'; this.style.color='black';" onmouseout="this.style.backgroundColor='#1c1f27'; this.style.color='white';"> About </span2></a></li>
    </ul>

    <script>
        window.addEventListener('scroll', function() {
            var items = document.querySelectorAll('.vertical li a');
            var activeItem;
            items.forEach(function(item) {
                var section = document.querySelector(item.getAttribute('href'));
                var sectionTop = section.offsetTop;
                var sectionBottom = sectionTop + section.offsetHeight;
                if (window.scrollY >= sectionTop && window.scrollY < sectionBottom) {
                    item.classList.add('active');
                    activeItem = item;
                 }
            });
            items.forEach(function(item) {
                if (item !== activeItem) {
                    item.classList.remove('active');
                 }
            });
        });
    </script>
    '''
    return html


def html_navbar_sNorm ():
    html = '''
    <ul class="vertical">
        <li><a href="#Home" style="background-color:#009DCF; color:white"> AutoMethyc </a></li>
        <li><a href="#Base"> Base quality </a></li>
        <li><a href="#Depth"> Depth </a></li>
        <li><a href="#Samples" > Coverage </a></li>
        <li><a href="#cgi" > CGI mapping </a></li>
        <li><a href="#All"> Methylation percentage </a></li>
        <li><a href="#Mean"> Mean methylation </a></li>
        <li><a href="#snv"> Variant calling </a><li>
        <li><a href="#about"> About </a></li>
    </ul>
    <script>
        window.addEventListener('scroll', function() {
            var items = document.querySelectorAll('.vertical li a');
            var activeItem;
            items.forEach(function(item) {
                var section = document.querySelector(item.getAttribute('href'));
                var sectionTop = section.offsetTop;
                var sectionBottom = sectionTop + section.offsetHeight;
                if (window.scrollY >= sectionTop && window.scrollY < sectionBottom) {
                    item.classList.add('active');
                    activeItem = item;
                 }
            });
            items.forEach(function(item) {
                if (item !== activeItem) {
                    item.classList.remove('active');
                 }
            });
        });
    </script>
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
    <div id="Samples">
        <h2 style="margin-bottom: 5px;"> Coverage </h2>
        <hr>
        Count of sites present in the regions of interest provided by BED file
    '''
    return html

def html_cgi():
    html = '''
    </div>
    <div id="cgi">
        <h2 style="margin-bottom: 5px;"> CGI mapping </h2>
        <hr>
        Mapped regions and their classification considering the nearest CpG island
         <div class="row">
            <div class="c">
                <img src="https://github.com/FerAmbriz/AutoMethyc/blob/master/img/IslaCpG.jpeg?raw=true" width="650" height="150">
            </div>
            </ol>
        </div>
    '''
    return html
def html_all():
    html = '''
    </div>
    <div id="All">
        <h2 id="All"; style="margin-bottom: 5px;"> Methylation percentage </h2>
        <hr>
        Methylation percentage considering the cytosines methylated and unmethylated for each site
    '''
    return html

def html_mean_gene():
    html = '''
    </div>
    <div id="Mean">
        <h2 style="margin-bottom: 5px;"> Mean methylation </h2>
        <hr>
           Average percentage of methylation present in each gene of the sequenced region.
    '''
    return html

def html_norm():
    html = '''
    </div>
    <div id="all_norm">
        <h1 id ="all_norm"; style="margin-bottom: 5px;"> Normalization </h1>
        <hr>
            Normalization was performed considering the mean and standard deviation of the controls
    '''
    return html

def html_mean_norm():
    html = '''
    </div>
    <div id="Mean_norm">
        <h2 style="margin-bottom: 5px;"> Mean normalized </h2>
        <hr>
            Mean normalization of each normalized site belonging to each gene
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
