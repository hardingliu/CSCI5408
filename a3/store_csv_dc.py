import findspark
findspark.init()

from pyspark.sql.functions import col
from pyspark.sql import SQLContext, SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from collections import namedtuple
from pyspark.sql.functions import desc
from pyspark.ml import PipelineModel

sc = SparkContext("local[2]", "Streaming App")

ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)

# host = "172.31.38.165"
# port = 5555
host = "localhost"
port = 9999

socket_stream = ssc.socketTextStream(host, port)  # Internal ip of  the tweepy streamer

lines = socket_stream.window(20)
lines.pprint()
fields = ("text")
Tweet = namedtuple('Tweet', fields)

pipeline_model = PipelineModel.load("logreg.model")


def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def do_something(time, rdd):
    print("========= %s =========" % str(time))
    try:
        # Get the singleton instance of SparkSession
        spark = getSparkSessionInstance(rdd.context.getConf())

        # Convert RDD[String] to RDD[Tweet] to DataFrame
        rowRdd = rdd.map(lambda w: Tweet(w))
        linesDataFrame = spark.createDataFrame(rowRdd)

        # Creates a temporary view using the DataFrame
        linesDataFrame.createOrReplaceTempView("tweets")

        # Do tweet character count on table using SQL and print it
        lineCountsDataFrame = spark.sql("select text from tweets")
        prediction = pipeline_model.transform(lineCountsDataFrame)
        prediction.show()
        lineCountsDataFrame.show()
        lineCountsDataFrame.coalesce(1).write.save(path='csv', format='csv', mode='append')
    except:
        pass


# key part!
lines.foreachRDD(do_something)

ssc.start()
ssc.awaitTermination()
