#!/user/bin/env/Python

import Sudoku
import SudokuPandas
import Board
import time
import Solver

def main():

    start = time.time()

    board = Board.Board()
    board.setBoardCSV("sudoku_board1.csv")  # load board from csv

    sudoku = Solver.SolverPandasDF()  # load the sudoku solver

    sudoku.addBoard(board) # fill the sudoku board in the data and the console

    solution = sudoku.solve() # solve the sudoku board

    sudoku.solutionWriteUp(solution) # write up the solution in the console and a txt file

    end = time.time()

    print("\nTotal time was: " + str(end-start))

if __name__ == "__main__":
    main()