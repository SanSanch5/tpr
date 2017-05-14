import math
from random import randint


def iterate_all_combinations(matrix):
    for a1 in matrix[0]:
        for a2 in matrix[1]:
            for a3 in matrix[2]:
                for a4 in matrix[3]:
                    for a5 in matrix[4]:
                        for a6 in matrix[5]:
                            for a7 in matrix[6]:
                                yield a1, a2, a3, a4, a5, a6, a7


def f(a1, a2, a3, a4, a5, a6, a7):
    # return abs((math.cos(a1+a3) * math.tanh(a2**3 + a3) - (a6 + a7)**2) / (a4 + a5))
    return abs(math.cos(a1+a2+a3+a4+a5+a6+a7))
    # return a1+a2+a3+a4+a5+a6+a7


# случайным образом изменяем каждый атрибут, возвращаем только те, что дают лучшее значение функции, чем предок
def make_mutations(generation, mutations_count_percent, attributes_values, attributes_values_count):
    mutations = []
    for attributes in generation:
        mutations_count = sum(attributes_values_count) * mutations_count_percent / 100
        for mutation_number in range(int(math.ceil(mutations_count))):
            i = randint(0, 6)
            attribute_values_count = attributes_values_count[i]
            mutation = attributes.copy()
            mutation[i] = attributes_values[i][randint(0, attribute_values_count-1)]
            mutations.append(mutation)

    return mutations


