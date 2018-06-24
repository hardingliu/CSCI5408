import tweepy
import socket
import requests
import time
import csv
import stat
import os
import socket
import json
import re


# Reference Dijana Kosmajac's code provided for A3
class TwitterStreamListener(tweepy.StreamListener):
    """
    A listener handles tweets are the received from the stream.
    This is a basic listener that sends recieved tweets through a socket.
    """

    def __init__(self, sc):
        super(TwitterStreamListener, self).__init__()
        self.client_socket = sc

    def on_status(self, status):
        # get_tweet returns user.id, screen_name, cleaned text
        tweet = self.get_tweet(status)
        # send cleaned tweets to spark stream
        self.client_socket.send((tweet[2] + "\n").encode('utf-8'))
        return True

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes

    def on_error(self, status_code):
        print("Status code")
        print(status_code)
        if status_code == 403:
            print("The request is understood, but the access is not allowed. Limit may be reached.")
            return False

    def get_tweet(self, tweet):
        text = tweet.text
        if hasattr(tweet, 'extended_tweet'):
            text = tweet.extended_tweet['full_text']
        return [str(tweet.user.id), tweet.user.screen_name, self.clean_str(text)]

    def clean_str(self, string):
        """
        Tokenization/string cleaning.
        """
        string = re.sub(r'http[^\s]*', ' ', string)
        string = re.sub(r'[\n\t\r]', ' ', string)
        string = re.sub(r'[^a-zA-Z0-9\'\s]', '', string)
        return string


if __name__ == '__main__':
    # Authentication
    consumer_key = "2a6tv2Ve6LPIAtuIY9YVM66NZ"
    consumer_secret = "jYoK0NpDhD9OvhTmpdgdIw9r5EA0Wu1CNSz4iRMSROcc0cMczu"
    access_token = "1000021124061782017-gDczTk8OS2yrGvg4MUdFO6jkXHGlMx"
    access_token_secret = "dyWS0fHGylTKXLOQRRj6levpciNU2YdICiqxc25K7WuAU"

    # Local connection
    # host = "172.31.38.165"          # Get local machine name (copy internal address from EC2 instance).
    # port = 5555                 # Reserve a port for your service.
    host = "localhost"
    port = 9999

    s = socket.socket()  # Create a socket object.
    s.bind((host, port))  # Bind to the port.

    print("Listening on port: %s" % str(port))

    s.listen(5)  # Now wait for client connection.
    c, addr = s.accept()  # Establish connection with client.

    print("Received request from: " + str(addr))
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,
                     retry_count=10, retry_delay=5, retry_errors=5)

    streamListener = TwitterStreamListener(c)
    myStream = tweepy.Stream(
            auth=api.auth, listener=streamListener, tweet_mode='extended')
    # added a filter for only english language
    myStream.filter(track=['Movie', 'Movies'],
                    languages=['en'], async=True)
