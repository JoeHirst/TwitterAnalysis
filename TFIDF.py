import re
import json
import pandas as pd
import numpy as np
import nltk
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from nltk.tokenize import TweetTokenizer

pd.set_option('display.max_colwidth', 1000)
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999
my_stop_words = text.ENGLISH_STOP_WORDS.union(string.punctuation)
fileCorpus = []

for line in open('twitDB.json'):
	fileCorpus.append(json.loads(line)['text'].lower())

strCorpus = "".join(fileCorpus)

tk = nltk.tokenize.word_tokenize(strCorpus)

fltCorpus = [word for word in tk if word not in my_stop_words]

fltString = [" ".join(fltCorpus)]

wordDist = nltk.FreqDist(fltCorpus)

wordFreq = pd.DataFrame(wordDist.most_common(),
                    columns=['Word', 'Frequency'])
	
tknzr = TweetTokenizer()

vectorizer = CountVectorizer(min_df=1, tokenizer=tknzr.tokenize, stop_words=my_stop_words)
X = vectorizer.fit_transform(fileCorpus)
df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())

print("\nRaw Text:\n")
print(fileCorpus)
print("\nTokenized Text:\n")
print(fltCorpus)
#print("\nTFIDF:\n")
#print(df)
print("\nWord Frequency:\n")
print(wordFreq)
#print(wordFreq.to_json(orient='records'))

vectorizer = TfidfVectorizer(min_df=1, tokenizer=tknzr.tokenize, stop_words=my_stop_words)
X = vectorizer.fit_transform(fltString)
df= pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
for index, row in df.iterrows():
	s = pd.Series(df.loc[index].sort_values(ascending=False))[:50]

print("\nTFIDF Word Weight(Top 50):\n")
print(s.to_string())