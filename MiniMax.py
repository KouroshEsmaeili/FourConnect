from copy import deepcopy
from json.encoder import INFINITY
import time
import numpy as np
import random
import copy

MAX_PLAYER = 2
MIN_PLAYER = 1
MAX_PLAYER_UTILITY = 100000
MIN_PLAYER_UTILITY = -100000
DRAW_UTILITY = 0
root1 = np.zeros((4, 4))


class State:
    def __init__(self, board, score, moves):
        self.board = board
        self.score = score
        self.moves: list = moves


def alpha_beta_search(root, depth):
    a = deepcopy(root)
    root_state = State(a, 0, [])
    return max_value(root_state, -INFINITY, INFINITY, depth)


def max_value(state: State, alpha, beta, depth):
    if terminal_test(state):
        return utility(state)
    if depth == 0:
        return State(deepcopy(state.board), score_calculator(state.board), deepcopy(state.moves))
    v = State(board=deepcopy(root1), score=-INFINITY, moves=[])
    for next_state in next_states(state, MAX_PLAYER):
        v = get_max_state(v, min_value(next_state, alpha, beta, depth - 1))
        if v.score >= beta:
            return v
        alpha = max(alpha, v.score)

    return v


def min_value(state: State, alpha, beta, depth):
    if terminal_test(state):
        return utility(state)
    if depth == 0:
        return State(deepcopy(state.board), score_calculator(state.board), deepcopy(state.moves))
    v = State(deepcopy(root1), INFINITY, [])
    for next_state in next_states(state, MIN_PLAYER):
        v = get_min_state(v, max_value(next_state, alpha, beta, depth - 1))
        if v.score <= alpha:
            return v
        beta = min(beta, v.score)

    return v


def get_max_state(s1: State, s2: State):
    if s1.score >= s2.score:
        return s1
    else:
        return s2


def get_min_state(s1: State, s2: State):
    if s1.score <= s2.score:
        return s1
    else:
        return s2


def terminal_test(state: State):
    board = state.board
    if we_have_match(board):
        return True
    return False


def we_have_match(board):
    if (is_vertical_match(board, MAX_PLAYER) or is_vertical_match(board, MIN_PLAYER) or
            is_horizontal_match(board, MAX_PLAYER) or is_horizontal_match(board, MIN_PLAYER) or
            is_diognal_match(board, MAX_PLAYER) or is_diognal_match(board, MIN_PLAYER) or
            is_all_full(board)):
        return True
    return False


def is_all_full(board):
    for cell in board:
        if 0 in cell:
            return False
    return True


def is_vertical_match(board, player):
    for i in range(board.shape[0] - 3):
        for j in range(board.shape[1]):
            if (board[i][j] == player and board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][
                j] == player):
                return True
    return False


def is_horizontal_match(board, player):
    for i in range(board.shape[0]):
        for j in range(board.shape[1] - 3):
            if (board[i][j] == player and board[i][j + 1] == player and board[i][j + 2] == player and board[i][
                j + 3] == player):
                return True
    return False


def is_diognal_match(board, player):
    for i in range(board.shape[0]):
        if i + 3 >= board.shape[0]:
            continue
        for j in range(board.shape[1]):
            if j + 3 >= board.shape[1]:
                continue
            if (board[i][j] == player and board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and
                    board[i + 3][j + 3] == player):
                return True
    for i in range(board.shape[0]):
        if i - 3 < 0:
            continue
        for j in range(board.shape[1]):
            if j + 3 >= board.shape[1]:
                continue
            if (board[i][j] == player and board[i - 1][j + 1] == player and board[i - 2][j + 2] == player and
                    board[i - 3][j + 3] == player):
                return True
    return False


def utility(state: State):
    board = state.board
    if is_vertical_match(board, MAX_PLAYER) or is_horizontal_match(board, MAX_PLAYER) or is_diognal_match(board,
                                                                                                          MAX_PLAYER):
        return State(deepcopy(board), MAX_PLAYER_UTILITY, deepcopy(state.moves))
    elif is_vertical_match(board, MIN_PLAYER) or is_horizontal_match(board, MIN_PLAYER) or is_diognal_match(board,
                                                                                                            MIN_PLAYER):
        return State(deepcopy(board), MIN_PLAYER_UTILITY, deepcopy(state.moves))
    else:
        return State(deepcopy(board), DRAW_UTILITY, deepcopy(state.moves))


def is_valid_location(board, col):
    return board[board.shape[0] - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(board.shape[0]):
        if board[r][col] == 0:
            return r


def next_states(state: State, player):
    states = []
    for c in range(state.board.shape[1]):
        if is_valid_location(board=state.board, col=c):
            new_board = deepcopy(state.board)
            row = get_next_open_row(state.board, c)
            new_board[row][c] = player
            new_moves = deepcopy(state.moves)
            new_moves.append(c)
            states.append(State(deepcopy(new_board), state.score, new_moves))
    return states


def score_calculator(board):
    MAX_PLAYER_three_score = three_check(board, MAX_PLAYER)
    MAX_PLAYER_two_score = two_check(board, MAX_PLAYER)

    MIN_PLAYER_three_score = three_check(board, MIN_PLAYER)
    MIN_PLAYER_two_score = two_check(board, MIN_PLAYER)

    score = MAX_PLAYER_two_score + 10 * MAX_PLAYER_three_score - (10 * MIN_PLAYER_three_score + MIN_PLAYER_two_score)
    return score


def three_check(board, player):
    count_of_threes = 0
    for r in range(board.shape[0] - 1):
        for c in range(board.shape[1] - 1):
            if c < board.shape[1] - 3:
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == player and board[r][c + 3] == 0:
                    count_of_threes += 1
                if r < board.shape[0] - 3:
                    if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == player and board[r + 3][c + 3] == 0:
                        count_of_threes += 1
            if c >= 3:
                if board[r][c] == board[r][c - 1] == board[r][c - 2] == player and board[r][c - 3] == 0:
                    count_of_threes += 1
                if r < board.shape[0] - 3:
                    if board[r][c] == board[r + 1][c - 1] == board[r + 2][c - 2] == player and board[r + 3][c - 3] == 0:
                        count_of_threes += 1

            if r < board.shape[0] - 3:
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == player and board[r + 3][c] == 0:
                    count_of_threes += 1
    return count_of_threes


def two_check(board, player):
    count_of_twos = 0
    for r in range(board.shape[0] - 1):
        for c in range(board.shape[1] - 1):
            if c < board.shape[1] - 3:
                if board[r][c] == board[r][c + 1] == player and board[r][c + 2] == board[r][c + 3] == 0:
                    count_of_twos += 1
                if r < board.shape[0] - 3:
                    if board[r][c] == board[r + 1][c + 1] == player and board[r + 2][c + 2] == board[r + 3][c + 3] == 0:
                        count_of_twos += 1
            if c >= 3:
                if board[r][c] == board[r][c - 1] == player and board[r][c - 2] == board[r][c - 3] == 0:
                    count_of_twos += 1
                if r < board.shape[0] - 3:
                    if board[r][c] == board[r + 1][c - 1] == player and board[r + 2][c - 2] == board[r + 3][c - 3] == 0:
                        count_of_twos += 1

            if r < board.shape[0] - 3:
                if board[r][c] == board[r + 1][c] == player and board[r + 2][c] == board[r + 3][c] == 0:
                    count_of_twos += 1
    return count_of_twos


def get_next_move(root):
    start_time = time.time()
    final_state = alpha_beta_search(root, depth=5)
    end_time = time.time()
    print('took:', end_time - start_time, 'ns')
    print('predicted final score:', final_state.score)
    print('predicted final board:\n', np.flip(final_state.board, 0))
    print('moves to reach final board:', final_state.moves)

    if len(final_state.moves) > 0:
        return final_state.moves[0]

    else:
        return 'finished!'
