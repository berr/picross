import numpy
from collections import Counter

BLACK = 1
WHITE = -1
EMPTY = 0


class Board():

    def __init__(self, board, lines, columns):
        self._board = board
        self._lines = lines
        self._columns = columns
        self._empty_entries = sum(board.reshape(-1) == EMPTY)


    @classmethod
    def create_empty_board(cls, lines, columns):
        board = numpy.zeros((len(lines), len(columns)), dtype=numpy.int8)
        return Board(board, lines, columns)


    @classmethod
    def copy_board(cls, board):
        return Board(board._board.copy(), board._lines, board._columns)

    @classmethod
    def create_from_board(cls, board, lines, columns):
        board = numpy.array(board, dtype=numpy.int8)
        for i in xrange(len(board)):
            board[i] = numpy.array(board[i], dtype=numpy.int8)

        return Board(board, lines, columns)


    def __getitem__(self, item):
        return self._board[item]


    def __setitem__(self, key, value):
        self._board[key] = value


    def _line_size(self):
        return len(self._columns)


    def _column_size(self):
        return len(self._lines)


    def check_line(self, line_number):
        line = self._lines[line_number]
        maximum_number_blacks = sum(line)
        maximum_number_whites = self._line_size() - maximum_number_blacks

        current_line = self._board[line_number,:]

        return self._check_array(
            current_line, line, maximum_number_blacks, maximum_number_whites,
            direction='line', direction_index=line_number,
        )


    def check_column(self, column_number):
        column = self._columns[column_number]
        maximum_number_blacks = sum(column)
        maximum_number_whites = self._column_size() - maximum_number_blacks

        current_column = self._board[:,column_number]

        return self._check_array(
            current_column, column, maximum_number_blacks, maximum_number_whites,
            direction='column', direction_index=column_number,
        )


    def _check_array(self, array, conditions, maximum_blacks, maximum_whites, direction, direction_index):
        count = Counter(array)

        if count[BLACK] > maximum_blacks:
            return False
        elif count[WHITE] > maximum_whites:
            return False


        strings_so_far = 0
        reading_string = False
        string_length = 0

        for i,s in enumerate(array):
            if s == EMPTY:
                if direction == 'line':
                    index = (direction_index, i)
                    check = lambda b: b.check_line(direction_index)
                elif direction == 'column':
                    index = (i, direction_index)
                    check = lambda b: b.check_column(direction_index)

                non_deterministic_board = Board.copy_board(self)

                non_deterministic_board[index] = BLACK
                if check(non_deterministic_board):
                    return True

                non_deterministic_board[index] = WHITE
                return check(non_deterministic_board)


            elif s == WHITE:
                if reading_string:
                    reading_string = False
                    strings_so_far += 1

                string_length = 0

            elif s == BLACK:
                if strings_so_far == len(conditions):
                    return False

                reading_string = True
                string_length += 1

                if string_length > conditions[strings_so_far]:
                    return False
            else:
                assert False


        return True


    def _array_priority(self, array, conditions):
        non_empty_entries = len(array) - sum(array != EMPTY)
        blocks = len(conditions)

        if non_empty_entries == 0:
            return -1

        return 2*non_empty_entries + blocks


    def _lines_priority(self):
        priorities = [self._array_priority(self._board[i, :], self._lines[i]) for i in xrange(len(self._lines))]
        return sorted(range(len(priorities)), key=lambda x: priorities[x])


    def _columns_priority(self):
        priorities = [self._array_priority(self._board[:, i], self._columns[i]) for i in xrange(len(self._columns))]
        return sorted(range(len(priorities)), key=lambda x: priorities[x])


    def solve(self, depth=1):
        if depth < 1:
            return True

        in_invalid_state = lambda b, ll, cc: not (b.check_line(ll) and b.check_column(cc))

        it = 0

        soft_limit = 6
        hard_limit = len(self._board)
        current_limit = soft_limit


        while self._empty_entries > 0:

            found_cell = False
            print 'Iteration {}: Remaning: {}'.format(it, self._empty_entries)

            lines_priority = self._lines_priority()
            for desired_line in lines_priority[:current_limit]:
                print 'Current line: {}. Remaining: {}'.format(desired_line, self._empty_entries)

                for c in xrange(self._line_size()):
                    if self._board[desired_line, c] == EMPTY:
                        non_deterministic_board = self.copy_board(self)
                        non_deterministic_board._empty_entries -= 1

                        non_deterministic_board[desired_line, c] = BLACK
                        black_failed = in_invalid_state(non_deterministic_board, desired_line, c)
                        if not black_failed and self._empty_entries > 1:
                            black_failed = not non_deterministic_board.solve(depth - 1)
                            if not black_failed and non_deterministic_board._empty_entries == 0:
                                self._board = non_deterministic_board._board
                                return True

                        non_deterministic_board[desired_line, c] = WHITE
                        white_failed = in_invalid_state(non_deterministic_board, desired_line, c)
                        if not white_failed and self._empty_entries > 1:
                            white_failed = not non_deterministic_board.solve(depth - 1)
                            if not white_failed and non_deterministic_board._empty_entries == 0:
                                self._board = non_deterministic_board._board
                                return True



                        if black_failed and white_failed:
                            return False
                        elif black_failed:
                            self._board[desired_line, c] = WHITE
                            self._empty_entries -= 1
                            found_cell = True
                        elif white_failed:
                            self._board[desired_line, c] = BLACK
                            self._empty_entries -= 1
                            found_cell = True




            columns_priority = self._columns_priority()
            for desired_column in columns_priority[:current_limit]:
                print 'Current column: {}. Remaining: {}'.format(desired_column, self._empty_entries)

                for l in xrange(self._column_size()):
                    if self._board[l, desired_column] == EMPTY:
                        non_deterministic_board = self.copy_board(self)
                        non_deterministic_board._empty_entries -= 1

                        non_deterministic_board[l, desired_column] = BLACK
                        black_failed = in_invalid_state(non_deterministic_board, l, desired_column)
                        if not black_failed and self._empty_entries > 1:
                            black_failed = not non_deterministic_board.solve(depth - 1)
                            if not black_failed and non_deterministic_board._empty_entries == 0:
                                self._board = non_deterministic_board._board
                                return True

                        non_deterministic_board[l, desired_column] = WHITE
                        white_failed = in_invalid_state(non_deterministic_board, l, desired_column)
                        if not white_failed and self._empty_entries > 1:
                            white_failed = not non_deterministic_board.solve(depth - 1)
                            if not white_failed and non_deterministic_board._empty_entries == 0:
                                self._board = non_deterministic_board._board
                                return True



                        if black_failed and white_failed:
                            return False
                        elif black_failed:
                            self._board[l, desired_column] = WHITE
                            self._empty_entries -= 1
                            found_cell = True
                        elif white_failed:
                            self._board[l, desired_column] = BLACK
                            self._empty_entries -= 1
                            found_cell = True


            if not found_cell:
                if current_limit == hard_limit:
                    raise RuntimeError('Insufficient information or low depth')
                else:
                    current_limit = hard_limit
            else:
                current_limit = soft_limit

            it += 1

        return True