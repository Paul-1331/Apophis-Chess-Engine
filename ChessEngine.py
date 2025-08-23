""" class responsible for storing all the information about the current state of a chess game,
also responsible for determining the valid moves at the current state, also keep a move log"""

class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element has 2 characters
        #first character represents color of the piece
        #second character represents the piece
        # -- represents a empty space with no piece
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whitetomove = True
        self.moveLog = []