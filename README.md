This program was written in python and generates a wordcloud from pdf files.

# Installation (Tested in python-3.8.2-amd64)
Install the folowing libraries
* matplotlib.pyplot (pip install xx) to plot the wordcloud
* nltk (e.g. pip install nltk==2.0.5) To sanitize the text to be plotted i.e, will enable to detect the tokens by lexical type, and omit massively the categories that we dont want to plot. e.g: determiners and articles (the, a ...), numericals (1, two, third ...),  Adverbs (really, already, still, early, now), conjunction (and, or, but, if, while, although...)
* numpy (pip install xx
* wordcloud (if right-clic does not work, launch in the system cmd > pip install wordcloud.

Microsoft Visual C++ 14.0 is required. https://www.scivision.dev/python-windows-visual-c-14-required/)
* PyPDF2 (pip install xx
* PIL (pip install xx
* collections (pip install xx 
* langdetect (pip install xx). For future applicatins, to enable different processing based on the detected language

# Configuration
Udpated the directory where the source file is located and the name of the file to be processed.
* repo_path = 'C:/..../'
* input_file = 'xxx.pdf'

The pdf files generated from Latex may present some troubles for the pages created with the insertion of oter pdf documentos.

# Exemple
## input
repo_path = 'C:/Users/../Desktop/'
input_file = 'EPRS_BRI(2020)646172_EN.pdf' # document available on https://www.europarl.europa.eu/RegData/etudes/BRIE/2020/646172/EPRS_BRI(2020)646172_EN.pdf

## output


