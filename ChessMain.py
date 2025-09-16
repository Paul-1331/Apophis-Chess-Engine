""" Main driver file responsible for user input and displaying current gamestate object"""

import pygame as p
import ChessEngine

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

""" Initialize a global dictionary of images. This will be called exactly once in main"""

def loadImages():
    pieces = ["wP","wR","wN","wB","wQ","wK","bP","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chessimages/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
    #we can access an IMAGE by saying  IMAGES["wP"]

""" Handle user input and update the graphics"""

def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made,we should regenerate valid moves only after user makes a move
    loadImages()#only do this once before the while loop
    running = True
    sqSelected = ()#no square is selected, keep track of last click of the user(tuple (row,col))
    playerClicks = [] #keep track of player clicks(two tuples:[(6,4),(4,4)])
    while running:
        for e in p.event.get():
            if e.type== p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()#(x,y)location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):#user clicked same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)#append for both first and second clicks
                if len(playerClicks)==2:#after 2nd click
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            print(move.getChessNotation())
                            sqSelected = ()#reset user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

""" Responsible for all the graphics within a current game state"""

def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    #add in pieces highlighting or move suggestions(later)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares
    # Show checkmate/stalemate message
    if gs.checkmate:
        if gs.whitetomove:
            drawEndGameText(screen, "Black wins by checkmate!")
        else:
            drawEndGameText(screen, "White wins by checkmate!")
    elif gs.stalemate:
        drawEndGameText(screen, "Stalemate!")

"""Draw the squares on the board. The top left corner is always light"""
def drawBoard(screen):
    colors = [p.Color("light gray"),p.Color("brown")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


"""Draw the pieces on the board using the current GameState.board"""
def drawPieces(screen,board):
     for r in range(DIMENSION):
         for c in range(DIMENSION):
             piece = board[r][c]
             if piece !="--":
                 screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 36, True, False)
    textObject = font.render(text, 0, p.Color('Blue'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - textObject.get_width()//2, HEIGHT//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)


if __name__ == "__main__":
    main()
