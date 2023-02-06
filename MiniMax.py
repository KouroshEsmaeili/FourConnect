from copy import deepcopy
from json.encoder import INFINITY
import time

MAX_PLAYER = 'o'
MIN_PLAYER = 'x'
MAX_PLAYER_UTILITY = 1
MIN_PLAYER_UTILITY = -1
DRAW_UTILITY = 0
LENGTH = 6
HEIGHT = 7
root = [[], [], [], [], [], []]


class State:
    def __int__(self, board, score, moves):
        self.board = board
        self.score = score
        self.moves: list = moves

    def cell_is_full(self, cell):
        if len(self.board[cell]) == HEIGHT:
            return True
        return False


def alpha_beta_search(root):
    root_state = State(deepcopy(root), 0, [])
    return max_value(root_state, -INFINITY, INFINITY)


def max_value(state: State, alpha, beta):
    if terminal_test(state):
        return utility(state)

    v = State(board=deepcopy(root), score=-INFINITY, moves=[])
    for next_state in next_states(state, MAX_PLAYER):
        v = get_max_state(v, min_value(next_state, alpha, beta))
        if v.score >= beta:
            return v
        alpha = max(alpha, v.score)

    return v


def min_value(state: State, alpha, beta):
    if terminal_test(state):
        return utility(state)

    v = State(board=deepcopy(root), score=INFINITY, moves=[])
    for next_state in next_states(state, MIN_PLAYER):
        v = get_min_state(v, max_value(next_state, alpha, beta))
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
        if len(cell) != HEIGHT:
            return False
    return True


def is_vertical_match(board, player):
    for i in range(LENGTH):
        for j in range(HEIGHT - 3):
            if (board[i][j] == player and board[i][j + 1] == player and board[i][j + 2] == player and board[i][
                j + 3] == player):
                return True
    return False


def is_horizontal_match(board, player):
    for i in range(HEIGHT):
        for j in range(LENGTH - 3):
            if (board[j][i] == player and board[j + 1][i] == player and board[j + 2][i] == player and board[j + 3][
                i] == player):
                return True
    return False


def is_diognal_match(board, player):
    for i in range(LENGTH):
        if i + 3 >= LENGTH:
            continue
        for j in range(HEIGHT):
            if j + 3 >= HEIGHT:
                continue
            if (board[i][j] == player and board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and
                    board[i + 3][j + 3] == player):
                return True
    for i in range(LENGTH):
        if i - 3 <= 0:
            continue
        for j in range(HEIGHT):
            if j + 3 >= HEIGHT:
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


def next_states(state: State, player):
    states = []
    for i, cell in enumerate(state.board):
        if not state.cell_is_full(cell=cell):
            new_board = deepcopy(state.board)
            for j in range(HEIGHT):
                if new_board[i][j] == '':
                    break
            new_board[i][j] = player
            new_moves = deepcopy(state.moves)
            new_moves.append(i)
            states.append(State(deepcopy(new_board), state.score, new_moves))
    return states


def get_next_move(root):
    start_time = time.time()
    final_state = alpha_beta_search(root)
    end_time = time.time()
    print('took:', end_time - start_time, 'ns')
    print('predicted final score:', final_state.score)
    print('predicted final board:', final_state.board)
    print('moves to reach final board:', final_state.moves)
    print()
    if len(final_state.moves) > 0:
        return final_state.moves[0] + 1
    else:
        return 'finished!'
