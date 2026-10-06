import unittest

import numpy as np

from connect_four.board import (
    PLAYER_ONE,
    PLAYER_TWO,
    copy_with_move,
    create_board,
    drop_piece,
    get_next_open_row,
    get_ordered_valid_moves,
    get_valid_moves,
    is_draw,
    is_valid_move,
    is_winning_move,
    other_player,
)
from connect_four.config import GameConfig


class BoardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = GameConfig(rows=6, columns=7, connect=4)
        self.board = create_board(self.config)

    def test_board_dimensions_are_configurable(self) -> None:
        config = GameConfig(rows=8, columns=9, connect=5)
        board = create_board(config)
        self.assertEqual((8, 9), board.shape)

    def test_piece_falls_to_lowest_open_row(self) -> None:
        first_row = drop_piece(self.board, 3, PLAYER_ONE)
        second_row = drop_piece(self.board, 3, PLAYER_TWO)
        self.assertEqual(0, first_row)
        self.assertEqual(1, second_row)

    def test_full_column_is_rejected(self) -> None:
        for row in range(self.config.rows):
            drop_piece(self.board, 0, PLAYER_ONE if row % 2 == 0 else PLAYER_TWO)

        self.assertFalse(is_valid_move(self.board, 0))
        self.assertIsNone(get_next_open_row(self.board, 0))
        with self.assertRaises(ValueError):
            drop_piece(self.board, 0, PLAYER_ONE)

    def test_out_of_range_columns_are_rejected_safely(self) -> None:
        for column in (-1, self.config.columns):
            with self.subTest(column=column):
                self.assertFalse(is_valid_move(self.board, column))
                self.assertIsNone(get_next_open_row(self.board, column))
                with self.assertRaises(ValueError):
                    drop_piece(self.board, column, PLAYER_ONE)

    def test_invalid_player_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            drop_piece(self.board, 0, 3)

    def test_other_player_validates_input(self) -> None:
        self.assertEqual(PLAYER_TWO, other_player(PLAYER_ONE))
        self.assertEqual(PLAYER_ONE, other_player(PLAYER_TWO))
        with self.assertRaises(ValueError):
            other_player(0)

    def test_valid_moves(self) -> None:
        self.assertEqual(list(range(7)), get_valid_moves(self.board))

    def test_center_first_ordering_on_odd_width_board(self) -> None:
        self.assertEqual([3, 2, 4, 1, 5, 0, 6], get_ordered_valid_moves(self.board))

    def test_center_first_ordering_on_even_width_board(self) -> None:
        config = GameConfig(rows=6, columns=6, connect=4)
        board = create_board(config)

        self.assertEqual([2, 3, 1, 4, 0, 5], get_ordered_valid_moves(board))

    def test_copy_with_move_does_not_mutate_original(self) -> None:
        copied = copy_with_move(self.board, 3, PLAYER_ONE)

        self.assertTrue(np.all(self.board == 0))
        self.assertEqual(PLAYER_ONE, copied[0, 3])
        self.assertFalse(np.shares_memory(self.board, copied))

    def test_horizontal_win(self) -> None:
        for column in range(4):
            drop_piece(self.board, column, PLAYER_ONE)
        self.assertTrue(is_winning_move(self.board, PLAYER_ONE, 4))

    def test_vertical_win(self) -> None:
        for _ in range(4):
            drop_piece(self.board, 2, PLAYER_TWO)
        self.assertTrue(is_winning_move(self.board, PLAYER_TWO, 4))

    def test_rising_diagonal_win(self) -> None:
        # Build PLAYER_ONE at (0,0), (1,1), (2,2), (3,3).
        drop_piece(self.board, 0, PLAYER_ONE)

        drop_piece(self.board, 1, PLAYER_TWO)
        drop_piece(self.board, 1, PLAYER_ONE)

        drop_piece(self.board, 2, PLAYER_TWO)
        drop_piece(self.board, 2, PLAYER_TWO)
        drop_piece(self.board, 2, PLAYER_ONE)

        drop_piece(self.board, 3, PLAYER_TWO)
        drop_piece(self.board, 3, PLAYER_TWO)
        drop_piece(self.board, 3, PLAYER_TWO)
        drop_piece(self.board, 3, PLAYER_ONE)

        self.assertTrue(is_winning_move(self.board, PLAYER_ONE, 4))

    def test_falling_diagonal_win(self) -> None:
        # Build PLAYER_ONE at (3,0), (2,1), (1,2), (0,3).
        for _ in range(3):
            drop_piece(self.board, 0, PLAYER_TWO)
        drop_piece(self.board, 0, PLAYER_ONE)

        for _ in range(2):
            drop_piece(self.board, 1, PLAYER_TWO)
        drop_piece(self.board, 1, PLAYER_ONE)

        drop_piece(self.board, 2, PLAYER_TWO)
        drop_piece(self.board, 2, PLAYER_ONE)

        drop_piece(self.board, 3, PLAYER_ONE)

        self.assertTrue(is_winning_move(self.board, PLAYER_ONE, 4))

    def test_connect_length_is_dynamic(self) -> None:
        config = GameConfig(rows=8, columns=9, connect=5)
        board = create_board(config)
        for column in range(5):
            drop_piece(board, column, PLAYER_ONE)

        self.assertTrue(is_winning_move(board, PLAYER_ONE, config.connect))
        self.assertFalse(is_winning_move(board, PLAYER_TWO, config.connect))

    def test_draw_detection(self) -> None:
        # A 2x3 connect-3 position with no three-in-a-row for either player.
        config = GameConfig(rows=2, columns=3, connect=3)
        board = np.array(
            [
                [PLAYER_ONE, PLAYER_TWO, PLAYER_ONE],
                [PLAYER_TWO, PLAYER_ONE, PLAYER_TWO],
            ],
            dtype=np.int8,
        )
        self.assertTrue(is_draw(board, config.connect))


if __name__ == "__main__":
    unittest.main()
