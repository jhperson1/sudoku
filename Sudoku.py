#!/user/bin/env/Python

from pulp import *

class SudokuPULP():

    ''' Use SudokuPULP to solve a 9 x 9 sudoku problem '''

    def __init__(self, board):
        prob = LpProblem("Sudoku", LpMaximize)
        variables = _addVariables()
        self._addObjective()
        self._addSudokuRules()

    def addBoard(self, board):
        hints = _readFromBoard(board)
        self._addSudokuHints()
        self._problemWriteUp()

    def solve(self):
        prob.solve()
        print "Status:", LpStatus[prob.status]
        solved_board = _writeToBoard(variables)
        return solved_board

    def __str__(self):
        return self._solutionWriteUp()

    # ------------ Helper functions ------------ #

    # add sudoku variables
    def _addVariables(self):
        Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Vals = Sequence
        Rows = Sequence
        Cols = Sequence
        Boxes = []
        for r in range(3):
            for c in range(3):
                list = [[(Rows[3*r + i], Cols[3*c +j]) for i in range(3) for j in range(3)]]
                Boxes += list
        variables = LpVariables.dicts("choice", (Vals, Rows, Cols), 0, 1, LpInteger)
        return variables

    # add objective function
    def _addObjective(self):
        self.prob += 0, "No specific objective function"

    # define the constraints
    def _addSudokuRules(self):
        # only one value per index
        for r in Rows:
            for c in Cols:
                self.prob += lpSum([variables[v] [r] [c]] for v in Vals) == 1, "Single Value"

        # one of each value in each row, column, box
        for v in Vals:
            for r in Rows:
                self.prob += lpSum([variables[v] [r] [c]] for c in Cols) == 1, "Row Value"
            for c in Cols:
                self.prob += lpSum([variables[v] [r] [c]] for r in Rows) == 1, "Column Value"
            for b in Boxes:
                self.prob += lpSum([variables[v] [r] [c] for (r,c) in b]) == 1, "Box Value"

    # convert 9 x 9 board of values 1-9 and 0 at blank squares --> list of tuples (row, col, value) representing hints
    def _readFromBoard(self, board):
        hints = []
        for i in range(9):
            for j in range(9):
                val = board[i][j]
                if val != 0:
                    hints.append((i,j,val))
        return hints

    def _addSudokuHints(self):
        for (val, row, col) in hints:
            self.prob += variables[val][row][col] == 1, ""

    # The problem data is written to an .lp file
    def _problemWriteUp(self):
        self.prob.writeLP("Sudoku.lp")
        print("LP problem specifications written to Sudoku.lp")

    # converts dictionary of variables --> 9 x 9 board of values 1-9
    def _writeToBoard(self):
        board = []
        for r in Rows:
            for c in Cols:
                for v in Vals:
                    if value(self.variables[v][r][c]) == 1:
                        board[r][c] = v
        return board

    # The problem solution is written to a .txt file
    def _solutionWriteUp(self):
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
        return "Solution Written to sudokuout.txt"