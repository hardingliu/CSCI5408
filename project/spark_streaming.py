# Reference Dijana Kosmajac's code provided for A3

import sys
import pickle
import json
from collections import namedtuple
from pyspark.sql.types import *

from pyspark.sql.functions import col
from pyspark.sql import SQLContext, SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import desc
from pyspark.ml import PipelineModel

sc = SparkContext("local[2]", "Streaming App")

ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)

host = "localhost"
port = 9999

# Internal ip of  the tweepy streamer
socket_stream = ssc.socketTextStream(host, port)

lines = socket_stream.window(20)
# fields = ['tweet', 'coordinates', 'created_at', 'retweet_count', 'favorite_count']
fields = ("tweet")
tweet = namedtuple('Tweet', fields)

pipeline_model = PipelineModel.load("the-model")


def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def do_it(rdd):
    spark = SparkSession.builder \
        .master("local") \
        .appName("5408-project") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
                                                
    tweet = rdd['tweet']
    coordinates = rdd['coordinates']
    created_at = rdd['created_at']
    retweet_count = rdd['retweet_count']
    favorite_count = rdd['favorite_count']
    data = tweet, coordinates, created_at, retweet_count, favorite_count
    schema = ["tweet", "coordinates", "created_at", "retweet_count", "favorite_count"]
    print(data)
    df = spark.createDataFrame([data], schema)

    # Creates a temporary view using the DataFrame
    df.createOrReplaceTempView("Tweet")

    # Do tweet character count on table using SQL and print it
    final_df = spark.sql("SELECT * FROM Tweet")

    prediction = pipeline_model.transform(final_df)
    prediction.show()

    prediction.createOrReplaceTempView("tweets_prediction")
    finalDataFrame = spark.sql("SELECT prediction, tweet, coordinates, created_at, retweet_count, favorite_count FROM tweets_prediction")
    finalDataFrame.coalesce(1).write.save(path='csv', format='csv', mode='append')



def do_something(time, rdd):
    print("========= %s =========" % str(time))
    try:
        # Get the singleton instance of SparkSession
        spark = getSparkSessionInstance(rdd.context.getConf())
        # rdd = rdd.map(lambda l: json.loads(l))
        # rdd.foreach(do_it)
        # print(type(rdd))

        # Convert RDD[Dict] to RDD[Tweet] to DataFrame
        row_rdd = rdd.map(lambda w: tweet(w))
        linesDataFrame = spark.createDataFrame(row_rdd)

        # Creates a temporary view using the DataFrame
        linesDataFrame.createOrReplaceTempView("Tweet")

        # Do tweet character count on table using SQL and print it
        df = spark.sql("SELECT tweet FROM Tweet")

        prediction = pipeline_model.transform(df)
        prediction.show()

        prediction.createOrReplaceTempView("tweets_prediction")
        finalDataFrame = spark.sql("SELECT prediction, tweet FROM tweets_prediction")
        finalDataFrame.coalesce(1).write.save(path='csv', format='csv', mode='append')
    except:
        pass

# key part!
lines.foreachRDD(do_something)

ssc.start()
ssc.awaitTermination()
