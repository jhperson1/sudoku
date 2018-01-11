#!/user/bin/env/Python

# purpose: read a txt file full of sudoku board puzzles

# incomplete file, can be implemented if we
# finish the rest of the components

import re

BOARDS_PATH = './sudoku_boards.txt'  # path to board data

def board_generator(path=BOARDS_PATH):
    with open(path, 'r') as f:

# unsure how to pattern match

        pattern = re.compile("Grid [0-9][0-9]")

        while f.readline():

        f.readline()

# board_generator()
pattern = "Grid [0-9][0-9]"
str = "Grid 09"
print(re.match(str,pattern))