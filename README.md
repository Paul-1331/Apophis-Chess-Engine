# Apophis Chess Engine

Apophis is a lightweight, modular chess engine built in Python. It features a custom 2D-grid-based board representation, complete legal move generation (including castling, en passant, and pawn promotions), and a search AI using depth-limited Minimax optimized with Alpha-Beta pruning. 

It comes with an interactive graphical interface built using Pygame and a performance benchmarking suite to measure speed and tactical accuracy.

---

## Features

* **Complete Legal Move Generator**: Full compliance with FIDE rules, including check detection, castling rights tracking, en passant captures, and automatic queen pawn promotions.
* **Alpha-Beta Minimax AI**: A depth-limited lookahead search AI utilizing Alpha-Beta pruning to optimize search space traversal.
* **Interactive Pygame GUI**: A clean, graphical interface that supports move highlighting, legal move suggestion, undoing moves (`Z` key), and game-over state overlays.
* **Clean Architecture**: Strong separation of concerns between game state management (`ChessEngine.py`), search AI (`Apophis.py`), and the user interface (`ChessMain.py`).
* **Benchmarking & Testing Tools**: Native CLI benchmark to profile move generation speed (Perft) and AI lookahead efficiency, alongside a graphical tool to visualize and test custom FEN board states.

---

## Project Architecture

* **`ChessEngine.py`**: Manages the board state, move history, en passant target squares, castling rights, and implements the move validation algorithms.
* **`Apophis.py`**: Contains the Minimax search and static material evaluation functions.
* **`ChessMain.py`**: The driver script containing the Pygame loop, drawing utilities, and user click handling.
* **`benchmark.py`**: Profiling script evaluating Perft throughput, search Nodes Per Second (NPS), and solving rate on a tactical suite.
* **`visualize_puzzle.py`**: Utility to load custom FEN strings, allowing you to play against the AI from any arbitrary position or watch the AI solve complex tactical sequences.

---

## Performance & Optimization Benchmarks

The engine was profiled on a local environment using Python 3.13.5:

### 1. Move Generation Speed (Perft)
Perft (Performance Test) counts the total leaf nodes at a given depth to verify move generator throughput:
* **Depth 1**: 20 positions (~82,000 NPS)
* **Depth 2**: 400 positions (~110,000 NPS)
* **Depth 3**: 8,902 positions (~111,000 NPS)
* **Depth 4**: 197,281 positions (**165,000+ NPS**)

### 2. Search Optimization
By implementing Alpha-Beta pruning, the search space at Depth 4 was **reduced by 99.27%** (visiting only 1,435 nodes instead of the raw 197,281 leaf nodes), enabling optimal moves to be calculated in **under 0.16 seconds**.

### 3. Tactical Accuracy
Tested against a tactical puzzle suite (including Mate-in-1, Mate-in-2, and tactical forks), the engine achieved a **100% solve rate** with an average decision time of **0.036 seconds** per puzzle.

---

## Getting Started

### Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/Paul-1331/Apophis-Chess-Engine.git
cd Apophis
pip install -r requirements.txt
```

### Running the Game
To start the interactive GUI:
```bash
python ChessMain.py
```

### Running the Benchmarks
To run the performance profiles and tactical tests:
```bash
python benchmark.py
```

### Testing Custom Positions
To visualize and test custom positions using FEN strings, edit the `TEST_FEN` variable in `visualize_puzzle.py` and run:
```bash
python visualize_puzzle.py
```

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.