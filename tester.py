#!/user/bin/env/Python

import Sudoku
import SudokuPandas
import Board
import time
import pdb

def main():
    board = Board.Board()
    board.setBoardCSV("sudoku_board1.csv")

    start = time.time()

    # sudoku = Sudoku.SudokuDictionary() # load the sudoku solver
    sudoku = SudokuPandas.SudokuPandasDF()
    sudoku.addBoard(board) # fill the sudoku board in the data and the console
    solution = sudoku.solve() # solve the sudoku board
    sudoku.solutionWriteUp(solution) # write up the solution in the console and a txt file

    end = time.time()

    print("\nTotal time was: " + str(end-start))

if __name__ == "__main__":
    main()

    # board_unsolved  =  [[5,3,0,0,7,0,0,0,0],
    #                     [6,0,0,1,9,5,0,0,0],
    #                     [0,9,8,0,0,0,0,6,0],
    #                     [8,0,0,0,6,0,0,0,3],
    #                     [4,0,0,8,0,3,0,0,1],
    #                     [7,0,0,0,2,0,0,0,6],
    #                     [0,6,0,0,0,0,2,8,0],
    #                     [0,0,0,4,1,9,0,0,5],
    #                     [0,0,0,0,8,0,0,7,0]]

    # board_solved = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
    #                 [6, 7, 2, 1, 9, 5, 3, 4, 8],
    #                 [1, 9, 8, 3, 4, 2, 5, 6, 7],
    #                 [8, 5, 9, 7, 6, 1, 4, 2, 3],
    #                 [4, 2, 6, 8, 5, 3, 7, 9, 1],
    #                 [7, 1, 3, 9, 2, 4, 8, 5, 6],
    #                 [9, 6, 1, 5, 3, 7, 2, 8, 4],
    #                 [2, 8, 7, 4, 1, 9, 6, 3, 5],
    #                 [3, 4, 5, 2, 8, 6, 1, 7, 9]]
