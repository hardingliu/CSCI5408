import findspark
findspark.init()

from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression

from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession \
    .builder \
    .appName("5408-A3") \
    .config("spark.some.config.option", "some-value") \
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

df = spark.read.csv("testdata.manual.2009.06.14.csv", header=False, schema=schema)

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
add_stopwords = ["http", "https", "amp", "rt", "t", "c", "the"]
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

# bag of words count
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

# convert string labels to indexes
label_stringIdx = StringIndexer(inputCol="polarity", outputCol="label")

lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)

# build the pipeline
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx, lr])

# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(training_data)
predictions = pipelineFit.transform(test_data)

# Evaluation
evaluator = MulticlassClassificationEvaluator()
print("F1: %g" % (evaluator.evaluate(predictions)))

# save the trained model for future use
pipelineFit.write().overwrite().save("logreg.model")
