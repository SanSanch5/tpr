# взять данные из первой лабы, придумать функцию ото всех атрибутов и найти её экстремум:
# 1. классическим алгоритмом
# 2. генетическим


import numpy as np
import sys

from tools import f, iterate_all_combinations, make_mutations



data_file = "data/ecoli_attributes.data"
dataset_shape = (336, 7)

print("Reading dataset...")
real_classes = []
all_attributes = np.zeros(shape=dataset_shape)
with open(data_file) as file:
    i = 0
    for line in file:
        line = line.rstrip('\n')
        attributes = line.split()
        all_attributes[i] = attributes
        i += 1

attributes_values_sets = [list(set(column_values)) for column_values in all_attributes.T]
attributes_values_count = [len(s) for s in attributes_values_sets]

# implement Erebor method ########################
# f_min = sys.float_info.max
# it = 0
# for combination in iterate_all_combinations(attributes_values_sets):
#     f_val = f(*combination)
#     if f_val < f_min:
#         print("iter ", it, ": min now is ", f_min)
#         f_min = f_val
#     it += 1
#
# print(f_min)

###################################################


# try genetic algorithm ###########################
bests_count = 100
iter_count = 1000
mutations_for_attribute_percent = 20
generation = all_attributes.copy()

f_min = sys.float_info.max
for i in range(iter_count):
    f_vals = [f(*attributes) for attributes in generation]
    f_vals_bests_sorted = sorted(f_vals)[:bests_count]

    # следующее поколение не должно давать результат хуже предыдущего
    # assert f_vals_bests_sorted[0] <= f_min, "Smth went wrong; it: %i, current f_min is %f, prev f_min was %f" % (i, f_vals_bests_sorted[0], f_min)

    # if f_min == f_vals_bests_sorted[0]:
    #     break

    f_min = f_vals_bests_sorted[0]

    generation_bests = [generation[f_vals.index(best)] for best in f_vals_bests_sorted]

    if i % 50 == 0:
        print("iter", i, ": min now is ", f_min, "attributes:", *generation_bests[0])

    generation = make_mutations(generation_bests, mutations_for_attribute_percent,
                                attributes_values_sets, attributes_values_count)
