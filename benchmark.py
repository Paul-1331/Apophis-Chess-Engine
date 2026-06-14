import time
import ChessEngine
import Apophis

def load_fen(gs, fen):
    """
    Parses a FEN (Forsyth-Edwards Notation) string and loads it into the GameState.
    This allows testing the AI and move generator on any arbitrary chess position.
    
    FEN Format: [Board Representation] [Active Color] [Castling Rights] [En Passant Target] ...
    Example: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" (Starting Position)
    """
    parts = fen.split()
    board_part = parts[0]
    active_color = parts[1]
    castling = parts[2]
    enpassant = parts[3]
    
    # 1. Reset and clear the board representation
    gs.board = [["--" for _ in range(8)] for _ in range(8)]
    
    # 2. Parse the piece placement rows (from rank 8 down to rank 1)
    rows = board_part.split('/')
    for r in range(8):
        col = 0
        for char in rows[r]:
            if char.isdigit():
                col += int(char)  # Skip empty squares
            else:
                color = 'w' if char.isupper() else 'b'
                piece = char.upper()
                gs.board[r][col] = color + piece
                # Track king locations for check detection
                if piece == 'K':
                    if color == 'w':
                        gs.whiteKingLocation = (r, col)
                    else:
                        gs.blackKingLocation = (r, col)
                col += 1
                
    # 3. Set whose turn it is
    gs.whitetomove = (active_color == 'w')
    
    # 4. Set en passant target square
    if enpassant != '-':
        col_char = enpassant[0]
        row_char = enpassant[1]
        col = ord(col_char) - ord('a')
        row = 8 - int(row_char)
        gs.enpassantPossible = (row, col)
    else:
        gs.enpassantPossible = ()
        
    # 5. Restore castling rights (True = not moved/allowed, False = moved/lost)
    gs.whiteKingMoved = 'K' not in castling and 'Q' not in castling
    gs.whiteRookAMoved = 'Q' not in castling
    gs.whiteRookHMoved = 'K' not in castling
    gs.blackKingMoved = 'k' not in castling and 'q' not in castling
    gs.blackRookAMoved = 'q' not in castling
    gs.blackRookHMoved = 'k' not in castling
    
    # 6. Reset game-over states and log
    gs.moveLog = []
    gs.checkmate = False
    gs.stalemate = False

# Global stats to track minimax evaluations
minimax_nodes = 0
minimax_evals = 0
minimax_prunes = 0

def benchmark_minimax(gs, validMoves, depth, alpha, beta, whiteToMove):
    """
    Subclass-free version of your minimax search with added node and pruning counters.
    Matches your exact AI logic in Apophis.py.
    """
    global minimax_nodes, minimax_evals, minimax_prunes
    minimax_nodes += 1

    if depth == 0:
        minimax_evals += 1
        return Apophis.scoreMaterial(gs.board), None

    best_move = None
    if whiteToMove:
        maxScore = -Apophis.CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            score, _ = benchmark_minimax(gs, gs.getValidMoves(), depth-1, alpha, beta, False)
            gs.undoMove()
            if score > maxScore:
                maxScore = score
                best_move = move
            alpha = max(alpha, maxScore)
            if beta <= alpha:
                minimax_prunes += 1
                break
        return maxScore, best_move
    else:
        minScore = Apophis.CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            score, _ = benchmark_minimax(gs, gs.getValidMoves(), depth-1, alpha, beta, True)
            gs.undoMove()
            if score < minScore:
                minScore = score
                best_move = move
            beta = min(beta, minScore)
            if beta <= alpha:
                minimax_prunes += 1
                break
        return minScore, best_move

# Perft implementation (counts all leaf nodes at depth to test move gen speed)
perft_nodes = 0
def perft(depth, gs):
    global perft_nodes
    if depth == 0:
        return 1
    moves = gs.getValidMoves()
    nodes = 0
    for move in moves:
        gs.makeMove(move)
        n = perft(depth - 1, gs)
        nodes += n
        perft_nodes += n
        gs.undoMove()
    return nodes

def run_perft_benchmark():
    print("=================== PERFT BENCHMARK ===================")
    gs = ChessEngine.GameState()
    load_fen(gs, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    for d in range(1, 5):
        global perft_nodes
        perft_nodes = 0
        start = time.perf_counter()
        count = perft(d, gs)
        end = time.perf_counter()
        elapsed = end - start
        nps = count / elapsed if elapsed > 0 else 0
        print(f"Perft Depth {d}: {count} leaves found in {elapsed:.4f}s ({nps:.2f} nodes/sec)")

def run_search_benchmark():
    print("\n=================== SEARCH BENCHMARK ===================")
    gs = ChessEngine.GameState()
    load_fen(gs, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    for d in range(1, 5):
        global minimax_nodes, minimax_evals, minimax_prunes
        minimax_nodes = 0
        minimax_evals = 0
        minimax_prunes = 0
        
        start = time.perf_counter()
        valid = gs.getValidMoves()
        score, move = benchmark_minimax(gs, valid, d, -Apophis.CHECKMATE, Apophis.CHECKMATE, gs.whitetomove)
        end = time.perf_counter()
        elapsed = end - start
        
        nps = minimax_nodes / elapsed if elapsed > 0 else 0
        move_notation = move.getChessNotation() if move else "None"
        print(f"Search Depth {d}: Best move {move_notation} (score {score}) in {elapsed:.4f}s")
        print(f"  - Total nodes evaluated: {minimax_nodes}")
        print(f"  - Leaf evaluations: {minimax_evals}")
        print(f"  - Alpha-Beta prunes: {minimax_prunes}")
        print(f"  - Search speed: {nps:.2f} nodes/sec")

def run_puzzle_tests():
    print("\n=================== PUZZLE SOLVING TESTS ===================")
    # Define tactical chess positions to test the AI's accuracy
    # Feel free to add your own puzzle definitions here!
    puzzles = [
        {
            "name": "Mate in 1 (Queen Mate)",
            "fen": "k7/P7/1Q6/8/8/8/8/K7 w - - 0 1",
            "expected": ["b6b8"],
            "depth": 2
        },
        {
            "name": "Scholar's Mate in 1",
            "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
            "expected": ["h5f7"],
            "depth": 2
        },
        {
            "name": "Tactical Fork (Knight fork of King and Queen)",
            "fen": "q3k3/8/8/3N4/8/8/8/4K3 w - - 0 1",
            "expected": ["d5c7"],
            "depth": 3  # Knight fork requires looking ahead to capture the queen
        },
        {
            "name": "Back-Rank Mate in 2",
            "fen": "6k1/5ppp/4r3/8/8/8/8/3R2K1 w - - 0 1",
            "expected": ["d1d8"],
            "depth": 3  # Requires depth 3 (1. Rd8+ Re8 2. Rxe8#)
        }
    ]
    
    solved_count = 0
    for idx, puzzle in enumerate(puzzles):
        gs = ChessEngine.GameState()
        load_fen(gs, puzzle["fen"])
        valid = gs.getValidMoves()
        
        global minimax_nodes
        minimax_nodes = 0
        start = time.perf_counter()
        score, move = benchmark_minimax(gs, valid, puzzle["depth"], -Apophis.CHECKMATE, Apophis.CHECKMATE, gs.whitetomove)
        end = time.perf_counter()
        elapsed = end - start
        
        move_notation = move.getChessNotation() if move else "None"
        success = move_notation in puzzle["expected"]
        if success:
            solved_count += 1
            status = "PASSED"
        else:
            status = "FAILED"
            
        print(f"Puzzle {idx+1}: {puzzle['name']} -> {status}")
        print(f"  - Expected: {puzzle['expected']}, Found: {move_notation}")
        print(f"  - Nodes evaluated: {minimax_nodes} in {elapsed:.4f}s ({minimax_nodes/(elapsed if elapsed > 0 else 1):.2f} nodes/sec)")

    print(f"\nSolved {solved_count}/{len(puzzles)} tactical puzzles successfully.")

if __name__ == "__main__":
    run_perft_benchmark()
    run_search_benchmark()
    run_puzzle_tests()
