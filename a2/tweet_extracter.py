import tweepy
import time
import json
import csv

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

#function for cleaning tweet text
def clean_text(text):
    text.replace('[^a-zA-Z0-9\' ]','')

    return text
	
#inputs for get_tweets function
#querying WWDC excluding retweets and replies
query = "#WWDC -filter:retweets AND -filter:replies"
tweetNum = 100

#get tweets with API and store in CSV file: tweets.csv
with open ('tweets.csv', 'w', encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['id','user','created_at','full_text','cleaned_full_text'])
    tweets = get_tweets(query, tweetNum)
    for tweet in tweets:
        writer.writerow([tweet.id_str, tweet.user.screen_name, tweet.created_at, tweet.full_text, clean_text(tweet.full_text)])
