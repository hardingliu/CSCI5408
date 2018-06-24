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
    StructField("text", StringType(), True),
    ])

df = spark.read.csv("tweets.csv", header=False, schema=schema)

prediction = pipeline_model.transform(df)

result = prediction.select("text", "prediction") \
    .collect()

for row in result:
    print("text=%s -> prediction=%s"
          % (row.text, row.prediction))
