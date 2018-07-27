import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
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
train_set = pd.read_csv('train.txt', sep='\t', names = ['text','lang'], encoding='utf-8')
selected_train_set = train_set.sample(n=100)
selected_train_set = selected_train_set.reset_index(drop=True)
training_data = selected_train_set.values[:, 0]
training_target = selected_train_set.values[:, 1]

#feature extraction to dense matrix form
vect = TfidfVectorizer()
X_train = vect.fit_transform(training_data)
X_train = pd.DataFrame(X_train.toarray(), columns=vect.get_feature_names())

#convert language label to integer
y_train = convert_target_to_num(training_target)

#2D PCA
pca_2d = PCA(n_components=2).fit_transform(X_train)

#plot 2D PCA
fig = plt.figure('2D', figsize=(8,6))
plt.scatter(pca_2d[:,0], pca_2d[:,1], c=y_train, cmap=plt.cm.Set1, edgecolor='k')
plt.xlabel('PC1')
plt.ylabel('PC2')

#3D PCA
pca_3d = PCA(n_components=3).fit_transform(X_train)

#plot 3D PCA
fig = plt.figure('3D', figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
ax.scatter(pca_3d[:,0], pca_3d[:,1], pca_3d[:,2], c=y_train, cmap=plt.cm.Set1, edgecolor='k', s=40)
ax.set_title("First three PCA directions")
ax.set_xlabel("PC1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("PC2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("PC3")
ax.w_zaxis.set_ticklabels([])

plt.show()
