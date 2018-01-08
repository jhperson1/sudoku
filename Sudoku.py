#!/user/bin/env/Python

from pulp import *

class SudokuPULP():
    ''' Use SudokuPULP to solve a 9 x 9 sudoku problem '''
    def __init__(self, board):
        n = len(board)
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

    # convert 9 x 9 board of values 1-9 and 0 at blank squares --> list of tuples (row, col, value) representing hints
    def readFromBoard(self, board):
        hints = []
        for i in range(9):
            for j in range(9):
                val = board[i][j]
                if val != 0:
                    hints.append((i,j,val))

    # define the constraints
    def addSudokuRules():
        # only one value per index
        for i in range(9):
            for j in range(9):
                sudoku += lpSum([variables[i] [j] [k - 1]] for k in range(1,10)) == 1, "Single Value"

        # all rows sum to 45
        for j in range(9):
            sudoku += lpSum([variables[i] [j] [k - 1] * k] for i in range(9), for k in range(1,10)) == 45, "Row Sum"

        # all columns sum to 45
        for i in range(9):
            sudoku += lpSum([variables[i] [j] [k - 1] * k] for j in range(9), for k in range(1,10)) == 45, "Column Sum"

        # all boxes sum to 45
        for row_scale in range(3):
            for col_scale in range(3):
                for i in range(3):
                    for j in range(3):
                        sudoku += lpSum([variables[row_scale * 3 + i][ col_scale * 3 + j] [k - 1] * k for k in range(1,10)]) == 45, "Box Sum"

    def addSudokuHints():
        for (val, row, col) in hints:
            sudoku += variables[val][row][col] == 1, ""

    # The problem data is written to an .lp file
    def problemWriteUp():
        sudoku.writeLP("Sudoku.lp")
        print("LP problem specifications written to Sudoku.lp")

    # converts dictionary of variables --> 9 x 9 board of values 1-9
    def writeToBoard(self, variables):
        board = []
        for r in Rows:
            for c in Cols:
                for v in Vals:
                    if value(choices[v][r][c])==1:
                        board[r][c] = v
        return board

    # The problem is solved
    def solve():
        sudoku.solve()
        print "Status:", LpStatus[prob.status]
        solved_board = writeToBoard(variables)
        print(solved_board)

    # The problem solution is written to a .txt file
    def solutionWriteUp():
        # A file called sudokuout.txt is created/overwritten for writing to
        sudokuout = open('sudokuout.txt','w')

        # The solution is written to the sudokuout.txt file
        for r in Rows:
            if r == "1" or r == "4" or r == "7":
                            sudokuout.write("+-------+-------+-------+\n")
            for c in Cols:
                for v in Vals:
                    if value(choices[v][r][c])==1:

                        if c == "1" or c == "4" or c =="7":
                            sudokuout.write("| ")

                        sudokuout.write(v + " ")

                        if c == "9":
                            sudokuout.write("|\n")
        sudokuout.write("+-------+-------+-------+")
        sudokuout.close()

        # The location of the solution is give to the user
        print "Solution Written to sudokuout.txt"