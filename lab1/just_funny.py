__author__ = 'alex'

# Взять набор классифицированных данных, представить, что они не классифицированы
# 80% данных кластеризовать, получить классы. Затем на них обучить классификатор
# и классифицировать оставшиеся 20%. Сравнить результаты с реальными данными.

# использую датасет шахматных позиций колорь+ладья против король+пешка (пешка в одном ходе от ферзя)
# из исходного набора данных вырезаю данные для тестовой выборки: строчки 651-1300,
# это примерно 20% от общей и в ней примерно поровну выигрышных и проигрышных позиций.
# остальное - обучающая выборка


import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler


training_data_file = "data/kr-vs-kp_training-set.data"
category_values = ['t', 'f', 'n', 'w', 'b', 'g', 'l']
dataset_shape = (2546, 36)

categories_le = LabelEncoder()
categories_le.fit(category_values)

print("Reading dataset...")
X = np.zeros(shape=dataset_shape)
with open(training_data_file) as f:
    i = 0
    for line in f:
        line = line.rstrip('\n')
        features_list = categories_le.transform(line.split(","))
        X[i] = features_list
        i += 1

print("Checking read values")
assert len(X) == dataset_shape[0], "Incorrect read of samples"
assert len(X[0]) == dataset_shape[1], "Incorrect read of features"

categories_enc = OneHotEncoder()
categories_enc.fit_transform(X)
StandardScaler().fit_transform(X)

print("Clustering")
af = AffinityPropagation(preference=-3100).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d, %d' % (n_clusters_, len(labels)))
