from __future__ import annotations

from collections.abc import Iterator

import numpy as np

from .config import GameConfig

EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
PLAYERS = (PLAYER_ONE, PLAYER_TWO)

Board = np.ndarray


def create_board(config: GameConfig) -> Board:
    """Create an empty board using the configured dimensions."""
    return np.zeros((config.rows, config.columns), dtype=np.int8)


def other_player(player: int) -> int:
    if player == PLAYER_ONE:
        return PLAYER_TWO
    if player == PLAYER_TWO:
        return PLAYER_ONE
    raise ValueError(f"invalid player: {player}")


def is_valid_move(board: Board, column: int) -> bool:
    """Return True when a piece can legally be dropped into *column*."""
    if column < 0 or column >= board.shape[1]:
        return False
    return bool(board[-1, column] == EMPTY)


def get_next_open_row(board: Board, column: int) -> int | None:
    """Return the lowest empty row in a column, or None when it is full."""
    if column < 0 or column >= board.shape[1]:
        return None

    for row in range(board.shape[0]):
        if board[row, column] == EMPTY:
            return row
    return None


def drop_piece(board: Board, column: int, player: int) -> int:
    """Drop *player*'s piece into *column* and return the occupied row.

    The board is modified in place. A ValueError is raised for an invalid
    player, out-of-range column, or full column.
    """
    if player not in PLAYERS:
        raise ValueError(f"invalid player: {player}")

    row = get_next_open_row(board, column)
    if row is None:
        raise ValueError(f"column {column} is full or out of range")

    board[row, column] = player
    return row


def get_valid_moves(board: Board) -> list[int]:
    return [
        column
        for column in range(board.shape[1])
        if is_valid_move(board, column)
    ]


def get_ordered_valid_moves(board: Board) -> list[int]:
    """Return legal moves ordered from the center outward.

    Center-first ordering does not change minimax correctness, but it usually
    improves alpha-beta pruning for Connect Four-like games.
    """
    center = (board.shape[1] - 1) / 2
    return sorted(get_valid_moves(board), key=lambda column: abs(column - center))


def iter_windows(board: Board, connect: int) -> Iterator[np.ndarray]:
    """Yield every horizontal, vertical, and diagonal window of length connect."""
    rows, columns = board.shape

    # Horizontal windows.
    for row in range(rows):
        for column in range(columns - connect + 1):
            yield board[row, column : column + connect]

    # Vertical windows.
    for column in range(columns):
        for row in range(rows - connect + 1):
            yield board[row : row + connect, column]

    # Rising diagonals: bottom-left -> top-right in the internal board layout.
    for row in range(rows - connect + 1):
        for column in range(columns - connect + 1):
            yield np.array(
                [board[row + offset, column + offset] for offset in range(connect)],
                dtype=board.dtype,
            )

    # Falling diagonals: top-left -> bottom-right visually.
    for row in range(connect - 1, rows):
        for column in range(columns - connect + 1):
            yield np.array(
                [board[row - offset, column + offset] for offset in range(connect)],
                dtype=board.dtype,
            )


def is_winning_move(board: Board, player: int, connect: int) -> bool:
    if player not in PLAYERS:
        raise ValueError(f"invalid player: {player}")

    return any(np.all(window == player) for window in iter_windows(board, connect))


def is_full(board: Board) -> bool:
    return not np.any(board == EMPTY)


def is_draw(board: Board, connect: int) -> bool:
    return (
        is_full(board)
        and not is_winning_move(board, PLAYER_ONE, connect)
        and not is_winning_move(board, PLAYER_TWO, connect)
    )


def copy_with_move(board: Board, column: int, player: int) -> Board:
    """Return a board copy with one legal move applied."""
    next_board = board.copy()
    drop_piece(next_board, column, player)
    return next_board


def format_board(board: Board) -> str:
    """Return a terminal-friendly board view with the top row printed first."""
    return np.array2string(np.flip(board, axis=0))
