__author__ = 'alex'

# Запускается после работы основного скрипта и считает точность и полноту

import numpy as np


results_file_name = "data/result.txt"
print("Calculating precision and recall")
clusters = [0, 1, 3, 4, 5]
classes = ['cp', 'im', 'om', 'omL', 'pp']
map_clusters_to_classes = dict(zip(clusters, classes))
map_classes_to_clusters = dict(zip(classes, clusters))

results_matrix_shape = (len(clusters), len(clusters))
results_matrix = np.zeros(shape=results_matrix_shape)
with open(results_file_name) as f:
    for line in f:
        data = line.strip().split()
        if len(data) != 3 or data[1] in {'-1', '2'} or data[2] in {'imS'}:
            continue

        cluster = int(data[1])
        real_class = data[2]
        if data[2] == 'imU':
            real_class = 'im'
        i_cluster = clusters.index(cluster)
        i_class = classes.index(real_class)
        results_matrix[i_class, i_cluster] += 1

precision_array = results_matrix.diagonal() / results_matrix.sum(axis=1)
recall_array = results_matrix.diagonal() / results_matrix.sum(axis=0)

precision = precision_array.mean()
recall = recall_array.mean()

print("Precision mean = %f, recall mean = %f" % (precision, recall))
