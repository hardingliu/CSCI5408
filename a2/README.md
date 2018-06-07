# Assignment 2

## Team members
Zongming Liu - B00784897

David Cui - B00788648

## Scripts
**tweet_extracter.py** - The python script to collect data from Twitter. It saves the data to a csv file named tweets.csv

**sentiment_analysis.py** - The python script to perform sentiment analysis on the Twitter data we collected. It reads Twitter data from the tweets.csv, and writes the sentiment analysis results to a csv file named tweets_sentiment.csv

**import_into_elasticsearch.py** - The python script to load data of sentiment analysis on Twitter data, and import the data into Elasticsearch.

**batch_job.sh** - To run this script as background process, the user can add this script to cron. First, the user needs to type `crontab -e`, which will open the cron file for the user to edit. Then the user can just add this line `00 00 * * * ./batch_job.sh`. Finally, the user can just save the file, exit the editor, and the scirpt will be executed at 00:00 every day in every month.

## References
The dataset for sentiment analysis comes from here:

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
