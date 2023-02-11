import pygame
import numpy as np
import sys
import math
import MiniMax

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

HEIGHT = 6
LENGTH = 7


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
    print(np.flip(board, 0))
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
                col = MiniMax.get_next_move(root=board, depth=5, player=2)
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
