#!/user/bin/env/Python

from pulp import *

# solve sudoku puzzle
# using linear programming
# without an explicit objective function
# but with linear constraints that yield
# a unique solution

# more documentation:
#   https://pythonhosted.org/PuLP/CaseStudies/a_sudoku_problem.html

# January 5th, 2017
def readFromBoard(board):
    board_variables = []
    zeros = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        for j in range(9):
            val = board[i][j]

            #while loop approach
            board_variables[i][j] = zeros
            k = 1
            while k != val:
                k++
            board_variables[i][j][k - 1] = 1

            #for loop approach
            for k in range(1,10):
                if val == k:
                    board_variables[i][j][k] = 1
                else
                    board_variables[i][j][k] = 0
    return board_variables

# January 5th, 2017
def convertToBoard(board_variables):
    board = []
    for i in range(9):
        for j in range(9):
            vector = board[i][j][:]
            k = vector.index(1)
            board[i][j] = k + 1
    return board

# January 5th, 2017
def addconstraints():
    # only one value per index
    for i in range(9):
        for j in range(9):
            prob += lpSum([val[i][j][k - 1]] for k in range(1,10)) == 1, "Single Value"

    # all rows sum to 45
    for j in range(9):
        prob += lpSum([val[i][j][k - 1] * k] for i in range(9), for k in range(1,10)) == 45, "Row Sum"

    # all columns sum to 45
    for i in range(9):
        prob += lpSum([val[i][j][k - 1] * k] for j in range(9), for k in range(1,10)) == 45, "Column Sum"

    # all boxes sum to 45
    for row_scale in range(3):
        for col_scale in range(3):
            for i in range(3):
                for j in range(3):
                    prob += lpSum([val[row_scale * 3 + i][col_scale * 3 + j][k - 1] * k for k in range(1,10)]) == 45, "Box Sum"


## SPECIFICATIONS
# solveSudoku : int x int --> int x int
# board is a list of lists, with convention as index (0,0) representing the
# bottom left corner of the puzzle

def solveSudoku(board):
    board_variables = readFromBoard(board)
    '''Linear Programming'''
    new_board = convertToBoard(board_variables)
    return new_board

def main():
    unsolved = [[0,0,8,7,1,5,0,0,3],
                [0,1,0,0,0,0,7,0,4],
                [0,0,0,0,3,0,0,5,8],
                [0,0,2,9,4,6,0,7,0],
                [0,9,0,3,0,1,0,8,0],
                [0,3,0,8,5,7,9,0,0],
                [1,5,0,0,6,0,0,0,0],
                [8,0,7,0,0,0,0,6,0],
                [4,0,0,5,7,2,8,0,0]]
    solved   = [[2,4,8,7,1,5,6,9,3],
                [3,1,5,6,8,9,7,2,4],
                [9,7,6,2,3,4,1,5,8],
                [5,8,2,9,4,6,3,7,1],
                [7,9,4,3,2,1,5,8,6],
                [6,3,1,8,5,7,9,4,2],
                [1,5,9,4,6,8,2,3,7],
                [8,2,7,1,9,3,4,6,5],
                [4,6,3,5,7,2,8,1,9]]

    # solveSudoku(unsolved)
    s = readFromBoard(unsolved)
    print(s)

if __name__ == "__main__":
    main()