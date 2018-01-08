#!/user/bin/env/Python

import Sudoku

def main():
    # create test board
    board_unsolved = [[0,0,8,7,1,5,0,0,3],
                     [0,1,0,0,0,0,7,0,4],
                     [0,0,0,0,3,0,0,5,8],
                     [0,0,2,9,4,6,0,7,0],
                     [0,9,0,3,0,1,0,8,0],
                     [0,3,0,8,5,7,9,0,0],
                     [1,5,0,0,6,0,0,0,0],
                     [8,0,7,0,0,0,0,6,0],
                     [4,0,0,5,7,2,8,0,0]]
    board_solved   = [[2,4,8,7,1,5,6,9,3],
                     [3,1,5,6,8,9,7,2,4],
                     [9,7,6,2,3,4,1,5,8],
                     [5,8,2,9,4,6,3,7,1],
                     [7,9,4,3,2,1,5,8,6],
                     [6,3,1,8,5,7,9,4,2],
                     [1,5,9,4,6,8,2,3,7],
                     [8,2,7,1,9,3,4,6,5],
                     [4,6,3,5,7,2,8,1,9]]

    # instantiate the solver object
    solver = Sudoku.SudokuPULP()

    # read the board into the variables
    variables = solver.readFromBoard()

    # solve the board
    solver.solve(variables)

    # write the variables into the board
    solved = solver


if __init__ == "__main__":
    main()