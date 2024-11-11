from sklearn import datasets
from sklearn.cluster import KMeans

# Load dataset
iris = datasets.load_iris()
X = iris.data

# Clustering
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(X)

# Print cluster centers
print("Cluster centers:\n", kmeans.cluster_centers_)
