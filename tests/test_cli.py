import unittest

from connect_four.cli import parse_args


class CliTests(unittest.TestCase):
    def test_defaults(self) -> None:
        args = parse_args([])

        self.assertEqual("hai", args.mode)
        self.assertEqual((6, 7, 4), (args.rows, args.columns, args.connect))
        self.assertEqual((5, 5), (args.depth1, args.depth2))
        self.assertEqual(90, args.cell_size)
        self.assertEqual(0.35, args.ai_delay)

    def test_custom_connect_n_dimensions(self) -> None:
        args = parse_args(["--rows", "8", "--columns", "9", "--connect", "5"])

        self.assertEqual((8, 9, 5), (args.rows, args.columns, args.connect))

    def test_mode_and_depth_options(self) -> None:
        args = parse_args(["--mode", "aiai", "--depth1", "3", "--depth2", "6"])

        self.assertEqual("aiai", args.mode)
        self.assertEqual((3, 6), (args.depth1, args.depth2))


if __name__ == "__main__":
    unittest.main()
