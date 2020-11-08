#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import csv
import re #regular expression
from textblob import TextBlob
import string
import os
import tweepy
import preprocessor as p




#This is a basic listener that just prints received tweets to stdout.
ckey = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd

#pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(ckey, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# tweets_Parkinsons="tweets_Parkinsons_1MARS.csv"
# tweets_Epilepsy="tweets_Epilepsy_1MARS.csv"
# tweets_HeartDisease="tweets_HeartDisease_1MARS.csv"
tweets_covid19 = "tweets_covid19_AFTER_6_novomber.csv"



COLS = {'id':{} ,'created_at':{} , 'source' :{}, 
        'original_text' :{},'clean_text' :{}, 'sentiment':{},
        'polarity':{}, 'subjectivity':{} , 'lang':{},
        'favorite_count':{}, 'retweet_count':{}, 'original_author':{},  
        'possibly_sensitive':{}, 'hashtags':{},'user_mentions':{},
        'place':{}, 'place_coord_boundaries':{}}


#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)


#set two date variables for date range
import os
import pandas as pd
import tweepy
import re
import string
from textblob import TextBlob
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

start_date = '2020-04-02'
end_date = '2020-05-02'

 
#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)
 

def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
 
    #after tweepy preprocessing the colon left remain after removing mentions
    #or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
 
 
    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
 
    #filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
 
    #looping through conditions
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    #print(word_tokens)
    #print(filtered_sentence)
    
    
def write_tweets(keyword, file):
    # If the file exists, then read the existing data from the CSV file.
    if os.path.exists(file):
        df = pd.read_csv(file, header=0)
    else:
        df = pd.DataFrame(columns=COLS)
    #page attribute in tweepy.cursor and iteration
    for page in tweepy.Cursor(api.search, q=keyword,
                              count=200, include_rts=False, since=start_date).pages(50):
        for status in page:
            new_entry = []
            status = status._json
 
            ## check whether the tweet is in english or skip to the next tweet
            if status['lang'] != 'en':
                continue
 
            #when run the code, below code replaces the retweet amount and
            #no of favorires that are changed since last download.
            if status['created_at'] in df['created_at'].values:
                i = df.loc[df['created_at'] == status['created_at']].index[0]
                if status['favorite_count'] != df.at[i, 'favorite_count'] or                    status['retweet_count'] != df.at[i, 'retweet_count']:
                    df.at[i, 'favorite_count'] = status['favorite_count']
                    df.at[i, 'retweet_count'] = status['retweet_count']
                continue
 
 
           #tweepy preprocessing called for basic preprocessing
            #clean_text = p.clean(status['text'])
 
            #call clean_tweet method for extra preprocessing
            filtered_tweet=clean_tweets(status['text'])
 
            #pass textBlob method for sentiment calculations
            blob = TextBlob(filtered_tweet)
            Sentiment = blob.sentiment
 
            #seperate polarity and subjectivity in to two variables
            polarity = Sentiment.polarity
            subjectivity = Sentiment.subjectivity
 
            #new entry append
            new_entry += [status['id'], status['created_at'],
                          status['source'], status['text'],filtered_tweet, Sentiment,polarity,subjectivity, status['lang'],
                          status['favorite_count'], status['retweet_count']]
 
            #to append original author of the tweet
            new_entry.append(status['user']['screen_name'])
 
            try:
                is_sensitive = status['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            new_entry.append(is_sensitive)
 
            # hashtagas and mentiones are saved using comma separted
            hashtags = ", ".join([hashtag_item['text'] for hashtag_item in status['entities']['hashtags']])
            new_entry.append(hashtags)
            mentions = ", ".join([mention['screen_name'] for mention in status['entities']['user_mentions']])
            new_entry.append(mentions)
 
            #get location of the tweet if possible
            try:
                location = status['user']['location']
            except TypeError:
                location = ''
            new_entry.append(location)
 
            try:
                coordinates = [coord for loc in status['place']['bounding_box']['coordinates'] for coord in loc]
            except TypeError:
                coordinates = None
            new_entry.append(coordinates)
 
            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            df = df.append(single_tweet_df, ignore_index=True)
            csvFile = open(file, 'a' ,encoding='utf-8')
            df.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8")
    
    
#declare keywords as a query for three categories
Parkinson_keywords =  '#parkinsons OR #parkinsonsdisease OR #parkinsonsawareness OR #neuro OR #movement OR #parkinsonsregenerationtraining OR #exercises OR #brain OR #neuroscience OR #rocksteadyboxing OR #neurologist OR #brains OR #lifecoach OR #mentaltoughness OR #theparkinsoncouncil OR #highenergy OR #fitness OR #philly OR #motivationalspeaker OR #nodaysoff OR #makeadifference OR #itsalifestyle OR #manayunk OR #carvedup #tattedup #joeydemalavez #inspiration #strength OR #motivation OR  #bhfyp OR #Parkinsons OR #disease OR #parkinsondisease OR #parkinson OR #disorder OR #sentiment OR #drug OR #symptoms OR #hyperactivity OR #neuro OR #depression OR #degenerative #telemedicine OR #telehealth OR #digitalhealth OR #ehealth OR #parkinsons  OR #patient OR #digitaltransformation'
Epilepsy_keywords = '#Epilepsy OR #epilepsyawareness OR #epilepsyaction OR #epilepsyalerts OR #epilepsybed OR #epilepsycongres OR #epilepsysurgery OR #epilepsysurgery OR #Epilepsytreatment OR #seizures OR #seizurefree'
HeartDisease_keywords = '#HeartDisease OR #stroke OR #Stroking OR #strokepatient OR #StrokeSurvivor OR #hearthealth OR #Stroke OR #HeartFailure'
Covid19_keywords = 'COVID-19 OR #chloroquine OR cautions OR #hydroxychloroquine OR #remdesivir hydroxychloroquine OR chloroquine OR medication OR Chloroquine Oral OR #HeartDisease OR #stroke OR #Stroking  OR #strokepatient OR #Stroke Survivor OR #hearthealth OR #Stroke OR #HeartFailure OR Uses OR Side Effects OR Interactions OR Pictures OR Diphosphate Covid19 OR chloroquine OR COVID-19 OR epidemic OR corona OR coronavirus OR pandemic OR patient OR ADR OR risk OR #vaccine OR drug OR treatement OR #COVID-19 OR covid OR OR #SARS-CoV-2 OR corona OR #coronaviruses'

#call main method passing keywords and file path
#write_tweets(Parkinson_keywords,tweets_Parkinsons)
write_tweets(Covid19_keywords, tweets_covid19)
#write_tweets(HeartDisease_keywords, tweets_HeartDisease)
