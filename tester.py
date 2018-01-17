#!/user/bin/env/Python

import time
import Board
import Solver

def main():

    start = time.time()

    board = Board.Board()
    board.setBoardCSV("sudoku_board1.csv")   # load board from csv

    sudoku = Solver.SolverDictionary()       # load the sudoku solver:
                                             #     sudoku = Solver.SolverPandasDF()
                                             #     sudoku = Solver.SolverDictionary()

    sudoku.addBoard(board)                   # fill the sudoku board in the data and the console

    solution = sudoku.solve()                # solve the sudoku board

    sudoku.solutionWriteUp(solution)         # write up the solution in the console and a txt file
                                             # open sudokuout.txt
    end = time.time()

    print("\nTotal time was: " + str(end-start))

if __name__ == "__main__":
    main()