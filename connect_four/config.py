from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    """Configuration for a Connect-N board.

    The default values describe standard Connect Four, while the engine itself
    supports other board dimensions and connection lengths.
    """

    rows: int = 6
    columns: int = 7
    connect: int = 4

    def __post_init__(self) -> None:
        if self.rows <= 0:
            raise ValueError("rows must be positive")
        if self.columns <= 0:
            raise ValueError("columns must be positive")
        if self.connect < 2:
            raise ValueError("connect must be at least 2")
        if self.connect > max(self.rows, self.columns):
            raise ValueError("connect cannot be larger than both board dimensions")
