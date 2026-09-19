from __future__ import annotations

from dataclasses import dataclass

from .board import Board
from .heuristic import HeuristicWeights
from .minimax import SearchResult, alpha_beta_search


@dataclass
class MinimaxAgent:
    depth: int = 5
    weights: HeuristicWeights = HeuristicWeights()

    def choose_move(
        self,
        board: Board,
        player: int,
        connect: int,
    ) -> SearchResult:
        return alpha_beta_search(
            board=board,
            depth=self.depth,
            player=player,
            connect=connect,
            weights=self.weights,
        )
