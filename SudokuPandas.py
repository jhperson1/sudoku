#!/user/bin/env/Python

# references
# https://stackoverflow.com/questions/12555323/adding-new-column-to-existing-dataframe-in-python-pandas

import pandas as pd
import csv
from pulp import *
import numpy as np
import pdb
# import storage

def main():
    sudoku = Sudoku()
    sudoku.addBoard(board)
    solution = sudoku.solve()

class Sudoku():
    def __init__(self):
        self.prob = LpProblem("Sudoku", LpMaximize)
        self.Sequence = np.array(range(1,10))
        self._addChoicesIndicesCSV("sudoku_pandas_df_indicies.csv")
        self.Boxes = self._addBoxes()
        self.choices = self._addChoices()
        self._addObjective()
        self._addSudokuRules()
        print("\nWelcome to the LP Sudoku Solver!")
        print("Sudoku rules have been")
        print("uploaded to your solver")
        self._updateStatus()
        self._printStatus()
        return None

    def addBoard(self, board):
        hints = self._readFromBoard(board)
        print("Here's the unsolved board \n")
        for row in board:
            print("{}".format(row))
        self._addSudokuHints(hints)
        self._problemWriteUp()
        self._updateStatus()
        self._printStatus()
        return None

    def solve(self):
        print "Starting SUDOKU solving magic ..."
        print "(But it's strategic and precise magic because"
        print " we're using linear programming)"
        self.prob.solve()
        self._updateStatus()
        self._printStatus()
        solved_board = self._writeToBoard()
        return solved_board

    def __str__(self):
        return self._solutionWriteUp()

    # ------ helper functions ------- #

    def _updateStatus(self):
        self.status = LpStatus[self.prob.status]
        return None

    def _printStatus(self):
        print "\n Status: {} \n".format(self.status)
        if self.status == "Optimal":
            print "We've found a solution!"
        # elif self.status == "Not Solved":
        #     print "Enter your sudoku puzzle using the _addBoard method"
        # else:
        #     print "Something went wrong, consider checking the board"
        print "\n"
        return None

    # add sudoku boxes
    def _addBoxes(self):
        Boxes = []
        for r in range(3):
            for c in range(3):
                list = [[(self.Sequence[3*r + i], self.Sequence[3*c +j]) for i in range(3) for j in range(3)]]
                Boxes += list
        return Boxes

    def _addChoicesIndicesCSV(self, name):
        vals = range(1,10) * 81
        rows = [j for j in range(1,10) for i in range(81)]
        cols = [j for i in range(1,10) for j in range(1,10) for k in range(1,10)]
        l_original = (vals, rows, cols)
        l_transpose = zip(*l_original)
        with open(name, "wb") as f:
            writer = csv.writer(f)
            names = ['vals', 'cols', 'rows']
            writer.writerow(names)
            writer.writerows(l_transpose)

    def _addChoices(self):
        choices = pd.read_csv('sudoku_pandas_df_indices.csv')
        counter = 0
        for r in range(1,10):
            for c in range(1,10):
                for v in range(1,10):
                    choices.set_value(counter, 'choice', LpVariable("Choice_{}_{}_{}".format(v,r,c), 0, 1, LpInteger))
                    counter += 1
        return choices

    # add objective function
    def _addObjective(self):
        self.prob += 0, "No specific objective function"
        return None

    def _addSudokuRules(self):
        # value constraint: forall i,j: sum_k {c_xyz} == 1
        for x in range(1,10):
            for y in range(1,10):
                v = self.choices[(self.choices['rows'] == x) & (self.choices['cols'] == y)]['choice'].tolist()
                self.prob += lpSum(v) == 1, ""

        # row and column constraint:
        # forall x,z: sum_y {c_xyz} == 1
        # forall y,z: sum_x {c_xyz} == 1
        for x in range(1,10):
            for z in range(1,10):
                v = self.choices[(self.choices['rows'] == x) & (self.choices['vals'] == z)]['choice'].tolist()
                self.prob += lpSum(v) == 1, ""

        for y in range(1,10):
            for z in range(1,10):
                v = self.choices[(self.choices['cols'] == y) & (self.choices['vals'] == z)]['choice'].tolist()
                self.prob += lpSum(v) == 1, ""

        # box constraint: forall k, boxes: sum_(i,j) {c_ijk} == 1
        for box in self.Boxes:
            for (r,c) in box:
                v = self.choices[(self.choices['rows'] == r) & (self.choices['cols'] == c)]['choice'].tolist()
                self.prob += lpSum(v) == 1, ""
        return None

    # convert 9 x 9 board of values 1-9 and 0 at blank squares --> list of tuples (row, col, value) representing hints
    def _readFromBoard(self, board):
        hints = []
        for y in range(1,10):
            for x in range(1,10):
                val = board[x-1][y-1]
                if val != 0:
                    hints.append((str(val),str(x),str(y)))
        return hints

    def _addSudokuHints(self, hints):
        for (val, row, col) in hints:
            e = self.choices[(self.choices['vals'] == int(val)) & (self.choices['cols'] == int(col)) & (self.choices['rows'] == int(row))]['choice'].tolist()
            self.prob += lpSum(e) == 1, ""
        return None

    # The problem data is written to an .lp file
    def _problemWriteUp(self):
        self.prob.writeLP("Sudoku.lp")
        print("\n Board specifications written to Sudoku.lp")
        return None

    # converts dictionary of choices --> 9 x 9 board of values 1-9
    def _writeToBoard(self):
        board = [[0] * 9 for i in range(9)]
        for r in self.Sequence:
            for c in self.Sequence:
                for v in self.Sequence:
                    e = self.choices[(self.choices['vals'] == int(v)) & (self.choices['cols'] == int(c)) & (self.choices['rows'] == int(r))]['choice'].tolist()
                    if value(e[0]) == 1.0:
                        board[int(r)-1][int(c)-1] = v
        return board

    # The problem solution is written to a .txt file
    def _solutionWriteUp(self):
        # A file called sudokuout.txt is created/overwritten for writing to
        sudokuout = open('sudokuout.txt','w')

        # The solution is written to the sudokuout.txt file
        for r in self.Sequence:
            if int(r) == 1 or int(r) == 4 or int(r) ==7:
                            sudokuout.write("+-------+-------+-------+\n")
            for c in self.Sequence:
                for v in self.Sequence:
                    e = self.choices[(self.choices['vals'] == int(v)) & (self.choices['cols'] == int(c)) & (self.choices['rows'] == int(r))]['choice'].tolist()
                    if value(e[0]) == 1.0:

                        if int(c) == 1 or int(c) == 4 or int(c) ==7:
                            sudokuout.write("| ")

                        sudokuout.write(str(v) + " ")

                        if int(c) == 9:
                            sudokuout.write("|\n")
        sudokuout.write("+-------+-------+-------+")
        sudokuout.close()

        # The location of the solution is give to the user
        return "Solution Written to sudokuout.txt"

    def _convertIntToNumpyInt(x):
        return np.array([x])[0]



