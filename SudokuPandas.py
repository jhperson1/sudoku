#!/user/bin/env/Python

import pandas

# choices is the dataframe

def _addChoices():
    choices = pandas.dataframe({"val", [1,9]}, {"row", [1,9]}, {"col", [1,9]}, {"choice", [0,1]})

def _addConstraints():
    # value constraint: forall i,j: sum_k {c_ijk} == 1
    for i in range(1,10):
        for j in range(1,10):
            t = choices.where("row" == i, "col" == j)
            prob += LpSum([t]) == 1, ""

    # row and column constraint:
    # forall i,k: sum_j {c_ijk} == 1
    # forall k,k: sum_i {c_ijk} == 1
    for i in range(1,10):
        for k in range(1,10):
            t = choices.where("row" == i, "val" == k)
            prob += LpSum([t]) == 1, ""

    for j in range(1,10):
        for k in range(1,10):
            t = choices.where("col" == j, "val" == k)
            prob += LpSum([t]) == 1, ""

    # box constraint: forall k, boxes: sum_(i,j) {c_ijk} == 1
    for box in boxes:
        for k in range(1,10):
            prob += LpSum([choices.where("row" == r, "col" == c, "val" == k)] for (r,c) in box)

def _addBoard(self, board):
    for i in range(9):
        for j in range(9):
            self.choices = board[i][j]