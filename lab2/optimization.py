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
bests_percent, bests_min, bests_max = (10, 30, 500)
iter_count = 1000
resets_count = 100
mutations_count_percent = 60
generation = all_attributes.copy()

f_min = sys.float_info.max
opt_values = []
time_to_reset = int(iter_count / resets_count)
time_to_reset_initial = int(iter_count / resets_count)
for i in range(iter_count):
    f_vals = [f(*attributes) for attributes in generation]

    bests_count = int(np.ceil(len(f_vals) * bests_percent / 100))
    if bests_count < bests_min:
        bests_count = bests_min
    elif bests_count > bests_max:
        bests_count = bests_max

    f_vals_bests_sorted = sorted(f_vals)[:bests_count]

    f_min = f_vals_bests_sorted[0]

    generation_bests = [generation[f_vals.index(best)] for best in f_vals_bests_sorted]

    if time_to_reset == 0:
        print("iter", i, ": min now is ", f_min, "attributes:", *generation_bests[0])
        opt_values.append(f_min)
        generation = all_attributes.copy()
        time_to_reset = time_to_reset_initial
    else:
        generation = make_mutations(generation_bests, mutations_count_percent,
                                    attributes_values_sets, attributes_values_count)
    time_to_reset -= 1

print(*opt_values)
print("min value is", min(opt_values))
