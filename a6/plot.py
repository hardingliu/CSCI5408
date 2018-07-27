import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

train_set = pd.read_csv('train.txt', sep='\t', names = ['text','lang'], encoding='utf-8')
selected_train_set = train_set.sample(n=100)
selected_train_set = selected_train_set.reset_index(drop=True)

vect = CountVectorizer()
sparse_dtm = vect.fit_transform(selected_train_set.text)
dense_dtm = pd.DataFrame(sparse_dtm.toarray(), columns=vect.get_feature_names())

#2D PCA
pca_2d = PCA(n_components=2).fit_transform(dense_dtm)
pca_2d = pd.DataFrame({'PC1':pca_2d[:,0],'PC2':pca_2d[:,1]})
pca_2d['Lang'] = selected_train_set.lang

#plot 2D PCA
fig = plt.figure('2D', figsize=(8,6))
plt.scatter(pca_2d['PC1'], pca_2d['PC2'], c=pca_2d['Lang'], cmap=plt.cm.Set1, edgecolor='k')
plt.xlabel('PC1')
plt.ylabel('PC2')

#3D PCA
pca_3d = PCA(n_components=3).fit_transform(dense_dtm)
pca_3d = pd.DataFrame({'PC1':pca_3d[:,0],'PC2':pca_3d[:,1],'PC3':pca_3d[:,2]})
pca_3d['Lang'] = selected_train_set.lang

#plot 3D PCA
fig = plt.figure('3D', figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
ax.scatter(pca_3d['PC1'], pca_3d['PC2'], pca_3d['PC3'], c=pca_3d['Lang'], cmap=plt.cm.Set1, edgecolor='k', s=40)
ax.set_title("First three PCA directions")
ax.set_xlabel("PC1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("PC2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("PC3")
ax.w_zaxis.set_ticklabels([])

plt.show()
