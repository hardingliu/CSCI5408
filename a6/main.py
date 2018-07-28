from time import time
import csv
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn import metrics

def convert_target_to_num(target_data):
    target_counts = np.unique(target_data)
    target_counts = target_counts.tolist()

    for i in range(len(target_data)):
        target_data[i] = target_counts.index(target_data[i])

    return target_data.astype('int')

# ref - http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(cm, classes):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix, without normalization')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def run(clf_name, pipeline, num_jobs, class_names, X_train, y_train, X_test, y_test):
    N_FEATURES_OPTIONS = [40, "all"]
    param_grid = [
        {
            'reduce_dim': [SelectKBest(chi2)],
            'reduce_dim__k': N_FEATURES_OPTIONS
        },
    ]
    grid = GridSearchCV(pipeline, n_jobs=num_jobs, param_grid=param_grid)
    t0 = time()
    grid.fit(X_train, y_train)
    result = clf_name + " done in %0.3fs"
    print(result % (time() - t0))
    prediction = grid.predict(X_test)
    score = metrics.accuracy_score(y_test, prediction)
    cnf_matrix = confusion_matrix(y_test, prediction)
    result = clf_name + " accuracy:   %0.3f"
    print(result % score)
    print("Best parameter:", grid.best_params_)
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names)
    print()


if __name__ == "__main__":
    training_file_path = 'data/train.txt'
    test_file_path = 'data/test-gold.txt'

    training_df = pd.read_csv(training_file_path, sep='\t', header=None, encoding='utf-8', quoting=csv.QUOTE_NONE)
    test_df = pd.read_csv(test_file_path, sep='\t', header=None, encoding='utf-8', quoting=csv.QUOTE_NONE)

    linear_svm = Pipeline([
        ('tfidf_vect', TfidfVectorizer()),
        ('reduce_dim', SelectKBest(chi2)),
        ('classify', LinearSVC())
    ])

    logistic_regression = Pipeline([
        ('tfidf_vect', TfidfVectorizer()),
        ('reduce_dim', SelectKBest(chi2)),
        ('classify', LogisticRegression())
    ])

    decision_tree = Pipeline([
        ('tfidf_vect', TfidfVectorizer()),
        ('reduce_dim', SelectKBest(chi2)),
        ('classify', DecisionTreeClassifier())
    ])

    naive_bayes = Pipeline([
        ('tfidf_vect', TfidfVectorizer()),
        ('reduce_dim', SelectKBest(chi2)),
        ('classify', MultinomialNB())
    ])

    # training data and targets
    X_train = training_df.values[:, 0]  # shape = (252000,)
    training_target = training_df.values[:, 1]  # shape = (252000,)

    # test data and targets
    X_test = test_df.values[:, 0]
    test_target = test_df.values[:, 1]

    # get class names
    class_names = np.unique(test_target).tolist()

    # convert training and testing target from string to number
    y_train = convert_target_to_num(training_target)  # shape = (252000,)
    y_test = convert_target_to_num(test_target)

    # train different classifiers
    run("Linear SVM", linear_svm, 4, class_names, X_train, y_train, X_test, y_test)
    run("Logistic Regression", logistic_regression, 4, class_names, X_train, y_train, X_test, y_test)
    run("Decision Trees", decision_tree, 4, class_names, X_train, y_train, X_test, y_test)
    run("Naive Bayes", naive_bayes, 4, class_names, X_train, y_train, X_test, y_test)

    # plot the confusion matrices
    plt.show()

