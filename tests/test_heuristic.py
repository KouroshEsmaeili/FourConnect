import unittest

from connect_four.board import PLAYER_ONE, PLAYER_TWO, create_board, drop_piece
from connect_four.config import GameConfig
from connect_four.heuristic import evaluate_board


class HeuristicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = GameConfig()
        self.board = create_board(self.config)

    def test_empty_board_is_neutral(self) -> None:
        self.assertEqual(0.0, evaluate_board(self.board, PLAYER_ONE, 4))

    def test_two_in_a_row_improves_score(self) -> None:
        base = evaluate_board(self.board, PLAYER_ONE, 4)
        drop_piece(self.board, 2, PLAYER_ONE)
        drop_piece(self.board, 3, PLAYER_ONE)
        self.assertGreater(evaluate_board(self.board, PLAYER_ONE, 4), base)

    def test_opponent_threat_reduces_score(self) -> None:
        for column in range(3):
            drop_piece(self.board, column, PLAYER_TWO)
        self.assertLess(evaluate_board(self.board, PLAYER_ONE, 4), 0)

    def test_top_row_patterns_are_evaluated(self) -> None:
        # This specifically protects against the old heuristic's top-row omission.
        for row in range(self.config.rows):
            drop_piece(self.board, 0, PLAYER_TWO if row < 5 else PLAYER_ONE)
            drop_piece(self.board, 1, PLAYER_TWO if row < 5 else PLAYER_ONE)

        self.assertNotEqual(0.0, evaluate_board(self.board, PLAYER_ONE, 4))


if __name__ == "__main__":
    unittest.main()
