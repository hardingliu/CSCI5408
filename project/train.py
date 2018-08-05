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

    splits = data_df.randomSplit([0.8, 0.2], 4)

    training = splits[0]
    test = splits[1]

    #-------------------------------------------------------------------------------------------------------------------

    tokenizer_svm = RegexTokenizer(inputCol="tweet", outputCol="words", pattern="\\s+")

    hashing_tf_svm = HashingTF(inputCol="words", outputCol="tf")

    idf_svm = IDF(inputCol="tf", outputCol="features")

    svm = LinearSVC()

    ovr = OneVsRest(classifier=svm)

    pipeline_svm = Pipeline(stages=[tokenizer_svm, hashing_tf_svm, idf_svm, ovr])

    model_svm = pipeline_svm.fit(training)
    result_svm = model_svm.transform(test)
    result_svm.show()

    predictionAndLabels = result_svm.select("prediction", "label")
    evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
    print("Test set accuracy = " + str(evaluator.evaluate(predictionAndLabels)))

    model_svm.write().overwrite().save("model-svm")

    #------------------------------------------------------------------------------------------------------------------
    tokenizer_nb = RegexTokenizer(inputCol="tweet", outputCol="words", pattern="\\s+")

    hashing_tf_nb = HashingTF(inputCol="words", outputCol="tf")

    idf_nb = IDF(inputCol="tf", outputCol="features")

    nb = NaiveBayes(modelType="multinomial")

    pipeline_nb = Pipeline(stages=[tokenizer_nb, hashing_tf_nb, idf_nb, nb])

    model_nb = pipeline_nb.fit(training)
    result_nb = model_nb.transform(test)
    result_nb.show()

    prediction_and_labels = result_nb.select("prediction", "label")
    evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
    print("Test set accuracy = " + str(evaluator.evaluate(prediction_and_labels)))

    model_nb.write().overwrite().save("model-nb")

    #------------------------------------------------------------------------------------------------------------------
    tokenizer_lr = RegexTokenizer(inputCol="tweet", outputCol="words", pattern="\\s+")

    hashing_tf_lr = HashingTF(inputCol="words", outputCol="tf")

    idf_lr = IDF(inputCol="tf", outputCol="features")

    lr = LogisticRegression()

    pipeline_lr = Pipeline(stages=[tokenizer_lr, hashing_tf_lr, idf_lr, lr])

    model_lr = pipeline_lr.fit(training)
    result_lr = model_lr.transform(test)
    result_lr.show()

    prediction_and_labels = result_lr.select("prediction", "label")
    evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
    print("Test set accuracy = " + str(evaluator.evaluate(prediction_and_labels)))

    model_lr.write().overwrite().save("model-lr")

    #------------------------------------------------------------------------------------------------------------------
    tokenizer_mlp = RegexTokenizer(inputCol="tweet", outputCol="words", pattern="\\s+")

    hashing_tf_mlp = HashingTF(inputCol="words", outputCol="tf")

    idf_mlp = IDF(inputCol="tf", outputCol="idf-features")

    selector = ChiSqSelector(numTopFeatures=40, featuresCol="idf-features",
                         outputCol="features")

    layers = [40, 30, 20, 10, 5, 3]

    mlp = MultilayerPerceptronClassifier(layers=layers)

    pipeline_mlp = Pipeline(stages=[tokenizer_mlp, hashing_tf_mlp, idf_mlp, selector, mlp])

    model_mlp = pipeline_mlp.fit(training)
    result_mlp = model_mlp.transform(test)
    result_mlp.show()

    prediction_and_labels = result_mlp.select("prediction", "label")
    evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
    print("Test set accuracy = " + str(evaluator.evaluate(prediction_and_labels)))

    model_mlp.write().overwrite().save("model-mlp")

    #-------------------------------------------------------------------------------------------------------------------
    spark.stop()
