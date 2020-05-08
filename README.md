This program was written in python and generates the top-100 wordcloud from pdf files. Many aspects can be customized, including the number of top words, colours, masks and stopwords.

# Installation 

Tested in python-2.7.18.amd64 and python-3.8.2-amd64, IDE Pycharm 2019.2.6.

After clonging the project, you may need to tnstall the folowing libraries:

* matplotlib.pyplot => To plot the wordcloud
* nltk => To sanitize the text that will be plotted. 

It will enable to detect the tokens by lexical type and omit massively the lexical categories that we do not want to plot. 
e.g: **Determiners & articles** *(the, a ...)*, **Numericals** *(1, two, third ...)*,  **Adverbs** *(really, already, still, early, now)*, **Conjunction** *(and, or, but, if, while, although...)*. 

**<ins>obs</ins>**: nltk sometimes requires installling from the command line e.g. pip install nltk==2.0.5.

* wordcloud  => To prepare the enablers and customize the wordcloud

if right-clic does not work, launch it from the system cmd > pip install wordcloud.

**<ins>obs</ins>**: Microsoft Visual C++ 14.0 is required. Follow further instruction on https://www.scivision.dev/python-windows-visual-c-14-required/)

* PyPDF2 => To extract all the text from the pdf file into a stream
* numpy => Optional use, to create a shape (mask) for the wordcloud
* PIL => to create a shape (mask) for the wordcloud
* collections => Optional use in a check functionality that will print the top-words list
* langdetect => Optional use for future applicatins to enable different processing based on the detected language

# Configuration
Specify both the location path and name of the document to be processed.
* repo_path = 'C:/..../'
* input_file = 'xxx.pdf'

The pdf files generated from Latex may present some troubles for the pages created with the insertion of other pdf documents.

# Tested case
## Input document
repo_path = 'C:/Users/../Desktop/'
input_file = 'EPRS_BRI(2020)646172_EN.pdf' # example document available on https://www.europarl.europa.eu/RegData/etudes/BRIE/2020/646172/EPRS_BRI(2020)646172_EN.pdf

## Output wordcloud
![wordcloud](https://user-images.githubusercontent.com/28622444/81429128-43904f00-9155-11ea-94e6-e9b58ef072ca.png)

