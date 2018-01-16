#!/user/bin/env/Python

import csv

import codecs
import pdb

class Board():
    def __init__(self):
        self.board = [[0] * 9 for i in range(9)] # empty board

    def setBoardCSV(self, valuesCSV):
        board = []
        with codecs.open(valuesCSV, "r", encoding="utf-8-sig") as f:
            for line in f:
                int_line = line[::2] # map(lambda i: line[i], filter(lambda i: i%2 == 0,range(len(line)))) # discard commas at odd indices
                row = []
                for e in int_line:
                    row.append(int(e))
                board.append(row)
        self.board = board

    def getValue(self, x, y):
        return self.board[x][y]

    def setValue(self, x, y, v):
        self.board[x][y] = v
        return None

    def printBoard(self, type):
        print("Here's the " + str(type) + " board \n")
        for row in self.board:
            print("{}".format(row))


board = Board()
board.setBoardCSV("sudoku_board1.csv")


# references
# https://stackoverflow.com/questions/34304945/split-xef-xbb-xbf-in-a-list-read-from-a-file/34305017