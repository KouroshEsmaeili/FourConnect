import unittest

from connect_four.config import GameConfig


class GameConfigTests(unittest.TestCase):
    def test_zero_and_negative_rows_are_rejected(self) -> None:
        for rows in (0, -1):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                GameConfig(rows=rows)

    def test_zero_and_negative_columns_are_rejected(self) -> None:
        for columns in (0, -1):
            with self.subTest(columns=columns), self.assertRaises(ValueError):
                GameConfig(columns=columns)

    def test_connect_below_two_is_rejected(self) -> None:
        for connect in (0, 1, -1):
            with self.subTest(connect=connect), self.assertRaises(ValueError):
                GameConfig(connect=connect)

    def test_impossible_connect_length_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            GameConfig(rows=4, columns=5, connect=6)

    def test_valid_non_standard_connect_n_is_accepted(self) -> None:
        config = GameConfig(rows=8, columns=9, connect=5)

        self.assertEqual((8, 9, 5), (config.rows, config.columns, config.connect))


if __name__ == "__main__":
    unittest.main()
