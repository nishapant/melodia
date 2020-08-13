from wordcloud import WordCloud, STOPWORDS
import numpy
from PIL import Image
import random


# returns a random color variation of green
def green_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ['#228B22', '#008000', '#006400', '#32CD32', '#3CB371', '#2E8B57', '#6B8E23', '#556B2F']
    return colors[random.randint(0, 7)]


# creates a word cloud in the shape of the spotify logo given a string of words
def create_word_cloud(string, shape_url):
    mask_array = numpy.array(Image.open(shape_url))

    wc = WordCloud(background_color="black", max_words=1000, mask=mask_array, stopwords=set(STOPWORDS), margin=12,
                   random_state=1).generate(string)

    wc.recolor(color_func=green_color_func, random_state=3)
    wc.to_file("wordCloud.png")
