#!/user/bin/env/Python
# Matt Alpert's Code

import math

import utils_MA

class board(object):

    def __init__(self, raw):
        self.raw_format = raw

    @property
    def raw_format(self):
        return self._raw_format

    @raw_format.setter
    def raw_format(self, raw):
        # ensure board has proper dimensions
        self._basic_validate(raw)

        # store board data
        self._raw_format = raw

        # process and store convenient views
        self._process_board()

    def get_row(self, row_num):
        return self._rows[row_num]

    def get_rows(self):
        return self._rows

    def get_column(self, col_num):
        return self._rows[col_num]

    def get_columns(self):
        return self._columns

    def get_digit(self, row_num, col_num):
        return self._rows[row_num][col_num]

    @staticmethod
    def _basic_validate(raw):
        num_cols = len(raw)

        for row in raw:
            if len(row) != num_cols:
                raise ValueError('There are {} columns but there is a row with {} digits'.format(num_cols,
                                                                                                 len(row)))

        if not utils_MA.is_square(num_cols):
            raise ValueError('Sudoku board side length {} is not a perfect square'.format(num_cols))

    def _process_board(self):
        # get side length of board and box
        self._dimension = len(self.raw_format)
        self._box_dimension = int(math.sqrt(self._dimension))

        self._rows = {row_num: row for row_num, row in enumerate(self.raw_format)}

        columns = {col_num: [] for col_num in range(self._dimension)}
        for row in self.raw_format:
            for col_num, digit in enumerate(row):
                columns[col_num].append(digit)
        self._columns = columns

    def __str__(self):
        lines = []

        # used for top/bottom of board and at end of boxes
        box_divider_row = '---' * self._box_dimension
        board_divider_row = '|' + '|'.join([box_divider_row] * self._box_dimension) + '|'

        # add rows
        for row_num, row in enumerate(self.raw_format):
            if row_num % self._box_dimension == 0:
                lines.append(board_divider_row)

            boxes_digits = [row[box_num * self._box_dimension: (box_num + 1) * self._box_dimension]
                            for box_num in range(self._box_dimension)]
            box_strings = [reduce(lambda acc, d: acc + ' {} '.format('-' if d is None else d), box_digits, '')
                           for box_digits in boxes_digits]
            lines.append('|' + '|'.join(box_strings) + '|')

        # bottom of board
        lines.append(board_divider_row)

        return '\n'.join(lines)


if __name__ == '__main__':
    import process_boards
    bd = process_boards.board_generator().next()
    b = board(bd)
    print(b)