'''
Author: Zongming Liu (zongmingxliu@gmail.com)
Reference: the tutorial of A2
'''


import tweepy
import json
import csv


class TweetsCollector:
    def __init__(self, auth):
        self.api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    def get_tweets(self, query, count):
        try:
            tweets = self.api.search(query, lang='en', count=count,
                                     tweet_mode='extended')
            tweets = tweets['statuses']
        except tweepy.error.TweepError as e:
            tweets = [json.loads(e.response.text)]
        return tweets

    def save_to_csv(self, file_name, fields, queries):
        with open(file_name, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for query in queries:
                tweets = self.get_tweets(query, 100)
                for tweet in tweets:
                    row = []
                    for field in fields:
                        row.append(tweet.get(field))
                    writer.writerow(row)


if __name__ == '__main__':
    consumer_key = '2a6tv2Ve6LPIAtuIY9YVM66NZ'
    consumer_secret = 'jYoK0NpDhD9OvhTmpdgdIw9r5EA0Wu1CNSz4iRMSROcc0cMczu'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    access_token = '1000021124061782017-gDczTk8OS2yrGvg4MUdFO6jkXHGlMx'
    access_token_secret = 'dyWS0fHGylTKXLOQRRj6levpciNU2YdICiqxc25K7WuAU'

    auth.set_access_token(access_token, access_token_secret)

    tweets_collector = TweetsCollector(auth)
    tweets_collector.save_to_csv(
        './tweets.csv', ['full_text'],
        ["#WWDC"])
