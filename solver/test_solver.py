import pytest
import numpy
from solver import Board
from solver import BLACK as B
from solver import WHITE as W
from solver import EMPTY as E


def test_change_board():
    board = Board.create_empty_board([[], [], []], [[], [], [], []])

    board[1,1] = W
    board[2,2] = B


    for i in range(3):
        for j in range(3):
            if (i,j) not in [(1,1), (2,2)]:
                assert board[i,j] == E


    assert board[1,1] == W
    assert board[2,2] == B


@pytest.mark.parametrize(['state', 'expected'],[
    ([E, E, E], True),
    ([E, E, B], True),
    ([E, E, W], True),
    ([E, B, E], True),
    ([E, B, B], True),
    ([E, B, W], True),
    ([B, E, E], True),
    ([B, E, W], True),
    ([B, B, E], True),
    ([B, B, W], True),
    ([W, E, E], True),
    ([W, E, B], True),
    ([W, B, E], True),
    ([W, B, B], True),

    ([E, W, E], False),
    ([E, W, B], False),
    ([E, W, W], False),
    ([B, W, E], False),
    ([B, W, B], False),
    ([B, W, W], False),
    ([W, W, E], False),
    ([W, W, B], False),
    ([W, W, W], False),
    ([W, E, W], False),
    ([W, B, W], False),
    ([B, E, B], False),
    ([B, B, B], False),


])
def test_check_line(state, expected):
    board = Board.create_empty_board([[2], [], []], [[], [], []])

    for i, s in enumerate(state):
        board[0, i] = s

    assert board.check_line(0) == expected


@pytest.mark.parametrize(['state', 'expected'],[
    ([E, E, E], True),
    ([E, E, B], True),
    ([E, E, W], True),
    ([E, B, E], True),
    ([E, B, B], True),
    ([E, B, W], True),
    ([B, E, E], True),
    ([B, E, W], True),
    ([B, B, E], True),
    ([B, B, W], True),
    ([W, E, E], True),
    ([W, E, B], True),
    ([W, B, E], True),
    ([W, B, B], True),

    ([E, W, E], False),
    ([E, W, B], False),
    ([E, W, W], False),
    ([B, W, E], False),
    ([B, W, B], False),
    ([B, W, W], False),
    ([W, W, E], False),
    ([W, W, B], False),
    ([W, W, W], False),
    ([W, E, W], False),
    ([W, B, W], False),
    ([B, E, B], False),
    ([B, B, B], False),


])
def test_check_column(state, expected):
    board = Board.create_empty_board([[], [], []], [[], [2], []])

    for i, s in enumerate(state):
        board[i, 1] = s

    assert board.check_column(1) == expected



@pytest.mark.parametrize(['state', 'expected'],[
    ([E, E, E, E, E, E, E, E, E, E], True),
    ([E, E, B, E, B, E, E, E, E, E], True),
    ([E, E, B, E, B, E, B, E, E, E], True),
    ([E, B, B, E, B, E, E, E, E, E], True),
    ([E, E, B, B, B, E, E, E, E, E], False),
    ([W, W, W, E, E, E, W, W, W, W], False),
    ([W, W, W, E, E, E, E, W, W, W], False),
    ([W, W, W, E, E, E, E, W, E, B], True),
])
def test_check_line_complex(state, expected):
    board = Board.create_empty_board([[], [], [2, 1, 2]], [[]] * 10)

    for i, s in enumerate(state):
        board[2, i] = s

    assert board.check_line(2) == expected



def board_to_list(board):
    board = list(board)
    for i in xrange(len(board)):
        board[i] = list(board[i])

    return board


def test_solve_simple():
    board = Board.create_E_board([[1], [1], [1]], [[1], [1], [1]])
    board[0,0] = B

    board.solve(depth=5)

    expected = [[B, W, W], [W, B, W], [W, W, B]]


    assert board_to_list(board._board) == expected


def test_solve_simple():
    board = Board.create_empty_board([[1], [1], [1]], [[1], [1], [1]])
    board[0,0] = B

    board.solve(depth=5)

    expected = [[B, W, W], [W, B, W], [W, W, B]]


    assert board_to_list(board._board) == expected



def test_solve_problem():
    b = [
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, B, B, E, E, E, E, E, E, E, B, B, E, E, E, E, E, E, E, B, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, B, B, E, E, B, E, E, E, B, B, E, E, B, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, B, E, E, E, E, B, E, E, E, E, B, E, E, E, B, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, B, B, E, E, E, E, B, B, E, E, E, E, B, E, E, E, E, B, B, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
        [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
    ]

    lines = [
        [7,3,1,1,7],
        [1,1,2,2,1,1],
        [1,3,1,3,1,1,3,1],
        [1,3,1,1,6,1,3,1],
        [1,3,1,5,2,1,3,1],
        [1,1,2,1,1],
        [7,1,1,1,1,1,7],
        [3,3],
        [1,2,3,1,1,3,1,1,2],
        [1,1,3,2,1,1],
        [4,1,4,2,1,2],
        [1,1,1,1,1,4,1,3],
        [2,1,1,1,2,5],
        [3,2,2,6,3,1],
        [1,9,1,1,2,1],
        [2,1,2,2,3,1],
        [3,1,1,1,1,5,1],
        [1,2,2,5],
        [7,1,2,1,1,1,3],
        [1,1,2,1,2,2,1],
        [1,3,1,4,5,1],
        [1,3,1,3,10,2],
        [1,3,1,1,6,6],
        [1,1,2,1,1,2],
        [7,2,1,2,5],
    ]

    columns = [
        [7,2,1,1,7],
        [1,1,2,2,1,1],
        [1,3,1,3,1,3,1,3,1],
        [1,3,1,1,5,1,3,1],
        [1,3,1,1,4,1,3,1],
        [1,1,1,2,1,1],
        [7,1,1,1,1,1,7],
        [1,1,3],
        [2,1,2,1,8,2,1],
        [2,2,1,2,1,1,1,2],
        [1,7,3,2,1],
        [1,2,3,1,1,1,1,1],
        [4,1,1,2,6],
        [3,3,1,1,1,3,1],
        [1,2,5,2,2],
        [2,2,1,1,1,1,1,2,1],
        [1,3,3,2,1,8,1],
        [6,2,1],
        [7,1,4,1,1,3],
        [1,1,1,1,4],
        [1,3,1,3,7,1],
        [1,3,1,1,1,2,1,1,4],
        [1,3,1,4,3,3],
        [1,1,2,2,2,6,1],
        [7,1,3,2,1,1],
    ]

    board = Board.create_from_board(b, lines, columns)


    board.solve()

    print board._board