#!/user/bin/env/Python

from pulp import *
import pandas as pd
import csv
import numpy as np
import Board

class SudokuPandasDF():

    ''' Use pandas dataframe of binary variables to solve a 9 x 9 sudoku puzzle as a linear program '''

    def __init__(self):
        self.prob = LpProblem("Sudoku", LpMaximize)
        self.Sequence, self.Vals, self.Rows, self.Cols = self._addBasics()
        self.choices = self._addChoices()
        self._addObjective()
        self._addSudokuRules()
        self._welcome()
        self._updateStatus()
        self._printStatus()
        return None

    def addBoard(self, board):
        hints = self._readFromBoard(board)
        board.printBoard("unsolved")
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

    def solutionWriteUp(self, board):
        board.printBoard("solved")

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

    # ------ helper functions ------- #

    def _welcome(self):
        print("\nWelcome to the LP Sudoku Solver!")
        print("Sudoku rules have been")
        print("uploaded to your solver")

    def _addBasics(self):
        Sequence = np.array(range(1,10))
        return Sequence, Sequence, Sequence, Sequence

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

    def _addChoices(self):
        def _createDataFrameCSV(name):
            def _labelBoxes(row, col):  # row, col in [1,9] --> box in [1,9]
                return (col-1)/3 + (row-1)/3 * 3 + 1
            vals = range(1,10) * 81
            rows = [j for j in range(1,10) for i in range(81)]
            cols = [j for i in range(1,10) for j in range(1,10) for k in range(1,10)]
            boxes = [0 for _i in range(729)]
            l_original = (vals, rows, cols, boxes)
            l_transpose = zip(*l_original)
            l_transpose = list(l_transpose)
            for i in range(729):  # set up boxes column
                r, c = l_transpose[i][1], l_transpose[i][2]
                l_transpose[i] = list(l_transpose[i])
                l_transpose[i][3] = _labelBoxes(r,c)
                l_transpose[i] = tuple(l_transpose[i])
            with open(name, "wb") as f:
                writer = csv.writer(f)
                names = ['vals','rows','cols','boxes']
                writer.writerow(names)
                writer.writerows(l_transpose)
        _createDataFrameCSV("sudoku_pandas_df_indicies.csv")
        choices = pd.read_csv('/Users/jessicahuang/Desktop/z_freewheel/sudoku/sudoku_pandas_df_indicies.csv')
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
        def _valueConstraint():
            for _, sub_choices in self.choices.groupby(['rows', 'cols']):
                self.prob += lpSum(sub_choices['choice'].tolist()) == 1
        def _rowConstraint():
            for _, sub_choices in self.choices.groupby(['rows', 'vals']):
                self.prob += lpSum(sub_choices['choice'].tolist()) == 1
        def _colConstraint():
            for _, sub_choices in self.choices.groupby(['cols', 'vals']):
                self.prob += lpSum(sub_choices['choice'].tolist()) == 1
        def _boxConstraint():
            for _, sub_choices in self.choices.groupby(['boxes', 'vals']):
                self.prob += lpSum(sub_choices['choice'].tolist()) == 1
        _valueConstraint()
        _rowConstraint()
        _colConstraint()
        _boxConstraint()
        return None

    def _readFromBoard(self, board):  # convert 9 x 9, values 1-9 and 0 at blank squares
                                      # --> list of tuples (row, col, value) representing hints
        hints = []
        for y in range(1,10):
            for x in range(1,10):
                val = board.getValue(x-1, y-1)
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
        board = Board.Board()
        for r in self.Sequence:
            for c in self.Sequence:
                for v in self.Sequence:
                    e = self.choices[(self.choices['vals'] == int(v)) & (self.choices['cols'] == int(c)) & (self.choices['rows'] == int(r))]['choice'].tolist()
                    if value(e[0]) == 1.0:
                        board.setValue(int(r)-1, int(c)-1, v)
        return board

    def _convertIntToNumpyInt(x):
        return np.array([x])[0]