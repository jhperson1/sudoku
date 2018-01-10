#!/user/bin/env/Python

class Board():
    def __init__(self, values):
        # the underscore indicates that the user shouldn't
        # directly call the board attribute. instead the
        # user should use the methods of the board class
        self._board = values

    def getValue(self, x, y):
        self._board[x][y]

    def addValue(self, x, y, v):
        self._board[x][y] = v