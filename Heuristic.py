import copy

import numpy as np


class Heuristic:
    def __init__(self, board: np.array):
        self.board: np.array = board
        self.rewards = {'four_connect': 2000, 'three_connect_two_blanks': 400, 'three_connect_one_blank': 50,
                        'two_connect_two_blanks': 10, 'two_connect_one_blank': 5}

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

    def find_diagonal(self, length: int, player: int):  # Checked
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

    def get_score_player(self, player: int):
        # When its 4 it doesn't matter that it is one blank or two blanks but we used the same functions
        four_connect_one_blank_H, four_connect_two_blanks_H = self.find_horizontal(4, player)
        four_connect_one_blank_V, four_connect_two_blank_V = self.find_vertical(4, player)
        four_connect_one_blank_D, four_connect_two_blank_D = self.find_diagonal(4, player)
        three_connect_one_blank_H, three_connect_two_blanks_H = self.find_horizontal(3, player)
        three_connect_one_blank_V, three_connect_two_blanks_V = self.find_vertical(3, player)
        three_connect_one_blank_D, three_connect_two_blanks_D = self.find_diagonal(3, player)
        two_connect_one_blank_H, two_connect_two_blanks_H = self.find_horizontal(2, player)
        two_connect_one_blank_V, two_connect_two_blanks_V = self.find_vertical(2, player)
        two_connect_one_blank_D, two_connect_two_blanks_D = self.find_diagonal(2, player)
        four_connect = four_connect_one_blank_H + four_connect_two_blanks_H + four_connect_one_blank_V + \
                       four_connect_two_blank_V + four_connect_one_blank_D + four_connect_two_blank_D
        three_connect_two_blanks = three_connect_two_blanks_H + three_connect_two_blanks_V + three_connect_two_blanks_D
        three_connect_one_blank = three_connect_one_blank_H + three_connect_one_blank_V + three_connect_one_blank_D
        two_connect_two_blanks = two_connect_two_blanks_H + two_connect_two_blanks_V + two_connect_two_blanks_D
        two_connect_one_blank = two_connect_one_blank_H + two_connect_one_blank_V + two_connect_one_blank_D
        score = self.rewards['four_connect'] * four_connect + self.rewards[
            'three_connect_two_blanks'] * three_connect_two_blanks + self.rewards[
                    'three_connect_one_blank'] * three_connect_one_blank + \
                self.rewards['two_connect_two_blanks'] * two_connect_two_blanks + self.rewards[
                    'two_connect_one_blank'] * two_connect_one_blank
        return score

    def get_score(self, player):
        opponent = 0
        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1
        else:
            raise Exception('No Such Player')  # Designed to be two players game
        score = self.get_score_player(player) - self.get_score_player(opponent)
        return score
