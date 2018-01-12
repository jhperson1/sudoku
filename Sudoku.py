#!/user/bin/env/Python

from pulp import *

import pdb

class SudokuPULP():

    ''' Use SudokuPULP to solve a 9 x 9 sudoku problem '''

    def __init__(self):
        self.prob = LpProblem("Sudoku", LpMaximize)
        self.Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.Vals = self.Sequence
        self.Rows = self.Sequence
        self.Cols = self.Sequence
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

    # ------------ Helper functions ------------ #

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

    # add sudoku choices
    def _addChoices(self):
        choices = LpVariable.dicts("Choice", (self.Vals, self.Rows, self.Cols), 0, 1, LpInteger)
        return choices

    # add objective function
    def _addObjective(self):
        self.prob += 0, "No specific objective function"
        return None

    # define the constraints
    def _addSudokuRules(self):
        # only one value per index
        for r in self.Rows:
            for c in self.Cols:
                self.prob += lpSum([self.choices[v] [r] [c]] for v in self.Vals) == 1, ""

        # one of each value in each row, column, box
        for v in self.Vals:
            for r in self.Rows:
                self.prob += lpSum([self.choices[v] [r] [c]] for c in self.Cols) == 1, ""
            for c in self.Cols:
                self.prob += lpSum([self.choices[v] [r] [c]] for r in self.Rows) == 1, ""
            for b in self.Boxes:
                self.prob += lpSum([self.choices[v] [r] [c] for (r,c) in b]) == 1, ""
        return None

    # convert 9 x 9 board of values 1-9 and 0 at blank squares --> list of tuples (row, col, value) representing hints
    def _readFromBoard(self, board):
        hints = []
        for j in range(9):
            for i in range(9):
                val = board[i][j]
                if val != 0:
                    hints.append((str(val),str(i+1),str(j+1)))
        return hints

    def _addSudokuHints(self, hints):
        for (val, row, col) in hints:
            self.prob += self.choices[val][row][col] == 1, ""
        return None

    # The problem data is written to an .lp file
    def _problemWriteUp(self):
        self.prob.writeLP("Sudoku.lp")
        print("\n Board specifications written to Sudoku.lp")
        return None

    # converts dictionary of choices --> 9 x 9 board of values 1-9
    def _writeToBoard(self):
        board = [[0] * 9 for i in range(9)]
        for r in self.Rows:
            for c in self.Cols:
                for v in self.Vals:
                    if value(self.choices[v][r][c]) == 1:
                        board[int(r)-1][int(c)-1] = int(v)
        return board

    # The problem solution is written to a .txt file
    def _solutionWriteUp(self):
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