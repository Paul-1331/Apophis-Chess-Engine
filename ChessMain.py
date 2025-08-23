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
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
    #we can access an IMAGE by saying  IMAGES["wP"]

""" Handle user input and update the graphics"""

def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    #print(gs.board)
    loadImages()#only do this once before the while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type== p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        p.display.flip()

""" Responsible for all the graphics within a current game state"""

def drawGameState(screen,gs):
    drawBoard(screen)#draw squares on the board
    #add in pieces highlighting or move suggestions(later)
    drawPieces(screen,gs.board)#draw pieces on top of those squares

"""Draw the squares on the board. The top left corner is always light"""
def drawBoard(screen):
    colors = [p.Color("light gray"),p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


"""Draw the pieces on the board using the current GameState.board"""
def drawPieces(screen,board):
     pass


if __name__ == "__main__":
    main()
