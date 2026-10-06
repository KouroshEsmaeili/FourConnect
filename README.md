# Connect Four — Minimax & Alpha-Beta Search

[![Tests](https://github.com/KouroshEsmaeili/FourConnect/actions/workflows/tests.yml/badge.svg)](https://github.com/KouroshEsmaeili/FourConnect/actions/workflows/tests.yml)

A modular Python implementation of Connect Four using **depth-limited minimax**, **alpha-beta pruning**, and **heuristic board evaluation**, with a lightweight Pygame interface.

Originally developed as part of an Advanced Programming course, the project has since been refactored into a cleaner standalone implementation focused on algorithms, game-state modeling, and testing. It is an educational algorithms project, not a competitive or perfect-play Connect Four engine.

## Highlights

- Human vs Human, Human vs AI, AI vs Human, and AI vs AI modes
- Configurable board dimensions, Connect-N target, and AI search depths
- Depth-limited minimax with alpha-beta pruning and center-first move ordering
- Hand-designed heuristic evaluation for horizontal, vertical, and diagonal patterns
- Pygame interface with search diagnostics and a typed, modular game engine
- Automated tests and CI on Python 3.10 and 3.12

## Search algorithm

The AI uses depth-limited minimax. At each layer, the player to move either maximizes the root player's score or minimizes it on behalf of the opponent. Terminal wins, losses, and draws receive fixed utility values; when the depth limit is reached first, the heuristic evaluates center control and potential Connect-N windows.

Alpha-beta bounds discard branches that cannot affect the selected result. Legal moves are examined from the center outward because promising moves found earlier often tighten those bounds sooner. This ordering can improve pruning efficiency, but it does not change minimax correctness.

Each search returns a `SearchResult` containing the selected move and score plus its principal variation, number of evaluated nodes, alpha-beta cutoff count, and elapsed time. The timing is diagnostic only and is not treated as a performance benchmark.

## Installation

Create and activate a Python 3.10+ virtual environment, then install the project. For development, include the test and lint tools:

```bash
python -m pip install -e ".[dev]"
```

For play-only use, `python -m pip install -e .` installs just the runtime dependencies.

## Run

After installation, each of these launches Human vs AI mode:

```bash
connect-four --mode hai
python -m connect_four --mode hai
python main.py --mode hai
```

Modes are `hh`, `hai`, `aih`, and `aiai`. Use `--rows`, `--columns`, and `--connect` for a custom Connect-N board; `--depth1` and `--depth2` set each AI player's search depth. Run any interface with `--help` for all options.

Controls: move the mouse to select a column, left-click to drop a piece, press `R` to restart, and press `Esc` to quit.

## Testing and validation

The 37-test suite covers game mechanics, win and draw detection, configurable Connect-N boards, heuristic behavior, immediate wins and forced blocks, search legality and determinism, diagnostics, validation, and CLI parsing.

```bash
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

## Architecture / project structure

```text
connect_four/
├── __init__.py      # package API
├── __main__.py      # python -m connect_four entry point
├── app.py           # Pygame application and rendering
├── board.py         # board state and game rules
├── cli.py           # argument parsing and application entry point
├── config.py        # validated Connect-N configuration
├── heuristic.py     # position evaluation
├── minimax.py       # minimax, alpha-beta pruning, and diagnostics
└── players.py       # AI player wrapper

tests/               # board, configuration, heuristic, search, and CLI tests
main.py              # backward-compatible script entry point
pyproject.toml       # packaging, dependencies, and Ruff configuration
```

## Limitations

- Depth-limited heuristic search is not a perfect Connect Four solver.
- There is no solved-game database or endgame tablebase.
- There is no transposition table, so repeated positions are not cached.
- Runtime increases rapidly with search depth.
- Heuristic weights are hand-designed rather than learned or scientifically tuned.
- Interactive GUI behavior has not received broad platform or device testing.

These are deliberate scope choices for a compact educational project.

## Attribution

This project originated as an Advanced Programming course project and was later refactored into the current modular, tested implementation.
