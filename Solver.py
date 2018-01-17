#!/user/bin/env/Python

from pulp import *
import pandas as pd
import csv
import numpy as np
import Board

class SolverParent(object):

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
        board.printBoard("unsolved")
        hints = self._readFromBoard(board)
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
    def solutionWriteUpALL(self):
        self.solutionWriteUp()

    # ------------ Helper functions ------------ #

    def _welcome(self):
        print("\nWelcome to the LP Sudoku Solver!")
        print("Sudoku rules have been")
        print("uploaded to your solver")
    def _updateStatus(self):
        self.status = LpStatus[self.prob.status]
        return None
    def _printStatus(self):
        print "\n Status: {} \n".format(self.status)
        if self.status == "Optimal":
            print "We've found a solution!"
        print "\n"
        return None
    def _addBasicsALL(self):
        self._addBasics()
    def _addChoicesALL(self):
        self._addChoices()
    def _addObjective(self):
        self.prob += 0, "No specific objective function"
        return None
    def _addSudokuRulesALL(self):
        self._addSudokuRules()
    def _readFromBoard(self, board):  # convert 9 x 9, values 1-9 and 0 at blank squares
                                      # --> list of tuples (row, col, value) representing hints
        hints = []
        for j in range(9):
            for i in range(9):
                val = board.getValue(i,j)
                if val != 0:
                    hints.append((str(val),str(i+1),str(j+1)))
        return hints
    def _addSudokuHintsALL(self, hints):
        self._addSudokuHints()
    def _problemWriteUp(self):  # The problem data is written to an .lp file
        self.prob.writeLP("Sudoku.lp")
        print("\n Board specifications written to Sudoku.lp")
        return None
    def _writeToBoardALL(self): # converts dictionary of choices --> 9 x 9 board of values 1-9
        self._writeToBoard()

class SolverPandasDF(SolverParent):

    ''' Use pandas dataframe of binary variables to solve a 9 x 9 sudoku puzzle as a linear program '''

    def __init__(self):
        super(SolverPandasDF, self).__init__()

    def solutionWriteUp(self, board):
        board.printBoard("solved")

        # A file called sudokuout.txt is created/overwritten for writing to
        sudokuout = open('sudokuout.txt','w')

        # The solution is written to the sudokuout.txt file
        for r in self.Sequence:
            if int(r) == 1 or int(r) == 4 or int(r) == 7:
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

    # ------------ Helper functions ------------ #

    def _addBasics(self):
        Sequence = np.array(range(1,10))
        return Sequence, Sequence, Sequence, Sequence
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
    def _addSudokuRules(self):
        def _elementConstraint():
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
        _elementConstraint()
        _rowConstraint()
        _colConstraint()
        _boxConstraint()
        return None
    def _addSudokuHints(self, hints):
        for (val, row, col) in hints:
            e = self.choices[(self.choices['vals'] == int(val)) & (self.choices['cols'] == int(col)) & (self.choices['rows'] == int(row))]['choice'].tolist()
            self.prob += lpSum(e) == 1, ""
        return None
    def _writeToBoard(self):  # converts dictionary of choices --> 9 x 9 board of values 1-9
        board = Board.Board()
        for r in self.Sequence:
            for c in self.Sequence:
                for v in self.Sequence:
                    e = self.choices[(self.choices['vals'] == int(v)) & (self.choices['cols'] == int(c)) & (self.choices['rows'] == int(r))]['choice'].tolist()
                    if value(e[0]) == 1.0:
                        board.setValue(int(r)-1, int(c)-1, v)
        return board

class SolverDictionary(SolverParent):

    ''' Use PULP dictionary of binary variables to solve a 9 x 9 sudoku puzzle as a linear program '''

    def __init__(self):
        super(SolverDictionary, self).__init__()

    def solutionWriteUp(self, board):
        board.printBoard("solved")

        # A file called sudokuout.txt is created/overwritten for writing to
        sudokuout = open('sudokuout.txt','w')

        # The solution is written to the sudokuout.txt file
        for r in self.Rows:
            if r == "1" or r == "4" or r == "7":
                            sudokuout.write("+-------+-------+-------+\n")
            for c in self.Cols:
                for v in self.Vals:
                    if value(self.choices[v][r][c])==1:

                        if c == "1" or c == "4" or c =="7":
                            sudokuout.write("| ")

                        sudokuout.write(v + " ")

                        if c == "9":
                            sudokuout.write("|\n")
        sudokuout.write("+-------+-------+-------+")
        sudokuout.close()

        # The location of the solution is give to the user
        return "Solution Written to sudokuout.txt"

    # ------------ Helper functions ------------ #

    def _addBasics(self):
        Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        return Sequence, Sequence, Sequence, Sequence
    def _addChoices(self):
        choices = LpVariable.dicts("Choice", (self.Vals, self.Rows, self.Cols), 0, 1, LpInteger)
        return choices
    def _addSudokuRules(self):
        def _elementConstraint():  # only one value per index
            for r in self.Rows:
                for c in self.Cols:
                    self.prob += lpSum([self.choices[v] [r] [c]] for v in self.Vals) == 1, ""
        def _rowConstraint():  # one of each value in each row, column, box
            for v in self.Vals:
                for r in self.Rows:
                    self.prob += lpSum([self.choices[v] [r] [c]] for c in self.Cols) == 1, ""
        def _colConstraint():
            for v in self.Vals:
                for c in self.Cols:
                    self.prob += lpSum([self.choices[v] [r] [c]] for r in self.Rows) == 1, ""
        def _boxConstraint():
            # add sudoku boxes
            def _addBoxes():
                Boxes = []
                for r in range(3):
                    for c in range(3):
                        list = [[(self.Sequence[3*r + i], self.Sequence[3*c +j]) for i in range(3) for j in range(3)]]
                        Boxes += list
                return Boxes
            Boxes = _addBoxes()
            for v in self.Vals:
                for b in Boxes:
                    self.prob += lpSum([self.choices[v] [r] [c] for (r,c) in b]) == 1, ""
        _elementConstraint()
        _rowConstraint()
        _colConstraint()
        _boxConstraint()
        return None
    def _addSudokuHints(self, hints):
        for (val, row, col) in hints:
            self.prob += self.choices[val][row][col] == 1, ""
        return None
    def _writeToBoard(self):  # converts dictionary of choices --> 9 x 9 board of values 1-9
        board = Board.Board()
        for r in self.Rows:
            for c in self.Cols:
                for v in self.Vals:
                    if value(self.choices[v][r][c]) == 1:
                        board.setValue(int(r)-1, int(c)-1, int(v))
        return board
