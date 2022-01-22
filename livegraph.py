#To run follow the upcoming instructions write the following in terminal:
# pip3 install -r requirements.txt
# python3 livegraph.py filename.txt

import collections
import pandas as pd
import sys
import nltk
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random

nltk.download('punkt')

filename = sys.argv[-1]
file = open(filename, 'rt')
text = file.read()
file.close()

tokens = nltk.word_tokenize(text)
# remove all tokens that are not alphabetic
words = [word.lower() for word in tokens if word.isalpha()]

colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
weights = [random.randint(15, 35) for i in range(30)]

data = go.Scatter(x=[random.random() for i in range(30)],
                 y=[random.random() for i in range(30)],
                 mode='text',
                 text=words,
                 marker={'opacity': 0.3},
                 textfont={'size': weights,
                           'color': colors})
layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                    'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
fig = go.Figure(data=[data], layout=layout)

plot(fig)