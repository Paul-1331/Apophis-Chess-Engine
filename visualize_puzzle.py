# pyrefly: ignore [missing-import]
import pygame as p
import ChessEngine
import Apophis
import ChessMain
from benchmark import load_fen

# ==========================================
# CONFIGURATION
# ==========================================
# Set the FEN position you want to visualize:
# Current: Back-Rank Mate in 2 (White to move)
TEST_FEN = "6k1/5ppp/4r3/8/8/8/8/3R2K1 w - - 0 1"

AI_DEPTH = 3            # Search depth for the AI

def main():
    p.init()
    screen = p.display.set_mode((ChessMain.WIDTH, ChessMain.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    # 1. Initialize empty GameState
    gs = ChessEngine.GameState()
    
    # 2. Load the custom FEN position
    load_fen(gs, TEST_FEN)
    
    # Automatically assign the active player from FEN as the AI, and the other as human
    white_is_human = not gs.whitetomove
    black_is_human = gs.whitetomove
    
    validMoves = gs.getValidMoves()
    moveMade = False
    ChessMain.loadImages()  # Reuse pieces images loader
    
    running = True
    sqSelected = ()
    playerClicks = []
    
    print(f"Loaded position: {TEST_FEN}")
    print(f"Active Player (Human): {'White' if white_is_human else 'Black'}")
    print(f"Opponent (AI): {'Black' if white_is_human else 'White'}")
    
    # Draw the initial board once and wait 1 second so you can see the setup before the AI plays
    ChessMain.drawGameState(screen, gs, sqSelected)
    p.display.flip()
    p.time.delay(1500)  # 1.5 seconds delay
    
    while running:
        # Determine if it's the AI's turn to move
        is_ai_turn = (gs.whitetomove and not white_is_human) or (not gs.whitetomove and not black_is_human)
        
        if is_ai_turn and not (gs.checkmate or gs.stalemate):
            # AI calculates best move
            AIMove = Apophis.findBestMove(gs, validMoves, AI_DEPTH)
            gs.makeMove(AIMove)
            moveMade = True
            print(f"AI plays: {AIMove.getChessNotation()}")
            p.time.delay(500)
        else:
            # Handle Human events
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN and not is_ai_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // ChessMain.SQ_SIZE
                    row = location[1] // ChessMain.SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                print(f"Player plays: {move.getChessNotation()}")
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # Press 'z' to undo moves
                        gs.undoMove()
                        if not white_is_human or not black_is_human:
                            gs.undoMove()  # Undo the AI move as well
                        moveMade = True
                        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        # Draw board, highlight options, draw pieces
        ChessMain.drawGameState(screen, gs, sqSelected)
        clock.tick(ChessMain.MAX_FPS)
        p.display.flip()
        
        if gs.checkmate or gs.stalemate:
            p.time.delay(3000)
            running = False

if __name__ == "__main__":
    main()
