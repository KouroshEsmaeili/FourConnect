from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .board import Board, EMPTY, iter_windows, other_player


@dataclass(frozen=True)
class HeuristicWeights:
    """Weights for the hand-designed board evaluation function.

    Pattern values grow exponentially with the number of pieces in a potential
    connection. This preserves the original project's idea of valuing twos and
    threes more strongly while generalizing to Connect-N boards.
    """

    pattern_base: int = 10
    center_weight: int = 3
    opponent_threat_multiplier: float = 1.25


def _pattern_value(piece_count: int, base: int) -> int:
    if piece_count <= 0:
        return 0
    return base ** (piece_count - 1)


def score_window(
    window: np.ndarray,
    player: int,
    connect: int,
    weights: HeuristicWeights,
) -> float:
    """Score one connection-sized board window from *player*'s perspective."""
    opponent = other_player(player)
    player_count = int(np.count_nonzero(window == player))
    opponent_count = int(np.count_nonzero(window == opponent))
    empty_count = int(np.count_nonzero(window == EMPTY))

    # A mixed window cannot become a connection for either player unless pieces
    # are somehow removed, so it contributes no positional value.
    if player_count and opponent_count:
        return 0.0

    if player_count == connect:
        return float(_pattern_value(connect, weights.pattern_base))
    if opponent_count == connect:
        return -float(_pattern_value(connect, weights.pattern_base))

    if player_count > 0 and player_count + empty_count == connect:
        return float(_pattern_value(player_count, weights.pattern_base))

    if opponent_count > 0 and opponent_count + empty_count == connect:
        value = _pattern_value(opponent_count, weights.pattern_base)
        # Blocking an opponent's near-complete connection is slightly more
        # urgent than creating an equivalent pattern ourselves.
        if opponent_count == connect - 1:
            value *= weights.opponent_threat_multiplier
        return -float(value)

    return 0.0


def _center_control_score(
    board: Board,
    player: int,
    weights: HeuristicWeights,
) -> float:
    """Reward occupying columns close to the geometric center of the board."""
    opponent = other_player(player)
    center = (board.shape[1] - 1) / 2
    score = 0.0

    for column in range(board.shape[1]):
        # The closest center column(s) receive the largest contribution.
        distance = abs(column - center)
        positional_weight = max(0.0, (board.shape[1] / 2) - distance)

        player_count = int(np.count_nonzero(board[:, column] == player))
        opponent_count = int(np.count_nonzero(board[:, column] == opponent))
        score += (
            player_count - opponent_count
        ) * positional_weight * weights.center_weight

    return score


def evaluate_board(
    board: Board,
    player: int,
    connect: int,
    weights: HeuristicWeights | None = None,
) -> float:
    """Evaluate a non-terminal board from *player*'s perspective."""
    weights = weights or HeuristicWeights()

    score = _center_control_score(board, player, weights)
    for window in iter_windows(board, connect):
        score += score_window(window, player, connect, weights)

    return score
