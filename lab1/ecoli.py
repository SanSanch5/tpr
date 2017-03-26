__author__ = 'alex'

# Взять набор классифицированных данных, представить, что они не классифицированы
# 80% данных кластеризовать, получить классы. Затем на них обучить классификатор
# и классифицировать оставшиеся 20%. Сравнить результаты с реальными данными.

# содержание белка в различных компонентах организма

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


training_data_file = "data/ecoli_training_set.data"
dataset_shape = (264, 7)

print("Reading dataset...")
data_dict = {}
X = np.zeros(shape=dataset_shape)
with open(training_data_file) as f:
    i = 0
    for line in f:
        line = line.rstrip('\n')
        attributes = line.split()
        data_dict[attributes[0]] = attributes[1:]
        X[i] = attributes[1:]
        i += 1

print("Checking read values")
assert len(X) == dataset_shape[0], "Incorrect read of samples"
assert len(X[0]) == dataset_shape[1], "Incorrect read of features"

StandardScaler().fit_transform(X)

print("Clustering")
db = DBSCAN(eps=0.16, min_samples=2).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)

# plot
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()

