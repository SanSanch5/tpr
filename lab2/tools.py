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
    return abs((math.cos(a1+a3) * math.tanh(a2**3 + a3) - (a6 + a7)**2) / (a4 + a5))
    # return abs(math.cos(a1+a2+a3+a4+a5+a6+a7))
    # return a1+a2+a3+a4+a5+a6+a7


# случайным образом изменяем каждый атрибут, возвращаем только те, что дают лучшее значение функции, чем предок
def make_mutations(generation, mutations_for_attribute_percent, attributes_values, attributes_values_count):
    mutations = []
    for attributes in generation:
        have_better = False
        f_val = f(*attributes)
        for i in range(7):
            attribute_values_count = attributes_values_count[i]
            mutations_count = attribute_values_count * mutations_for_attribute_percent / 100
            mutation = attributes.copy()
            for mutation_number in range(int(math.ceil(mutations_count))):
                mutation[i] = attributes_values[i][randint(0, attribute_values_count-1)]
                # if f(*mutation) < f_val:
                #    have_better = True
                mutations.append(mutation)

        # если из потомства не оказалось никого лучше, то оставляем предка
        # if not have_better:
        #     mutations.append(attributes)
    return mutations


