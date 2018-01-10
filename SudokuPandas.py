#!/user/bin/env/Python

import pandas

def _addChoices():
    choices = pandas.dataframe({"val", [1,9]}, {"row", [1,9]}, {"col", [1,9]}, {"choice", [0,1]})

def _addConstraints():
    # value constraint: forall i,j: sum_k {c_ijk} == 1
    for i in range(1,10):
        for j in range(1,10):
            t = choices.where("row" == i, "col" == j)
            prob += LpSum([t]) == 1, ""

    # row and column constraint: forall i,k: sum_j {c_ijk} == 1
    for i in range(1,10):
        for k in range(1,10):
            t = choices.where("row" == i, "val" == k)
            prob += LpSum([t]) == 1, ""

    for j in range(1,10):
        for k in range(1,10):
            t = choices.where("col" == j, "val" == k)
            prob += LpSum([t]) == 1, ""

    # box constraint: forall k, boxes: sum_(i,j) {c_ijk} == 1

def _addBoard():