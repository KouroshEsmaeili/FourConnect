# Connect Four — Minimax & Alpha-Beta Search

A modular Python implementation of Connect Four using **depth-limited minimax**, **alpha-beta pruning**, and **heuristic board evaluation**, with a lightweight Pygame interface.

Originally developed as part of an Advanced Programming course, the project has since been refactored into a cleaner standalone implementation focused on algorithms, game-state modeling, and testing.

## Features

* Human vs Human
* Human vs AI
* AI vs Human
* AI vs AI
* Minimax search
* Alpha-beta pruning
* Heuristic evaluation
* Center-first move ordering
* Configurable AI search depth
* Dynamic board dimensions
* Configurable Connect-N rules
* Pygame interface
* Automated tests

## Algorithm

The AI uses depth-limited minimax:

```text
Game State
    │
    ▼
Legal Moves
    │
    ▼
Minimax Search
 ┌─────┴─────┐
MAX         MIN
 └─────┬─────┘
       ▼
Alpha-Beta Pruning
       │
 ┌─────┴─────┐
Terminal   Depth Limit
 State         │
   │           ▼
 Utility    Heuristic
```

The heuristic evaluates horizontal, vertical, and diagonal windows and rewards promising patterns while penalizing opponent threats.

The search also explores central columns first to improve alpha-beta pruning efficiency.

## Project Structure

```text
connect_four/
├── app.py
├── board.py
├── config.py
├── heuristic.py
├── minimax.py
└── players.py

tests/
├── test_board.py
├── test_heuristic.py
└── test_minimax.py

main.py
pyproject.toml
```

## Installation

```bash
python -m venv .venv
python -m pip install -e .
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Run

Human vs AI:

```bash
python main.py --mode hai
```

Other modes:

```bash
python main.py --mode hh
python main.py --mode aih
python main.py --mode aiai
```

Custom board:

```bash
python main.py --rows 8 --columns 9 --connect 5
```

Custom AI depth:

```bash
python main.py --mode aiai --depth1 3 --depth2 5
```

## Controls

* Mouse: select column
* Left click: drop piece
* `R`: restart
* `Esc`: quit

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests cover game rules, win detection, dynamic board sizes, heuristic behavior, and minimax decisions.

## Tech

Python · NumPy · Pygame · unittest
