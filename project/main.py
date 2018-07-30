import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import IntegerType, DoubleType, StringType
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, LinearSVC, NaiveBayes, OneVsRest
from pyspark.ml.feature import HashingTF, RegexTokenizer, StopWordsRemover, ChiSqSelector, IDF
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

if __name__ == "__main__":
    file_path = "data/data.csv"

    spark = SparkSession.builder \
        .master("local") \
        .appName("5408-project") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    schema = StructType([
        StructField("tweet", StringType(), False),
        StructField("label", IntegerType(), False),
        StructField("confidence", DoubleType(), False)
    ])

    data_df = spark.read.csv(file_path, header=True,
                             schema=schema, mode="DROPMALFORMED")

    # print(data_df.count())

    splits = data_df.randomSplit([0.8, 0.2], 4)

    training = splits[0]
    test = splits[1]

    regex_tokenizer = RegexTokenizer(inputCol="tweet", outputCol="words", pattern="\\s+")

    # stop_words = ["http", "https", "rt", "the", "RT", "@", "a", "an"] + StopWordsRemover.loadDefaultStopWords("english")
    # stop_words_remover = StopWordsRemover(inputCol="words", outputCol="filtered_words", stopWords=stop_words)

    hashing_tf = HashingTF(inputCol="words", outputCol="tf")

    idf = IDF(inputCol="tf", outputCol="features")

    #------------------------------------------------------------------------------------------------------------------
    # selector = ChiSqSelector(featuresCol="idf", outputCol="features", labelCol="label")

    layers = [10, 8, 5, 3]
    trainer = MultilayerPerceptronClassifier(featuresCol="selected_features", layers=layers, seed=4)

    svm = LinearSVC()

    nb = NaiveBayes(modelType="multinomial")

    lr = LogisticRegression()

    ovr = OneVsRest(classifier=svm)
    #------------------------------------------------------------------------------------------------------------------

    pipeline = Pipeline(stages=[regex_tokenizer, hashing_tf, idf, ovr])

    model = pipeline.fit(training)

    result = model.transform(test)
    result.show()

    predictionAndLabels = result.select("prediction", "label")
    evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
    print("Test set accuracy = " + str(evaluator.evaluate(predictionAndLabels)))

    model.write().overwrite().save("the-model")

    spark.stop()
