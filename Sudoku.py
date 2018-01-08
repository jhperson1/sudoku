#!/user/bin/env/Python

from pulp import *

class SudokuPULP():
    ''' Use SudokuPULP to solve a 9 x 9 sudoku problem '''
    def __init__(self, board):
        n = len(board)

    # convert 9 x 9 board of values 1-9 and 0 at blank squares ---> list of tuples (row, col, value) representing hints
    def readFromBoard(self, board):
        hints = []
        for i in range(9):
            for j in range(9):
                val = board[i][j]
                if val != 0:
                    hints.append((i,j,val))

    def writeToBoard(self, variables):


    sudoku = LpProblem("Sudoku", LpMaximize)

    # set up constants
    # A list of strings from "1" to "9" is created
    Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # The Vals, Rows and Cols sequences all follow this form
    VALS = Sequence
    ROWS = Sequence
    COLS = Sequence

    # dictionary: key = (row, col, val), value = 0 or 1
    variables = LpVariables.dicts("choice", (VALS, ROWS, COLS), 0, 1, LpInteger)

    # add objective function
    sudoku += 0, "No specific objective function"

    # define the constraints
    def addSudokuRules():
        # only one value per index
        for i in range(9):
            for j in range(9):
                sudoku += lpSum([variables[i, j, k - 1]] for k in range(1,10)) == 1, "Single Value"

        # all rows sum to 45
        for j in range(9):
            sudoku += lpSum([variables[i, j, k - 1] * k] for i in range(9), for k in range(1,10)) == 45, "Row Sum"

        # all columns sum to 45
        for i in range(9):
            sudoku += lpSum([variables[i, j, k - 1] * k] for j in range(9), for k in range(1,10)) == 45, "Column Sum"

        # all boxes sum to 45
        for row_scale in range(3):
            for col_scale in range(3):
                for i in range(3):
                    for j in range(3):
                        sudoku += lpSum([variables[row_scale * 3 + i, col_scale * 3 + j,k - 1] * k for k in range(1,10)]) == 45, "Box Sum"

    def addSudokuHints():
        for index in hints:
            sudoku += variables[]