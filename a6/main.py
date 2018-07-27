import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics


def convert_target_to_num(target_data):
    target_counts = np.unique(target_data)
    target_counts = target_counts.tolist()

    for i in range(len(target_data)):
        target_data[i] = target_counts.index(target_data[i])

    return target_data.astype('int')


if __name__ == "__main__":
    training_file_path = 'data/train.txt'
    test_file_path = 'data/test-gold.txt'

    training_df = pd.read_csv(training_file_path, sep='\t', header=None, encoding='utf-8', quoting=csv.QUOTE_NONE)
    test_df = pd.read_csv(test_file_path, sep='\t', header=None, encoding='utf-8', quoting=csv.QUOTE_NONE)

    # training data and targets
    training_data = training_df.values[:, 0]  # shape = (252000,)
    training_target = training_df.values[:, 1]  # shape = (252000,)

    # test data and targets
    test_data = test_df.values[:, 0]
    test_target = test_df.values[:, 1]

    # Vectorizing training and testing data
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(training_data)
    X_test = vectorizer.transform(test_data)

    # convert training and testing target from string to number
    y_train = convert_target_to_num(training_target)  # shape = (252000,)
    y_test = convert_target_to_num(test_target)

    clf = LinearSVC()
    clf.fit(X_train, y_train)
    prediction = clf.predict(X_test)
    score = metrics.accuracy_score(y_test, prediction)
    print("Linear SVM accuracy:   %0.3f" % score)

    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    prediction = clf.predict(X_test)
    score = metrics.accuracy_score(y_test, prediction)
    print("Logistic Regression accuracy:   %0.3f" % score)

    # it's taking so long...
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    prediction = clf.predict(X_test)
    score = metrics.accuracy_score(y_test, prediction)
    print("Decision Tree accuracy:   %0.3f" % score)

    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    prediction = clf.predict(X_test)
    score = metrics.accuracy_score(y_test, prediction)
    print("Multinomial NB accuracy:   %0.3f" % score)
