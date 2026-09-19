import argparse

from connect_four.app import MODES, ConnectFourApp
from connect_four.config import GameConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect Four with heuristic minimax and alpha-beta pruning."
    )
    parser.add_argument(
        "--mode",
        choices=sorted(MODES),
        default="hai",
        help="hh, hai, aih, or aiai (default: hai)",
    )
    parser.add_argument("--rows", type=int, default=6)
    parser.add_argument("--columns", type=int, default=7)
    parser.add_argument("--connect", type=int, default=4)
    parser.add_argument("--depth1", type=int, default=5)
    parser.add_argument("--depth2", type=int, default=5)
    parser.add_argument("--cell-size", type=int, default=90)
    parser.add_argument("--ai-delay", type=float, default=0.35)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GameConfig(
        rows=args.rows,
        columns=args.columns,
        connect=args.connect,
    )

    app = ConnectFourApp(
        config=config,
        mode=MODES[args.mode],
        player_one_depth=args.depth1,
        player_two_depth=args.depth2,
        cell_size=args.cell_size,
        ai_delay_seconds=args.ai_delay,
    )
    app.run()


if __name__ == "__main__":
    main()
