__author__ = 'alex'

# Взять набор классифицированных данных, представить, что они не классифицированы
# 80% данных кластеризовать, получить классы. Затем на них обучить классификатор
# и классифицировать оставшиеся 20%. Сравнить результаты с реальными данными.

# содержание белка в различных компонентах организма
# Attribute Information.
#
#   1.  Sequence Name: Accession number for the SWISS-PROT database
#   2.  mcg: McGeoch's method for signal sequence recognition.
#   3.  gvh: von Heijne's method for signal sequence recognition.
#   4.  lip: von Heijne's Signal Peptidase II consensus sequence score.
#            Binary attribute.
#   5.  chg: Presence of charge on N-terminus of predicted lipoproteins.
# 	   Binary attribute.
#   6.  aac: score of discriminant analysis of the amino acid content of
# 	   outer membrane and periplasmic proteins.
#   7. alm1: score of the ALOM membrane spanning region prediction program.
#   8. alm2: score of ALOM program after excluding putative cleavable signal
# 	   regions from the sequence.
#
#
# Class Distribution. The class is the localization site. Please see Nakai &
# 		       Kanehisa referenced above for more details.
#
#  cp  (cytoplasm)                                    143
#  im  (inner membrane without signal sequence)        77
#  pp  (perisplasm)                                    52
#  imU (inner membrane, uncleavable signal sequence)   35
#  om  (outer membrane)                                20
#  omL (outer membrane lipoprotein)                     5
#  imL (inner membrane lipoprotein)                     2
#  imS (inner membrane, cleavable signal sequence)      2


import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn import svm


training_data_file = "data/ecoli_training_set.data"
dataset_shape = (264, 7)

print("Reading dataset...")
samples_names = []
real_classes = []
X = np.zeros(shape=dataset_shape)
with open(training_data_file) as f:
    i = 0
    for line in f:
        line = line.rstrip('\n')
        attributes = line.split()
        samples_names.append(attributes[0])
        X[i] = attributes[1:-1]
        real_classes.append(attributes[-1])
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

print("\nLearn SVM now")
clf = svm.SVC()
clf.fit(X, labels)
print("SVM learned: ", clf)

print("\nClassify test set")
test_data_file = "data/ecoli_test_set.data"
test_set_shape = (72, 7)

# При чтении тестовой выборки сформирую вектор из реальных классов, потом промаплю его в полученные кластеры
print("Reading test set...")
test_X = np.zeros(shape=test_set_shape)
with open(test_data_file) as f:
    i = 0
    for line in f:
        line = line.rstrip('\n')
        attributes = line.split()
        samples_names.append(attributes[0])
        test_X[i] = attributes[1:-1]
        real_classes.append(attributes[-1])
        i += 1

print("Checking read values")
assert len(X) == dataset_shape[0], "Incorrect read of test samples"
assert len(X[0]) == dataset_shape[1], "Incorrect read of test features"

print("Predict test set")
test_Y = clf.predict(test_X)

all_predicted = list(labels)
all_predicted.extend(list(test_Y))

output_file_name = "data/result.txt"
with open(output_file_name, 'w') as f:
    print("Sample name, predicted cluster's number and real class:", file=f)
    for name, pred, real_class in zip(samples_names, all_predicted, real_classes):
        print("%s\t%i\t%s" % (name, pred, real_class), file=f)

print("The result has been written to file %s" % output_file_name)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
