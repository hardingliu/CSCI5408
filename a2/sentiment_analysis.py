'''
Author: Zongming Liu (zongming.liu@dal.ca)
'''

import sys
import csv
from os.path import exists
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


class SentimentAnalysis:
    def __init__(self, input_file, output_file):
        if exists(input_file):
            self.input_file = input_file
            self.output_file = output_file
        else:
            msg = input_file + ' does not exist!'
            sys.exit(msg)

    def read_analyze_write(self):
        sentences = []
        with open(self.input_file, 'r') as input_csv_file:
            csv_reader = csv.reader(input_csv_file)
            for row in csv_reader:
                for s in row:
                    sentences.append(s.rstrip())
            sentences.pop(0)
        # http://www.nltk.org/howto/sentiment.html
        analyzer = SentimentIntensityAnalyzer()
        with open(self.output_file, 'w') as output_csv_file:
            csv_writer = csv.writer(output_csv_file)
            csv_writer.writerow(
                ['Tweet', 'Positive Score', 'Negative Score', 'Neutral Score',
                 'Sentiment Score', 'Sentiment'])
            for sentence in sentences:
                ss = analyzer.polarity_scores(sentence)
                row = []
                row.append(sentence)
                positive_score = ss['pos']
                row.append(positive_score)
                negative_score = ss['neg']
                row.append(negative_score)
                neutral_score = ss['neu']
                row.append(neutral_score)
                sentiment_score = ss['compound']
                row.append(sentiment_score)
                if sentiment_score > 0:
                    sentiment = 'positive'
                elif sentiment_score < 0:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
                row.append(sentiment)
                csv_writer.writerow(row)


if __name__ == '__main__':
    sentiment_analysis = SentimentAnalysis(
        './tweets.csv', './tweets_sentiment.csv')
    sentiment_analysis.read_analyze_write()
