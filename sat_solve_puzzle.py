#!/usr/bin/env python3

import numpy as np
from pyeda.inter import And, NHot, Not, Or, exprvars

vars = exprvars("I", 11, 11)

conditions = []


def make_grid(solution) -> list[list[int]]:
    return [[solution[vars[row, col]] for col in range(11)] for row in range(11)]


for row in vars:
    conditions.append(NHot(2, *row))

for col in zip(*vars):
    conditions.append(NHot(2, *col))

regions = np.array(
    (
        (6, 6, 6, 6, 6, 8, 8, 5, 4, 4, 9),
        (6, 6, 0, 6, 6, 8, 5, 5, 4, 4, 9),
        (6, 6, 0, 8, 8, 8, 8, 5, 5, 4, 9),
        (6, 6, 0, 8, 1, 1, 1, 9, 5, 5, 9),
        (0, 6, 0, 8, 1, 9, 9, 9, 9, 9, 9),
        (0, 0, 0, 8, 1, 1, 1, 9, 2, 2, 2),
        (8, 8, 8, 8, 8, 8, 1, 9, 2, 10, 10),
        (8, 7, 7, 7, 1, 1, 1, 9, 2, 10, 10),
        (8, 7, 7, 3, 9, 9, 9, 9, 2, 10, 10),
        (8, 8, 7, 3, 3, 9, 9, 9, 2, 2, 2),
        (8, 7, 7, 3, 9, 9, 9, 9, 9, 9, 9),
    ),
    dtype=np.uint8,
)

for region_number in range(11):
    indices = zip(*np.where(regions == region_number))
    vars_in_region = [vars[int(y), int(x)] for y, x in indices]
    conditions.append(NHot(2, *vars_in_region))

expression = And(*conditions)
expression = expression.to_cnf()

print(repr(np.array(make_grid(expression.satisfy_one()))))

# top left adjacency
for row in range(10):
    for col in range(10):
        conditions.append(Or(Not(vars[row, col]), Not(vars[row + 1, col + 1])))

# top adjacency
for row in range(10):
    for col in range(11):
        conditions.append(Or(Not(vars[row, col]), Not(vars[row + 1, col])))

# top right adjacency
for row in range(10):
    for col in range(10):
        conditions.append(Or(Not(vars[row + 1, col]), Not(vars[row, col + 1])))

# left adjacency
for row in range(11):
    for col in range(10):
        conditions.append(Or(Not(vars[row, col]), Not(vars[row, col + 1])))

expression = And(*conditions)
expression = expression.to_cnf()

for solution in expression.satisfy_all():
    print(repr(np.array(make_grid(solution))))
