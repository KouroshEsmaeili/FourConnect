import copy
import random

import pygame
import MiniMax
import numpy as np
import sys
import math

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

HEIGHT = 6
LENGTH = 7
HUMAN = 1
AI = 2


def Create_board():
    board = np.zeros((HEIGHT, LENGTH))
    return board


def Drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[HEIGHT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(HEIGHT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print("_________________________")
    # print(board)
    print(np.flip(board, 0))
    # print(board[0][1])
    print("_________________________")


def winning_move(board, piece):
    for c in range(LENGTH - 3):
        for r in range(HEIGHT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True
    for c in range(LENGTH):
        for r in range(HEIGHT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    for c in range(LENGTH - 3):
        for r in range(HEIGHT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    for c in range(LENGTH - 3):
        for r in range(3, HEIGHT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def draw_board(board):
    for c in range(LENGTH):
        for r in range(HEIGHT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(LENGTH):
        for r in range(HEIGHT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, WHITE, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def score_calculator(board):
    AI_three_score = three_check(board, AI)
    AI_two_score = two_check(board, AI)

    HUMAN_three_score = three_check(board, HUMAN)
    HUMAN_two_score = two_check(board, HUMAN)

    score = AI_two_score + 10*AI_three_score - (10*HUMAN_three_score + HUMAN_two_score)
    return score


def three_check(board, player):
    count_of_threes = 0
    for r in range(HEIGHT - 1):
        for c in range(LENGTH - 1):
            if c < LENGTH - 3:
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == player and board[r][c + 3] == 0:
                    count_of_threes += 1
                if r < HEIGHT - 3:
                    if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == player and board[r + 3][c + 3] == 0:
                        count_of_threes += 1
            if c >= 3:
                if board[r][c] == board[r][c - 1] == board[r][c - 2] == player and board[r][c - 3] == 0:
                    count_of_threes += 1
                if r < HEIGHT - 3:
                    if board[r][c] == board[r + 1][c - 1] == board[r + 2][c - 2] == player and board[r + 3][c - 3] == 0:
                        count_of_threes += 1

            if r < HEIGHT - 3:
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == player and board[r + 3][c] == 0:
                    count_of_threes += 1
    return count_of_threes


def two_check(board, player):
    count_of_twos = 0
    for r in range(HEIGHT - 1):
        for c in range(LENGTH - 1):
            if c < LENGTH - 3:
                if board[r][c] == board[r][c + 1] == player and board[r][c + 2] == board[r][c + 3] == 0:
                    count_of_twos += 1
                if r < HEIGHT - 3:
                    if board[r][c] == board[r + 1][c + 1] == player and board[r + 2][c + 2] == board[r + 3][c + 3] == 0:
                        count_of_twos += 1
            if c >= 3:
                if board[r][c] == board[r][c - 1] == player and board[r][c - 2] == board[r][c - 3] == 0:
                    count_of_twos += 1
                if r < HEIGHT - 3:
                    if board[r][c] == board[r + 1][c - 1] == player and board[r + 2][c - 2] == board[r + 3][c - 3] == 0:
                        count_of_twos += 1

            if r < HEIGHT - 3:
                if board[r][c] == board[r + 1][c] == player and board[r + 2][c] == board[r + 3][c] == 0:
                    count_of_twos += 1
    return count_of_twos


def find_bestMove(board, player):
    playable_moves = find_playable_locations(board)
    best_score = float("-inf")
    best_col = random.choice(playable_moves)
    for col in playable_moves:
        row = get_next_open_row(board, col)
        temp_board = copy.deepcopy(board)
        Drop_piece(temp_board, row, col, player)
        if winning_move(temp_board, AI):
            score = 1000000
        else:
            score = score_calculator(temp_board)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def find_playable_locations(board):
    playable_locations = []
    for col in range(LENGTH):
        if is_valid_location(board, col):
            playable_locations.append(col)
    return playable_locations


def my_MiniMax(board, alpha, beta, depth, maximizingPlayer):
    playable_locations = find_playable_locations(board)
    is_terminal_state, winner = we_have_match(board)
    if (depth == 0) or is_terminal_state:
        if is_terminal_state:
            if winner == AI:
                return (None, 1000000)
            if winner == HUMAN:
                return (None, -1000000)
            else:
                return (None, 0)
        else:
            return (None, score_calculator(board))
    if maximizingPlayer:
        value = float("-inf")
        column = random.choice(playable_locations)
        for col in playable_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            Drop_piece(temp_board, row, col, AI)
            new_score = my_MiniMax(temp_board, alpha, beta, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = float("inf")
        column = random.choice(playable_locations)
        for col in playable_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            Drop_piece(temp_board, row, col, AI)
            new_score = my_MiniMax(temp_board, alpha, beta, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col

            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def we_have_match(board):
    if (is_vertical_match(board, AI)) or (is_horizontal_match(board, AI)) or (is_diognal_match(board, AI)):
        return True, AI

    if (is_vertical_match(board, HUMAN)) or (is_horizontal_match(board, HUMAN)) or (is_diognal_match(board, HUMAN)):
        return True, HUMAN

    if is_all_full(board):
        return True, 0

    return False, None


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


board = Create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100
width = LENGTH * SQUARESIZE
height = (HEIGHT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, WHITE, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            print_board(board)
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    Drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = font.render("Player 1 wins!!", True, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn = turn % 2

            else:
                col = find_bestMove(board, AI)
                print(col)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    Drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = font.render("Player 2 wins!!", True, WHITE)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn = turn % 2

            draw_board(board)

            if game_over:
                pygame.time.wait(3000)
