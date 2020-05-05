"""
===============
Generating a square wordcloud from the US constitution using default arguments.
Source: https://stackoverflow.com/questions/28786534/increase-resolution-with-word-cloud-and-remove-empty-border
"""

import matplotlib.pyplot as plt
import nltk
import numpy as np
from nltk import word_tokenize
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import PyPDF2
from PIL import Image
import collections
from langdetect import detect, detect_langs

# Input file location
repo_path = 'C:/Users/X260/Desktop/'
input_file = 'thesis.pdf'


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
        print '#IncludedPages:', i + 1
    return page_text


# function to sanitize the text
# Universal Part-of-Speech Tagset => https://www.nltk.org/book/ch05.html
    # ADJ	adjective	new, good, high, special, big, local # ADP	adposition	on, of, at, with, by, into, under
    # ADV	adverb	really, already, still, early, now  # CONJ	conjunction	and, or, but, if, while, although
    # DET	determiner, article	the, a, some, most, every, no, which # NOUN	noun	year, home, costs, time, Africa
    # NUM	numeral	twenty-four, fourth, 1991, 14:24 # PRT	particle	at, on, out, over per, that, up, with
    # PRON	pronoun	he, their, her, its, my, I, us # VERB	verb	is, say, told, given, playing, would
    # .	punctuation marks	. , ; ! # X	other	ersatz, esprit, dunno, gr8, univeristy
def nlp_filter(text):
    lang = detect(text)
    langs = detect_langs(text)
    finaltext = ''
    for word in text.split(" "):
        exclusion_list = ['DT', 'IN', 'RB', 'WP', 'JJ', 'CD', '.', ',', ':', 'POS', '[', 'WP', 'CC', 'PRP$', 'LS',
                          'NNP', 'TO', 'IN', 'MD']
        token = word_tokenize(word)
        token_and_postag = nltk.pos_tag(token)[0]

        # print token_and_postag
        # exclude adpositions, conjunction, determiners, numerals, particle, pronouns and punctuation
        print "token_and_postag: ", token_and_postag
        # print "length: ", )
        # if token_and_postag[1] in exclusion_list: # Not working with the list
        if token_and_postag[1] != '.' and token_and_postag[1] != ',' and token_and_postag[1] != ':' and \
                token_and_postag[1] != '[' and token_and_postag[1] != ']' and token_and_postag[1] != '&' and \
                token_and_postag[1] != 'CC' and token_and_postag[1] != 'CD' and token_and_postag[1] != 'DT' and \
                token_and_postag[1] != 'IN' and token_and_postag[1] != 'LS' and \
                token_and_postag[1] != 'MD' and token_and_postag[1] != 'POS' and \
                token_and_postag[1] != 'PRP$' and token_and_postag[1] != 'TO' and \
                token_and_postag[1] != 'WP' and len(token_and_postag[1]) < 3:
            print 'len(token_and_postag[1])', len(token_and_postag[1])
            finaltext = finaltext + ' ' + word.upper()

        # if token_and_postag[1] not in exclusion_list or \
        # len(token_and_postag[1]) < 3:

    # print 'Received finaltext :', text
    # print 'finaltext filtered:', finaltext
    print 'Languages probability:', langs
    print 'Selected language:', lang
    return finaltext


# function to swap number 0 to 255 in the mask image
def mask_transform_format(val):
    if val == 0:
        return 255
    else:
        return val


# to create a shape (mask) for your wordcloud
image_mask = np.array(Image.open(repo_path + "mask.png"))

# Transform your mask into a new one that will work with the function:
transformed_mask = np.ndarray((image_mask.shape[0], image_mask.shape[1]), np.int32)
for i in range(len(image_mask)):
    transformed_mask[i] = list(map(mask_transform_format, image_mask[i]))

# Extract the sentences in the array and for a unique finaltext
text_stream_array = extract_all_text(repo_path + input_file)  # Receives an array of sentences fron the input_file.pdf

# Transfortm the array stream into a stream of string
text_stream_string = ''
for i in range(0, len(text_stream_array)):
    text_stream_string = text_stream_string + text_stream_array[i]

# include only certain words. See filter in function transform_nlp()
final_text = nlp_filter(text_stream_string)
# nlp_filter("what, how, that, which")

# Excluded words
stopwords = STOPWORDS
stopwords.add('Finally')
max_words = 1000

# Generate the Wordcloud data set and specifies the size of the image
wordcloud = WordCloud(stopwords=stopwords, width=545, height=792, background_color="white",
                      max_words=max_words,
                      # colormap="Blues",
                      max_font_size=50, min_font_size=5,
                      # mask=image_mask
                      # mask=transformed_mask, contour_width=2, contour_color='blue'
                      ).generate(final_text)

# Verifies the top words
filtered_words = [word for word in final_text.split() if word not in stopwords]
counted_words = collections.Counter(filtered_words)
words = []
counts = []
for letter, count in counted_words.most_common(max_words):
    words.append(letter)
    counts.append(count)
print 'Words: ', words
print 'Frequency: ', counts

# # # Opens a plot of the generated image, defining the minimum and maximum size of the words, plus the facecolor.
plt.figure(figsize=(20, 10), facecolor='k')
plt.imshow(wordcloud, interpolation="bilinear")

# # create coloring from image
# image_colors = ImageColorGenerator(image_mask)
# plt.figure(figsize=[7,7])
# plt.imshow(wordcloud.recolor(color_func=image_colors), cmap='gray_r', interpolation="bilinear")

plt.axis("off")
plt.savefig(repo_path + 'wordcloud.pdf', bbox_inches='tight')  # get the final output in a pdf file
plt.savefig(repo_path + 'wordcloud.png', bbox_inches='tight')  # get the final output in a png file
plt.tight_layout(pad=0)

# Display the image
plt.show()
