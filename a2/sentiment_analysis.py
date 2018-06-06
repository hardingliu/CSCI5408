'''
Author: Zongming Liu (zongming.liu@dal.ca)
'''

# https://www.nltk.org/_modules/nltk/sentiment/vader.html
# https://github.com/cjhutto/vaderSentiment

import sys
import csv
from os.path import exists
from nltk import word_tokenize


class SentimentAnalysis:
    def __init__(self, input_file, output_file, lexicon_file):
        if exists(input_file) and exists(lexicon_file):
            self.input_file = input_file
            self.output_file = output_file
            self.lexicon_file = lexicon_file
        elif not exists(input_file):
            msg = input_file + " does not exist"
            sys.exit(msg)
        elif not exists(lexicon_file):
            msg = lexicon_file + " does not exist"
            sys.exit(msg)

    def load_lexicon(self):
        lexicon_dict = {}
        with open(self.lexicon_file, 'r') as lexicon_file:
            csv_reader = csv.reader(lexicon_file, delimiter='\t')
            for row in csv_reader:
                lexicon_dict[row[0]] = float(row[1])
        return lexicon_dict

    def read_analyze_write(self):
        sentences = []
        with open(self.input_file, 'r') as input_csv_file:
            csv_reader = csv.reader(input_csv_file)
            next(csv_reader)
            for row in csv_reader:
                sentence = ''
                clean_sentence = ''
                for s in row[-2]:
                    sentence += s
                for s in row[-1]:
                    clean_sentence += s
                sentence_tuple = (sentence, clean_sentence.rstrip())
                sentences.append(sentence_tuple)
        lexicon_dict = self.load_lexicon()
        with open(self.output_file, 'w') as output_csv_file:
            csv_writer = csv.writer(output_csv_file)
            csv_writer.writerow(
                ['Tweet', 'Sentiment Score', 'Sentiment'])
            for sentence_tuple in sentences:
                sentence = sentence_tuple[0]
                clean_sentence = sentence_tuple[1]
                tokens = word_tokenize(clean_sentence)
                row = []
                row.append(sentence)
                sentiment_score = 0
                num_valid_tokens = 0
                for token in tokens:
                    if token in lexicon_dict:
                        num_valid_tokens += 1
                        sentiment_score += lexicon_dict[token]
                if num_valid_tokens > 0:
                    sentiment_score = sentiment_score / num_valid_tokens
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
        './tweets.csv', './tweets_sentiment.csv',
        './vader_lexicon/vader_lexicon.txt')
    sentiment_analysis.read_analyze_write()
