"""Command-line interface for launching Connect Four."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .config import GameConfig

MODE_CHOICES = ("hh", "hai", "aih", "aiai")


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser without initializing Pygame."""
    parser = argparse.ArgumentParser(
        description="Connect Four with heuristic minimax and alpha-beta pruning."
    )
    parser.add_argument(
        "--mode",
        choices=MODE_CHOICES,
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
    return parser


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments, optionally from an explicit sequence."""
    return create_parser().parse_args(args)


def main(args: Sequence[str] | None = None) -> None:
    """Launch the configured Pygame application."""
    parsed = parse_args(args)

    # Importing the graphical application only after parsing keeps --help usable
    # in headless environments without initializing Pygame.
    from .app import MODES, ConnectFourApp

    config = GameConfig(
        rows=parsed.rows,
        columns=parsed.columns,
        connect=parsed.connect,
    )
    app = ConnectFourApp(
        config=config,
        mode=MODES[parsed.mode],
        player_one_depth=parsed.depth1,
        player_two_depth=parsed.depth2,
        cell_size=parsed.cell_size,
        ai_delay_seconds=parsed.ai_delay,
    )
    app.run()


if __name__ == "__main__":
    main()
