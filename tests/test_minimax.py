import unittest

from connect_four.board import PLAYER_ONE, PLAYER_TWO, create_board, drop_piece
from connect_four.config import GameConfig
from connect_four.minimax import WIN_UTILITY, alpha_beta_search


class MinimaxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = GameConfig()

    def test_player_one_takes_immediate_win(self) -> None:
        board = create_board(self.config)
        for column in range(3):
            drop_piece(board, column, PLAYER_ONE)

        result = alpha_beta_search(board, depth=3, player=PLAYER_ONE, connect=4)
        self.assertEqual(3, result.column)
        self.assertGreaterEqual(result.score, WIN_UTILITY)

    def test_player_two_takes_immediate_win(self) -> None:
        board = create_board(self.config)
        for column in range(3):
            drop_piece(board, column, PLAYER_TWO)

        result = alpha_beta_search(board, depth=3, player=PLAYER_TWO, connect=4)
        self.assertEqual(3, result.column)
        self.assertGreaterEqual(result.score, WIN_UTILITY)

    def test_player_two_blocks_immediate_loss(self) -> None:
        board = create_board(self.config)
        for column in range(3):
            drop_piece(board, column, PLAYER_ONE)

        result = alpha_beta_search(board, depth=2, player=PLAYER_TWO, connect=4)
        self.assertEqual(3, result.column)

    def test_search_returns_legal_move(self) -> None:
        board = create_board(self.config)
        for row in range(self.config.rows):
            drop_piece(board, 3, PLAYER_ONE if row % 2 == 0 else PLAYER_TWO)

        result = alpha_beta_search(board, depth=2, player=PLAYER_ONE, connect=4)
        self.assertIsNotNone(result.column)
        self.assertNotEqual(3, result.column)

    def test_terminal_board_returns_no_move(self) -> None:
        board = create_board(self.config)
        for column in range(4):
            drop_piece(board, column, PLAYER_ONE)

        result = alpha_beta_search(board, depth=3, player=PLAYER_TWO, connect=4)
        self.assertIsNone(result.column)
        self.assertLessEqual(result.score, -WIN_UTILITY)

    def test_dynamic_board_search(self) -> None:
        config = GameConfig(rows=5, columns=6, connect=4)
        board = create_board(config)
        for column in range(3):
            drop_piece(board, column, PLAYER_ONE)

        result = alpha_beta_search(
            board,
            depth=2,
            player=PLAYER_ONE,
            connect=config.connect,
        )
        self.assertEqual(3, result.column)


if __name__ == "__main__":
    unittest.main()
