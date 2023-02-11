import copy

import numpy as np


class Heuristic:
    def __init__(self, board: np.array):
        self.board: np.array = board
        self.score = 0

    def find_horizontal(self, length: int, player: int):  # Checked
        count_one_blank = 0
        count_two_blank = 0
        for i in range(len(self.board)):
            num_count = 0
            for j in range(len(self.board[i])):
                if self.board[i][j] == player:
                    num_count += 1
                else:
                    num_count = 0
                if num_count == length:
                    if j + 1 < len(self.board[i]) and j - length >= 0:
                        if self.board[i][j + 1] == 0 and self.board[i][j - length] == 0:
                            count_two_blank += 1
                        elif self.board[i][j + 1] == 0 and self.board[i][j - length] != 0 and self.board[i][
                            j - length] != player:
                            count_one_blank += 1
                        elif self.board[i][j + 1] != 0 and self.board[i][j - length] == 0 and self.board[i][
                            j + 1] != player:
                            count_one_blank += 1
                    elif j + 1 < len(self.board[i]):
                        if self.board[i][j + 1] == 0:
                            count_one_blank += 1
                    elif j - length >= 0:
                        if self.board[i][j - length] == 0:
                            count_one_blank += 1
                    num_count = 0
        return count_one_blank, count_two_blank

    def find_vertical(self, length: int, player: int):  # Checked
        count_one_blank = 0
        count_two_blank = 0
        transpose_board = copy.deepcopy(self.board.transpose())
        for i in range(len(transpose_board)):
            num_count = 0
            for j in range(len(transpose_board[i])):
                if transpose_board[i][j] == player:
                    num_count += 1
                else:
                    num_count = 0
                if num_count == length:
                    if j + 1 < len(transpose_board[i]) and j - length >= 0:
                        if transpose_board[i][j + 1] == 0 and transpose_board[i][j - length] == 0:
                            count_two_blank += 1
                        elif transpose_board[i][j + 1] == 0 and transpose_board[i][j - length] != 0 and \
                                transpose_board[i][j - length] != player:
                            count_one_blank += 1
                        elif transpose_board[i][j + 1] != 0 and transpose_board[i][j - length] == 0 and \
                                transpose_board[i][j + 1] != player:
                            count_one_blank += 1
                    elif j + 1 < len(transpose_board[i]):
                        if transpose_board[i][j + 1] == 0:
                            count_one_blank += 1
                    elif j - length >= 0:
                        if transpose_board[i][j - length] == 0:
                            count_one_blank += 1
                    num_count = 0
        return count_one_blank, count_two_blank

    def diagonal(self, length: int, player: int):  # Checked
        diagonal_axes_main: list = []
        diagonal_axes_rot: list = []
        diagonal_axes: list = []
        transpose_board = np.rot90(self.board, k=3, axes=(0, 1))
        m = len(self.board)
        n = len(self.board[0])

        # Making proper diagonals ready to check

        for i in range(-m, n):
            try:
                temp = np.diag(self.board, i)
                diagonal_axes_main.append(temp)
            except:
                pass
        for i in range(-n, m):
            try:
                temp = np.diag(transpose_board, i)
                diagonal_axes_rot.append(temp)
            except:
                pass
        for i in range(3):
            diagonal_axes_main.pop(0)
            diagonal_axes_rot.pop(0)
        for i in range(2):
            diagonal_axes_main.pop(-1)
            diagonal_axes_rot.pop(-1)
        diagonal_axes.extend(diagonal_axes_main)
        diagonal_axes.extend(diagonal_axes_rot)

        # Finding diagonal connects

        count_one_blank = 0
        count_two_blank = 0
        for i in range(len(diagonal_axes)):
            num_count = 0
            for j in range(len(diagonal_axes[i])):
                if diagonal_axes[i][j] == player:
                    num_count += 1
                else:
                    num_count = 0
                if num_count == length:
                    if j + 1 < len(diagonal_axes[i]) and j - length >= 0:
                        if diagonal_axes[i][j + 1] == 0 and diagonal_axes[i][j - length] == 0:
                            count_two_blank += 1
                        elif diagonal_axes[i][j + 1] == 0 and diagonal_axes[i][j - length] != 0 and diagonal_axes[i][
                            j - length] != player:
                            count_one_blank += 1
                        elif diagonal_axes[i][j + 1] != 0 and diagonal_axes[i][j - length] == 0 and diagonal_axes[i][
                            j + 1] != player:
                            count_one_blank += 1
                    elif j + 1 < len(diagonal_axes[i]):
                        if diagonal_axes[i][j + 1] == 0:
                            count_one_blank += 1
                    elif j - length >= 0:
                        if diagonal_axes[i][j - length] == 0:
                            count_one_blank += 1
                    num_count = 0
        return count_one_blank, count_two_blank
