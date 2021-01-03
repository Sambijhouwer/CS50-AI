"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX, countO = 0,0
    for i in board:
        for j in i:
            if j == X:
                countX += 1
            elif j == O:
                countO += 1
    if countX > countO:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    options = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                options.add((i,j))
    return options


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    copy_board = copy.deepcopy(board)
    mover = player(copy_board)
    try:
        copy_board[i][j] = mover
    except:
        raise Exception
    
    return copy_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal / Vertical
    elems_d_1 = set()
    elems_d_2 = set()
    diagonals = [2,1,0]
    for i in range(len(board)):
        elems_h = set()
        elems_v = set()
        for j in range(len(board)):
            elems_h.add(board[i][j])
            elems_v.add(board[j][i])
        elems_d_1.add(board[i][i])
        elems_d_2.add(board[i][diagonals[i]])
        if len(elems_h) == 1 and None not in elems_h:
            return (next(iter(elems_h)))
        elif len(elems_v) == 1 and None not in elems_v:
            return (next(iter(elems_v)))

    if len(elems_d_1) == 1 and None not in elems_d_1:
        return next(iter(elems_d_1))
    if len(elems_d_2) == 1 and None not in elems_d_2:
        return next(iter(elems_d_2))
    
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    best_action = None
    if current_player == X:
        v = float('-inf')
        for action in actions(board):
            value = min_value(result(board, action))
            if value > v:
                v = value
                best_action = action
    else:
        v = float('inf')
        for action in actions(board):
            value = max_value(result(board,action))
            if value < v:
                v = value
                best_action = action
    
    return best_action


def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v