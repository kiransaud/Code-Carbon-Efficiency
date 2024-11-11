from sklearn import datasets
from sklearn.decomposition import PCA

# Load dataset
cancer = datasets.load_breast_cancer()
X = cancer.data

# PCA transformation
pca = PCA(n_components=2)
X_r = pca.fit_transform(X)

print("Explained variance ratio:", pca.explained_variance_ratio_)
