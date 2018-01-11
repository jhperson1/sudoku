
# Matt Alpert's Version

BOARDS_PATH = './sudoku_boards.txt'  # path to board data


def board_generator(path=BOARDS_PATH):
    with open(path, 'r') as f:
        # first line should always just label first board
        f.readline()

        board = []  # stores board in list of list form

        for line in f:
            content = line.strip()

            if content.startswith('Grid'):
                # we are done with the current board
                yield board

                # prepare for next one
                board = []
            else:
                board.append([digit if digit != 0 else None for digit in content])

        # snag the last one
        yield board

        return
