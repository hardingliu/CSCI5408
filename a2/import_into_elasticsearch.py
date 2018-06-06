'''
Author: Zongming Liu (zongming.liu@dal.ca)
'''

# https://elasticsearch-dsl.readthedocs.io/en/latest/

import csv
import sys
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Index, Float, Keyword, Text
from elasticsearch_dsl.connections import connections
from os.path import exists

connections.create_connection(hosts=['localhost'])


class Tweet(DocType):
    tweet = Text(analyzer='snowball', fields={'raw': Keyword()})
    sentiment = Text(analyzer='snowball')
    sentiment_score = Float()

    class Meta:
        index = 'tweet-sentiment'

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Tweet, self).save(** kwargs)


class ImportIntoElasticsearch:
    def __init__(self, input_file):
        if exists(input_file):
            self.input_file = input_file
        else:
            msg = input_file + ' does not exist!'
            sys.exit(msg)

    def load_data(self):
        index = Index('tweet-sentiment')
        if not index.exists():
            Tweet.init()
        with open(self.input_file, 'r') as input_csv_file:
            csv_reader = csv.reader(input_csv_file)
            next(csv_reader)
            for row in csv_reader:
                tweet = Tweet(tweet=row[0], sentiment=row[-1],
                              sentiment_score=row[-2])
                tweet.save()


if __name__ == '__main__':
    elasticsearch_importer = ImportIntoElasticsearch('./hahah.csv')
    elasticsearch_importer.load_data()
