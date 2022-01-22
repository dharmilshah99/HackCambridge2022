from textblob import TextBlob
import sys

filename = sys.argv[-1]
file = open(filename, 'rt')
text = file.read()
file.close()

Blobject = TextBlob(text)
sentiment = Blobject.sentiment.polarity

print(sentiment)