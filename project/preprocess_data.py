import csv
import re


def clean_tweet(tweet):
    tweet = re.sub(r'\[.*\]', ' ', tweet)
    tweet = re.sub(r'https?://.*\b', ' ', tweet)
    tweet = re.sub(r'\W', ' ', tweet)
    tweet = re.sub(r'[0-9]+\b', ' ', tweet)
    tweet = re.sub(r'\s+', ' ', tweet)
    return tweet


if __name__ == "__main__":
    original_file_path = "data/1377884570_tweet_global_warming.csv"
    cleaned_file_path = "data/data.csv"
    with open(original_file_path, newline='', encoding='ISO-8859-1') as input_file, open(cleaned_file_path, 'w', newline='') as output_file:
        reader = csv.reader(input_file, delimiter=',')
        writer = csv.writer(output_file, delimiter=',')
        for row in reader:
            tweet = row[0]
            # tweet = clean_tweet(tweet)
            result = re.match(r'\w', tweet)
            if result is None:
                continue
            existence = row[1]
            result = re.match(r'\w', existence)
            if result is None:
                continue
            confidence = row[2]
            result = re.match(r'\w', existence)
            if result is None:
                continue
            if existence == 'N' or existence == 'No':
                existence = 0
            elif existence == 'Y' or existence == 'Yes':
                existence = 1
            elif existence == 'NA' or existence == 'N/A':
                existence = 2
            writer.writerow([tweet, existence, confidence])
