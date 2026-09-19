from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import monotonic

import pygame

from .board import (
    PLAYER_ONE,
    PLAYER_TWO,
    create_board,
    drop_piece,
    is_full,
    is_valid_move,
    is_winning_move,
    other_player,
)
from .config import GameConfig
from .players import MinimaxAgent

# --- Color palette ---------------------------------------------------------

BG = (18, 22, 30)
PANEL_BG = (28, 34, 46)
FOOTER_BG = (24, 29, 40)

BOARD_BLUE = (54, 98, 180)
BOARD_BLUE_DARK = (41, 81, 154)

SLOT_BG = (10, 14, 22)
SLOT_RIM = (70, 110, 190)

PLAYER_ONE_COLOR = (232, 82, 88)    # red
PLAYER_TWO_COLOR = (244, 244, 248)  # white

TEXT = (240, 243, 248)
TEXT_MUTED = (171, 180, 196)

ACCENT = (255, 204, 64)             # gold
SUCCESS = (80, 200, 120)            # green
PREVIEW_ALPHA = 145
HOVER_ALPHA = 28
OVERLAY_ALPHA = 165


class Controller(str, Enum):
    HUMAN = "human"
    AI = "ai"


@dataclass(frozen=True)
class GameMode:
    player_one: Controller
    player_two: Controller


MODES = {
    "hh": GameMode(Controller.HUMAN, Controller.HUMAN),
    "hai": GameMode(Controller.HUMAN, Controller.AI),
    "aih": GameMode(Controller.AI, Controller.HUMAN),
    "aiai": GameMode(Controller.AI, Controller.AI),
}


class ConnectFourApp:
    def __init__(
        self,
        config: GameConfig,
        mode: GameMode,
        player_one_depth: int = 5,
        player_two_depth: int = 5,
        cell_size: int = 90,
        ai_delay_seconds: float = 0.35,
    ) -> None:
        pygame.init()

        self.config = config
        self.mode = mode
        self.cell_size = cell_size
        self.ai_delay_seconds = ai_delay_seconds

        self.top_bar_height = max(72, cell_size)
        self.footer_height = max(40, cell_size // 2)
        self.board_width = config.columns * cell_size
        self.board_height = config.rows * cell_size
        self.width = self.board_width
        self.height = self.top_bar_height + self.board_height + self.footer_height
        self.radius = max(8, cell_size // 2 - 8)

        self.board_top = self.top_bar_height
        self.board_bottom = self.board_top + self.board_height

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect Four — Minimax")

        self.title_font = pygame.font.SysFont("segoe ui", max(24, cell_size // 3), bold=True)
        self.font = pygame.font.SysFont("segoe ui", max(20, cell_size // 4))
        self.small_font = pygame.font.SysFont("segoe ui", max(16, cell_size // 6))

        self.clock = pygame.time.Clock()

        self.agents = {
            PLAYER_ONE: MinimaxAgent(depth=player_one_depth),
            PLAYER_TWO: MinimaxAgent(depth=player_two_depth),
        }

        self.board = create_board(config)
        self.current_player = PLAYER_ONE
        self.game_over = False
        self.message = ""
        self.hover_x: int | None = None
        self.last_move_time = monotonic()
        self.last_move: tuple[int, int] | None = None
        self.winning_cells: set[tuple[int, int]] = set()

    # ---------------------------------------------------------------------
    # Basic metadata / helpers
    # ---------------------------------------------------------------------

    def controller_for(self, player: int) -> Controller:
        return self.mode.player_one if player == PLAYER_ONE else self.mode.player_two

    def mode_label(self) -> str:
        labels = {
            (Controller.HUMAN, Controller.HUMAN): "Human vs Human",
            (Controller.HUMAN, Controller.AI): "Human vs AI",
            (Controller.AI, Controller.HUMAN): "AI vs Human",
            (Controller.AI, Controller.AI): "AI vs AI",
        }
        return labels[(self.mode.player_one, self.mode.player_two)]

    def player_color(self, player: int) -> tuple[int, int, int]:
        return PLAYER_ONE_COLOR if player == PLAYER_ONE else PLAYER_TWO_COLOR

    def player_name(self, player: int) -> str:
        return f"Player {player}"

    def reset(self) -> None:
        self.board = create_board(self.config)
        self.current_player = PLAYER_ONE
        self.game_over = False
        self.message = ""
        self.hover_x = None
        self.last_move_time = monotonic()
        self.last_move = None
        self.winning_cells = set()

    def board_position_to_screen_center(self, row: int, column: int) -> tuple[int, int]:
        x = column * self.cell_size + self.cell_size // 2
        y = self.board_bottom - row * self.cell_size - self.cell_size // 2
        return x, y

    def hovered_column(self) -> int | None:
        if self.hover_x is None:
            return None
        column = self.hover_x // self.cell_size
        if 0 <= column < self.config.columns:
            return column
        return None

    def find_winning_cells(self, player: int) -> set[tuple[int, int]]:
        connect = self.config.connect
        rows, columns = self.board.shape

        # Horizontal
        for row in range(rows):
            for col in range(columns - connect + 1):
                cells = [(row, col + offset) for offset in range(connect)]
                if all(int(self.board[r, c]) == player for r, c in cells):
                    return set(cells)

        # Vertical
        for col in range(columns):
            for row in range(rows - connect + 1):
                cells = [(row + offset, col) for offset in range(connect)]
                if all(int(self.board[r, c]) == player for r, c in cells):
                    return set(cells)

        # Rising diagonal
        for row in range(rows - connect + 1):
            for col in range(columns - connect + 1):
                cells = [(row + offset, col + offset) for offset in range(connect)]
                if all(int(self.board[r, c]) == player for r, c in cells):
                    return set(cells)

        # Falling diagonal
        for row in range(connect - 1, rows):
            for col in range(columns - connect + 1):
                cells = [(row - offset, col + offset) for offset in range(connect)]
                if all(int(self.board[r, c]) == player for r, c in cells):
                    return set(cells)

        return set()

    # ---------------------------------------------------------------------
    # Game actions
    # ---------------------------------------------------------------------

    def apply_move(self, column: int) -> None:
        if self.game_over or not is_valid_move(self.board, column):
            return

        player = self.current_player
        row = drop_piece(self.board, column, player)
        self.last_move = (row, column)

        if is_winning_move(self.board, player, self.config.connect):
            self.winning_cells = self.find_winning_cells(player)
            self.message = f"{self.player_name(player)} wins! Press R to restart"
            self.game_over = True
        elif is_full(self.board):
            self.message = "Draw! Press R to restart"
            self.game_over = True
        else:
            self.current_player = other_player(player)

        self.last_move_time = monotonic()

    def make_ai_move(self) -> None:
        if self.game_over:
            return

        if monotonic() - self.last_move_time < self.ai_delay_seconds:
            return

        player = self.current_player
        result = self.agents[player].choose_move(
            self.board,
            player=player,
            connect=self.config.connect,
        )

        print(
            f"Player {player} AI | depth={result.depth} | "
            f"move={result.column} | score={result.score:.2f} | "
            f"nodes={result.nodes_evaluated} | "
            f"cutoffs={result.alpha_beta_cutoffs} | "
            f"time={result.elapsed_seconds:.4f}s | "
            f"pv={result.principal_variation}"
        )

        if result.column is None:
            self.message = "Game finished — Press R to restart"
            self.game_over = True
            return

        self.apply_move(result.column)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_r:
                self.reset()
                return True

        if event.type == pygame.MOUSEMOTION:
            self.hover_x = event.pos[0]

        if self.game_over:
            return True

        if self.controller_for(self.current_player) != Controller.HUMAN:
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            column = event.pos[0] // self.cell_size
            self.apply_move(column)

        return True

    # ---------------------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------------------

    def draw_top_bar(self) -> None:
        pygame.draw.rect(
            self.screen,
            PANEL_BG,
            (0, 0, self.width, self.top_bar_height),
        )

        title = f"{self.mode_label()}   •   {self.config.rows}×{self.config.columns}   •   Connect {self.config.connect}"
        title_surface = self.title_font.render(title, True, TEXT)
        self.screen.blit(title_surface, (16, 10))

        if self.game_over:
            status_text = self.message
        else:
            controller = self.controller_for(self.current_player)
            if controller == Controller.AI:
                dots = "." * ((int(monotonic() * 3) % 3) + 1)
                depth = self.agents[self.current_player].depth
                status_text = (
                    f"{self.player_name(self.current_player)} (AI, depth={depth}) is thinking{dots}"
                )
            else:
                status_text = f"{self.player_name(self.current_player)} turn"

        status_surface = self.font.render(status_text, True, TEXT)
        self.screen.blit(status_surface, (16, self.top_bar_height - 34))

        help_surface = self.small_font.render("R: restart   •   ESC: quit", True, TEXT_MUTED)
        help_rect = help_surface.get_rect(topright=(self.width - 16, self.top_bar_height - 30))
        self.screen.blit(help_surface, help_rect)

        if not self.game_over:
            chip_radius = max(10, self.radius // 2)
            chip_x = self.width - 34
            chip_y = 24
            pygame.draw.circle(
                self.screen,
                self.player_color(self.current_player),
                (chip_x, chip_y),
                chip_radius,
            )
            pygame.draw.circle(
                self.screen,
                TEXT_MUTED,
                (chip_x, chip_y),
                chip_radius,
                2,
            )

    def draw_hover_preview(self) -> None:
        if self.game_over:
            return
        if self.controller_for(self.current_player) != Controller.HUMAN:
            return

        column = self.hovered_column()
        if column is None or not is_valid_move(self.board, column):
            return

        # Column highlight
        highlight = pygame.Surface((self.cell_size, self.board_height), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, HOVER_ALPHA))
        self.screen.blit(highlight, (column * self.cell_size, self.board_top))

        # Top preview piece
        preview_surface = pygame.Surface((self.cell_size, self.top_bar_height), pygame.SRCALPHA)
        color = self.player_color(self.current_player) + (PREVIEW_ALPHA,)
        pygame.draw.circle(
            preview_surface,
            color,
            (self.cell_size // 2, self.top_bar_height // 2),
            self.radius,
        )
        self.screen.blit(preview_surface, (column * self.cell_size, 0))

    def draw_board(self) -> None:
        board_rect = pygame.Rect(0, self.board_top, self.board_width, self.board_height)

        # Board background
        pygame.draw.rect(self.screen, BOARD_BLUE_DARK, board_rect)
        pygame.draw.rect(self.screen, BOARD_BLUE, board_rect.inflate(-6, -6), border_radius=8)

        # Empty slots
        for visual_row in range(self.config.rows):
            for column in range(self.config.columns):
                x = column * self.cell_size
                y = self.board_top + visual_row * self.cell_size
                center = (x + self.cell_size // 2, y + self.cell_size // 2)

                pygame.draw.circle(self.screen, SLOT_RIM, center, self.radius + 2)
                pygame.draw.circle(self.screen, SLOT_BG, center, self.radius)

        # Pieces
        for row in range(self.config.rows):
            for column in range(self.config.columns):
                piece = int(self.board[row, column])
                if piece == 0:
                    continue

                x, y = self.board_position_to_screen_center(row, column)

                # small shadow
                pygame.draw.circle(
                    self.screen,
                    (0, 0, 0),
                    (x + 2, y + 3),
                    self.radius,
                )

                pygame.draw.circle(
                    self.screen,
                    self.player_color(piece),
                    (x, y),
                    self.radius,
                )

                # last move highlight
                if self.last_move == (row, column):
                    pygame.draw.circle(self.screen, ACCENT, (x, y), self.radius + 4, 3)

                # winning highlight
                if (row, column) in self.winning_cells:
                    pygame.draw.circle(self.screen, SUCCESS, (x, y), self.radius + 8, 5)

    def draw_footer(self) -> None:
        footer_y = self.board_bottom
        pygame.draw.rect(
            self.screen,
            FOOTER_BG,
            (0, footer_y, self.width, self.footer_height),
        )

        help_text = "Click a column to drop a piece"
        if self.controller_for(self.current_player) == Controller.AI and not self.game_over:
            help_text = "AI move in progress..."
        if self.game_over:
            help_text = "Press R to restart or ESC to quit"

        help_surface = self.small_font.render(help_text, True, TEXT_MUTED)
        self.screen.blit(help_surface, (12, footer_y + 10))

        # Column numbers
        for col in range(self.config.columns):
            label = self.small_font.render(str(col + 1), True, TEXT_MUTED)
            label_rect = label.get_rect(
                center=(
                    col * self.cell_size + self.cell_size // 2,
                    footer_y + self.footer_height // 2,
                )
            )
            self.screen.blit(label, label_rect)

    def draw_game_over_overlay(self) -> None:
        if not self.game_over:
            return

        overlay = pygame.Surface((self.width, self.board_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, OVERLAY_ALPHA))
        self.screen.blit(overlay, (0, self.board_top))

        box_width = min(self.width - 40, max(320, self.width // 2))
        box_height = 110
        box_x = (self.width - box_width) // 2
        box_y = self.board_top + (self.board_height - box_height) // 2

        pygame.draw.rect(
            self.screen,
            PANEL_BG,
            (box_x, box_y, box_width, box_height),
            border_radius=12,
        )
        pygame.draw.rect(
            self.screen,
            ACCENT,
            (box_x, box_y, box_width, box_height),
            width=2,
            border_radius=12,
        )

        message_surface = self.title_font.render(self.message, True, TEXT)
        message_rect = message_surface.get_rect(center=(self.width // 2, box_y + 38))
        self.screen.blit(message_surface, message_rect)

        hint_surface = self.small_font.render("Press R to play again", True, TEXT_MUTED)
        hint_rect = hint_surface.get_rect(center=(self.width // 2, box_y + 80))
        self.screen.blit(hint_surface, hint_rect)

    def draw(self) -> None:
        self.screen.fill(BG)
        self.draw_top_bar()
        self.draw_hover_preview()
        self.draw_board()
        self.draw_footer()
        self.draw_game_over_overlay()
        pygame.display.flip()

    # ---------------------------------------------------------------------
    # Main loop
    # ---------------------------------------------------------------------

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event)
                if not running:
                    break

            if (
                running
                and not self.game_over
                and self.controller_for(self.current_player) == Controller.AI
            ):
                self.make_ai_move()

            self.draw()
            self.clock.tick(60)

        pygame.quit()