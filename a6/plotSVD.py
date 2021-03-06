import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#convert language label to integer label
def convert_target_to_num(target_data):
    target_counts = np.unique(target_data)
    target_counts = target_counts.tolist()

    for i in range(len(target_data)):
        target_data[i] = target_counts.index(target_data[i])

    return target_data.astype('int')

#read training data and randomly select some
train_set = pd.read_csv('data/train.txt', sep='\t', names = ['text','lang'], encoding='utf-8')
selected_train_set = train_set.sample(n=1000)
selected_train_set = selected_train_set.reset_index(drop=True)
training_data = selected_train_set.values[:, 0]
training_target = selected_train_set.values[:, 1]

#feature extraction to dense matrix form
vect = TfidfVectorizer()
X_train = vect.fit_transform(training_data)

#convert language label to integer
y_train = convert_target_to_num(training_target)

svd_3d = TruncatedSVD(n_components=3).fit_transform(X_train)

#plot 3D SVD
fig = plt.figure('3D', figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
ax.scatter(svd_3d[:,0], svd_3d[:,1], svd_3d[:,2], c=y_train, cmap=plt.cm.Set1, edgecolor='k', s=40)
ax.set_xlabel("SVD1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("SVD2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("SVD3")
ax.w_zaxis.set_ticklabels([])

plt.show()
