from __future__ import annotations

from dataclasses import dataclass
from math import inf
from time import perf_counter

from .board import (
    Board,
    copy_with_move,
    get_ordered_valid_moves,
    is_full,
    is_winning_move,
    other_player,
)
from .heuristic import HeuristicWeights, evaluate_board

WIN_UTILITY = 1_000_000
DRAW_UTILITY = 0


@dataclass
class SearchStats:
    nodes_evaluated: int = 0
    alpha_beta_cutoffs: int = 0


@dataclass
class NodeResult:
    score: float
    principal_variation: list[int]


@dataclass
class SearchResult:
    column: int | None
    score: float
    principal_variation: list[int]
    depth: int
    nodes_evaluated: int
    alpha_beta_cutoffs: int
    elapsed_seconds: float


def _terminal_score(
    board: Board,
    maximizing_player: int,
    connect: int,
    remaining_depth: int,
) -> float | None:
    minimizing_player = other_player(maximizing_player)

    if is_winning_move(board, maximizing_player, connect):
        # The depth bonus prefers faster wins.
        return float(WIN_UTILITY + remaining_depth)

    if is_winning_move(board, minimizing_player, connect):
        # The depth penalty prefers delaying unavoidable losses.
        return float(-WIN_UTILITY - remaining_depth)

    if is_full(board):
        return float(DRAW_UTILITY)

    return None


def max_value(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: int,
    connect: int,
    stats: SearchStats,
    weights: HeuristicWeights,
) -> NodeResult:
    stats.nodes_evaluated += 1

    terminal_score = _terminal_score(
        board, maximizing_player, connect, remaining_depth=depth
    )
    if terminal_score is not None:
        return NodeResult(terminal_score, [])

    if depth == 0:
        return NodeResult(
            evaluate_board(board, maximizing_player, connect, weights),
            [],
        )

    best = NodeResult(-inf, [])
    for column in get_ordered_valid_moves(board):
        next_board = copy_with_move(board, column, maximizing_player)
        child = min_value(
            next_board,
            depth - 1,
            alpha,
            beta,
            maximizing_player,
            connect,
            stats,
            weights,
        )

        if child.score > best.score:
            best = NodeResult(child.score, [column, *child.principal_variation])

        if best.score >= beta:
            stats.alpha_beta_cutoffs += 1
            return best

        alpha = max(alpha, best.score)

    return best


def min_value(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: int,
    connect: int,
    stats: SearchStats,
    weights: HeuristicWeights,
) -> NodeResult:
    stats.nodes_evaluated += 1

    terminal_score = _terminal_score(
        board, maximizing_player, connect, remaining_depth=depth
    )
    if terminal_score is not None:
        return NodeResult(terminal_score, [])

    if depth == 0:
        return NodeResult(
            evaluate_board(board, maximizing_player, connect, weights),
            [],
        )

    minimizing_player = other_player(maximizing_player)
    best = NodeResult(inf, [])

    for column in get_ordered_valid_moves(board):
        next_board = copy_with_move(board, column, minimizing_player)
        child = max_value(
            next_board,
            depth - 1,
            alpha,
            beta,
            maximizing_player,
            connect,
            stats,
            weights,
        )

        if child.score < best.score:
            best = NodeResult(child.score, [column, *child.principal_variation])

        if best.score <= alpha:
            stats.alpha_beta_cutoffs += 1
            return best

        beta = min(beta, best.score)

    return best


def alpha_beta_search(
    board: Board,
    depth: int,
    player: int,
    connect: int,
    weights: HeuristicWeights | None = None,
) -> SearchResult:
    """Choose a move using depth-limited minimax with alpha-beta pruning."""
    if depth < 1:
        raise ValueError("depth must be at least 1")

    weights = weights or HeuristicWeights()
    stats = SearchStats()
    start = perf_counter()

    terminal_score = _terminal_score(
        board, player, connect, remaining_depth=depth
    )
    if terminal_score is not None:
        elapsed = perf_counter() - start
        stats.nodes_evaluated += 1
        return SearchResult(
            column=None,
            score=terminal_score,
            principal_variation=[],
            depth=depth,
            nodes_evaluated=stats.nodes_evaluated,
            alpha_beta_cutoffs=stats.alpha_beta_cutoffs,
            elapsed_seconds=elapsed,
        )

    # Root search is kept explicit so the returned column always corresponds to
    # the current player's move, while max_value/min_value remain easy to read.
    best = NodeResult(-inf, [])
    alpha = -inf
    beta = inf
    stats.nodes_evaluated += 1

    for column in get_ordered_valid_moves(board):
        next_board = copy_with_move(board, column, player)
        child = min_value(
            next_board,
            depth - 1,
            alpha,
            beta,
            player,
            connect,
            stats,
            weights,
        )

        if child.score > best.score:
            best = NodeResult(child.score, [column, *child.principal_variation])

        alpha = max(alpha, best.score)

    elapsed = perf_counter() - start
    best_column = best.principal_variation[0] if best.principal_variation else None

    return SearchResult(
        column=best_column,
        score=best.score,
        principal_variation=best.principal_variation,
        depth=depth,
        nodes_evaluated=stats.nodes_evaluated,
        alpha_beta_cutoffs=stats.alpha_beta_cutoffs,
        elapsed_seconds=elapsed,
    )
