# Reference Dijana Kosmajac's code provided for A3

import findspark
findspark.init()

from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, ChiSqSelector
from pyspark.ml.classification import LogisticRegression

from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import StringIndexer

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession \
    .builder \
    .appName("5408-A3") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .getOrCreate()

pipeline_model = PipelineModel.load("logreg.model")

# https://stackoverflow.com/a/44558280/8263143
schema = StructType([
    StructField("polarity", StringType(), True),
    StructField("id", StringType(), True),
    StructField("date", StringType(), True),
    StructField("query", StringType(), True),
    StructField("user", StringType(), True),
    StructField("text", StringType(), True)
    ])

# http://help.sentiment140.com/for-students - training dataset source
df = spark.read.csv("./training-data/testdata.manual.2009.06.14.csv", header=False, schema=schema)

drop_list = ["id", "date", "query", "user"]
df = df.select([column for column in df.columns if column not in drop_list])
df.show(5)

df.printSchema()

df.groupBy("polarity") \
        .count() \
        .orderBy(col("count").desc()) \
        .show()

df.groupBy("text") \
        .count() \
        .orderBy(col("count").desc()) \
        .show()

# set seed for reproducibility
(training_data, test_data) = df.randomSplit([0.7, 0.3], seed=100)
print("Training data count: " + str(training_data.count()))
print("Test data count: " + str(test_data.count()))

# regular expression tokenizer
regexTokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\W")

# stop words
add_stopwords = ["http", "https", "amp", "rt", "t", "c", "the", "RT", "@"]
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

# bag of words count
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

# convert string labels to indexes
indexer = StringIndexer(inputCol="polarity", outputCol="label")

# feature-selector
selector = ChiSqSelector(numTopFeatures=10, featuresCol="features",
                         outputCol="selectedFeatures", labelCol="label")

# logistic regression model
lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)

# build the pipeline
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, indexer, selector, lr])

# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(training_data)
prediction = pipelineFit.transform(test_data)

# Evaluation
evaluator = MulticlassClassificationEvaluator()
print("F1: %g" % (evaluator.evaluate(prediction)))

# save the trained model for future use
pipelineFit.write().overwrite().save("logreg.model")
