"""
===============
Generating a square wordcloud from the US constitution using default arguments.
Source: https://stackoverflow.com/questions/28786534/increase-resolution-with-word-cloud-and-remove-empty-border
"""

from os import path
import matplotlib.pyplot as plt
import nltk
import numpy as np
from nltk import word_tokenize
from wordcloud import WordCloud, STOPWORDS
import PyPDF2
from PIL import Image
import collections
import re

repo_path = 'C:/Users/X260/Desktop/'


# Extract all the text from the pdf file into a stream
def extract_all_text(filename):
    page_text = []
    with open(filename, "rb") as file:
        f = PyPDF2.PdfFileReader(file)
        # excluded_begin_pages = 36  # Pages before introduction
        # excluded_end_pages = 29  # From bibliography to the end of the document
        excluded_begin_pages = 0  # Pages before introduction
        excluded_end_pages = 0  # From bibliography to the end of the document
        print '#TotalPages:', f.getNumPages()
        # for i in range(0, f.getNumPages()):
        for i in range(excluded_begin_pages, f.getNumPages() - excluded_end_pages):
            page = f.getPage(i)
            pcontent = page.extractText() + "\n"
            pcontent = " ".join(pcontent.replace(u"\xa0", u" ").strip().split())
            page_text.append(pcontent)
        print '#IncludedPages:', i
    return (page_text)


# function to sanitize the text
# ADJ	adjective	new, good, high, special, big, local
# ADP	adposition	on, of, at, with, by, into, under
# ADV	adverb	really, already, still, early, now
# CONJ	conjunction	and, or, but, if, while, although
# DET	determiner, article	the, a, some, most, every, no, which
# NOUN	noun	year, home, costs, time, Africa
# NUM	numeral	twenty-four, fourth, 1991, 14:24
# PRT	particle	at, on, out, over per, that, up, with
# PRON	pronoun	he, their, her, its, my, I, us
# VERB	verb	is, say, told, given, playing, would
# .	punctuation marks	. , ; !
# X	other	ersatz, esprit, dunno, gr8, univeristy
def transform_nlp(text):
    print 'Received finaltext :', text
    finaltext = ''
    for word in text.split(" "):
        exclusion_list = ['DT', 'IN', 'RB', 'WP', 'JJ', 'CD', 'CC', 'POS', 'NN', 'PRP$', 'WRB', 'WDT']
        token = word_tokenize(word)
        token_and_postag = nltk.pos_tag(token)[0]

        # print token_and_postag
        # exclude adpositions, conjunction, determiners, numerals, particle, pronouns and punctuation
        print "token_and_postag: ", token_and_postag
        # print "length: ", len(token_and_postag[1])
        if token_and_postag[1] != 'DT' and token_and_postag[1] != 'IN' and token_and_postag[1] != 'RB' and \
                token_and_postag[1] != 'WP' and token_and_postag[1] != 'JJ' and token_and_postag[1] != 'CD' and \
                token_and_postag[1] != '.' and token_and_postag[1] != ',' and token_and_postag[1] != ':' and \
                token_and_postag[1] != 'POS' and token_and_postag[1] != '[' and token_and_postag[1] != 'WP' and \
                token_and_postag[1] != 'CC' and token_and_postag[1] != 'PRP$' and token_and_postag[1] != 'LS' and \
                token_and_postag[1] != 'NNP' and token_and_postag[1] != 'TO' and token_and_postag[1] != 'IN' and \
                token_and_postag[1] != 'MD':
            finaltext = finaltext + ' ' + word.upper()

        # if token_and_postag[1] not in exclusion_list or \
        # len(token_and_postag[1]) < 3:

    print 'finaltext filtered:', finaltext
    return finaltext


# function to swap number 0 to 255 in the mask image
def transform_format(val):
    if val == 0:
        return 255
    else:
        return val


# to create a shape (mask) for your wordcloud
image_mask = np.array(Image.open(repo_path + "mask.png"))

# Transform your mask into a new one that will work with the function:
transformed_mask = np.ndarray((image_mask.shape[0], image_mask.shape[1]), np.int32)
for i in range(len(image_mask)):
    transformed_mask[i] = list(map(transform_format, image_mask[i]))

# Extract the sentences in the array and for a unique finaltext
filetext = extract_all_text(
    repo_path + 'Zoom_for_ Higher_Education.pdf')  # Receives an array of sentences
finaltext = ''

for i in range(0, len(filetext)):
    finaltext = finaltext + filetext[i]

transformed_finaltext = transform_nlp(finaltext)  # include only certain words. See filter in function transform_nlp()
# print 'finaltext: ', finaltext
# print 'transformed_finaltext: ', transformed_finaltext
# transform_nlp("what, how, that, which")

# Excluded words
stopwords = STOPWORDS
stopwords.add('Finally')
max_words = 100

# Generate the Wordcloud data set and specifies the size of the image
wordcloud = WordCloud(width=595, height=842, stopwords=stopwords, max_words=max_words,
                      background_color="black", colormap="Blues",
                      # max_font_size=50, min_font_size=1,
                      # mask=transformed_mask, contour_width=2, contour_color='blue'
                      ).generate(transformed_finaltext)

# Verifies the top words
filtered_words = [word for word in transformed_finaltext.split() if word not in stopwords]
counted_words = collections.Counter(filtered_words)
words = []
counts = []
for letter, count in counted_words.most_common(max_words):
    words.append(letter)
    counts.append(count)
print 'Words: ', words
print 'Frequency: ', counts

# # Opens a plot of the generated image, defining the minimum and maximum size of the words, plus the facecolor.
plt.figure(figsize=(20, 10), facecolor='k')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

# plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight') # get the final output in a pdf file
plt.tight_layout(pad=0)

# Display the image
plt.show()
