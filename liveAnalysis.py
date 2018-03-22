import json
import tweepy
import re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import TweetTokenizer

ckey = 'mOM0xFfIQLBxhk4RGXt1qJxuv'
csecret = 'mrbmLUbCbDBTiIb1zen4lYkaEEoIcjSKzyo41hQZdIpW5NYdef'
atoken = '903992855240335360-Muc0vCduGUWtpAKXCU1llLay8wQiiE2'
asecret = 'o0GdL9xq8fIyMgDm5H8LuB3srDSVivf1AQOJ22jxLVfla'

tknzr = TweetTokenizer()
analyzer = SentimentIntensityAnalyzer()

def getSentiment(sentence):
    sentiment = analyzer.polarity_scores(sentence)['compound']
    
    return sentiment

def wordCount(sentence):
    wordList = []
    wordCounts = {}
    tkn = tknzr.tokenize(sentence)
    for words in tkn:
        if not any(words in s for s in wordCounts):
            #wordList.append(words)
            #wordCounts[words] = tkn.count(words)
            count = tkn.count(words)
            for i in wordList:
                wordCounts = {
                    words: count
                    }
            wordCounts[words] = count
                   
    return str(wordCounts)

class listener(StreamListener):

    def on_data(self, data):
        rawTweet = json.loads(data)
        tweetByte = rawTweet['text'].encode('ascii', 'ignore')
        cleanTweet = tweetByte.decode('UTF-8')
        tweet = re.sub(r"http\S+", "", cleanTweet)
        tweet = re.sub(r"@(\S+)", "", tweet)

        time = rawTweet['created_at']

        if('RT  ' in tweet):
            for char in tweet:
                tweet = tweet.replace("RT  ","")
            
            sentiment = getSentiment(tweet)
            words = wordCount(tweet)
            #print(tweet, sentiment, words)
            tweetData = {}
            tweetData = {
                'text': tweet,
                'sentiment': sentiment,
                'time': time,
                'words': words
                }
                
            saveFile = open('twitDBa.json','a')
            s =  json.dumps(tweetData)
            print(str(s))
            saveFile.write(s)
            #saveFile.write(tweet)
            #saveFile.write(sentiment)
            #saveFile.write(str(words))
            #saveFile.write(json.dumps({{"tweet":tweet}, {"sentiment":sentiment}, {"wordcount":words}}))
            saveFile.write('\n')
            saveFile.close()
        
        return True

    def on_error(self, status):
        print (status)


auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"], languages=["en"])
