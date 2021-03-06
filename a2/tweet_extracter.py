import tweepy
import time
import json
import csv
import pandas

'''
Author: David Cui
'''
#this is written with the help of the Lab pdf posted on Brightspace, so the structure is similar, but the code is written by me.

#auth keys
consumer_key = "2a6tv2Ve6LPIAtuIY9YVM66NZ"
consumer_secret = "jYoK0NpDhD9OvhTmpdgdIw9r5EA0Wu1CNSz4iRMSROcc0cMczu"
access_key = "1000021124061782017-gDczTk8OS2yrGvg4MUdFO6jkXHGlMx"
access_secret = "dyWS0fHGylTKXLOQRRj6levpciNU2YdICiqxc25K7WuAU"

#auth and get api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#function for getting tweets with an input query
def get_tweets(query, count):
    try:
		#get full text tweets, only english tweets to make data cleaning easier
        tweets = api.search(query, count=count, tweet_mode='extended', lang="en")
    except tweepy.error.TweepError as e:
        trends = json.loads(e.response.text)

    return tweets

#inputs for get_tweets function
#querying WWDC WWDC18 WWDC2018 excluding retweets and replies
query = "#WWDC -filter:retweets AND -filter:replies"
tweetNum = 100

#get tweets with API and store in CSV file: tweets.csv
with open ('tweets.csv', 'w', encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['id','user','created_at','text'])
    tweets = get_tweets(query, tweetNum)
    for tweet in tweets:
        writer.writerow([tweet.id_str, tweet.user.screen_name, tweet.created_at, tweet.full_text])
		
#data cleaning
tweets = pandas.read_csv("tweets.csv", encoding="utf-8")
tweets["clean_text"]=tweets["text"].str.replace('http[^\s]*',' ')
tweets["clean_text"]=tweets["clean_text"].str.replace('[\n\r]',' ')
tweets["clean_text"]=tweets["clean_text"].str.replace('&amp;','and')
tweets["clean_text"]=tweets["clean_text"].str.replace('â€™','\'')
tweets["clean_text"]=tweets["clean_text"].str.replace('[^a-zA-Z0-9\'\s]','')

tweets.to_csv('tweets.csv', encoding="utf-8", index=False)