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
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = () #coordinates for the square where enpassant capture is possible

    """Takes move as parameter and executes it, will not work for enpassant,castling,pawn promotion"""
    def makeMove(self,move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)#log the move so we can undo it later
        self.whitetomove = not self.whitetomove #swap players
        #update King Location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow,move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'#queen promotion only for now

        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'
        if move.pieceMoved[1] == 'P' and abs(move.startRow-move.endRow) == 2:
            self.enpassantPossible = ((move.startRow+move.endRow)//2,move.startCol)
        else:
            self.enpassantPossible = () #reseting enpasant possible

    
    """Undo the last move"""
    def undoMove(self):
        if self.moveLog:#make sure moveLog is not empty
            lastMove = self.moveLog.pop()
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.whitetomove = not self.whitetomove
            if lastMove.pieceMoved == "wK":
                self.whiteKingLocation = (lastMove.startRow,lastMove.startCol)
            elif lastMove.pieceMoved == "bK":
                self.blackKingLocation = (lastMove.startRow,lastMove.startCol)
            if lastMove.isPawnPromotion:
                self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved[0]+'P'
            if lastMove.isEnpassantMove:
                self.board[lastMove.endRow][lastMove.endCol] = '--'
                self.board[lastMove.startRow][lastMove.endCol] = lastMove.pieceCaptured
                self.enpassantPossible = (lastMove.startRow,lastMove.startCol)
            if lastMove.pieceMoved == 'P' and abs(lastMove.startRow-lastMove.endRow)==2:
                self.enpassantPossible = ()

    def getValidMoves(self):
        moves =  self.getAllPossibleMoves()

        tempEnpassantPossible = self.enpassantPossible

        for i in range(len(moves)-1,-1,-1):
            """ For each of my moves, check if any of opponents moves attack my king"""
            self.makeMove(moves[i])#we make a move, now it is opponents turn, and we need to check if now our king is under attack
            self.whitetomove = not self.whitetomove #this is so that we are checking if our king is in check, not the opponents king
            if self.inCheck():
                moves.remove(moves[i])
            self.whitetomove = not self.whitetomove #change back to their move
            self.undoMove() #take back move and change back to our move
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.enpassantPossible = tempEnpassantPossible
        return moves


    def inCheck(self):
        if self.whitetomove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
        
    
    """def squareUnderAttack(self,r,c):
        self.whitetomove = not self.whitetomove #switch to other player temporarily
        oppMoves = self.getAllPossibleMoves()
        self.whitetomove = not self.whitetomove #switch back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False"""

    def squareUnderAttack(self, r, c):
        """
        Returns True if the square (r, c) is under attack by the opponent.
        Efficiently checks for pawn, knight, bishop, rook, queen, and king attacks.
        """
        enemy_color = 'b' if self.whitetomove else 'w'
        ally_color = 'w' if self.whitetomove else 'b'

        # Check for pawn attacks
        if enemy_color == 'b':
            # Black pawns attack from above
            if r-1 >= 0:
                if c-1 >= 0 and self.board[r-1][c-1] == 'bP':
                    return True
                if c+1 < 8 and self.board[r-1][c+1] == 'bP':
                    return True
        else:
            # White pawns attack from below
            if r+1 < 8:
                if c-1 >= 0 and self.board[r+1][c-1] == 'wP':
                    return True
                if c+1 < 8 and self.board[r+1][c+1] == 'wP':
                    return True

        # Check for knight attacks
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == enemy_color + 'N':
                    return True

        # Check for rook/queen attacks (straight lines)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    piece = self.board[nr][nc]
                    if piece == "--":
                        continue
                    elif piece[0] == ally_color:
                        break
                    elif piece[0] == enemy_color and (piece[1] == 'R' or piece[1] == 'Q'):
                        return True
                    else:
                        break
                else:
                    break

        # Check for bishop/queen attacks (diagonals)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    piece = self.board[nr][nc]
                    if piece == "--":
                        continue
                    elif piece[0] == ally_color:
                        break
                    elif piece[0] == enemy_color and (piece[1] == 'B' or piece[1] == 'Q'):
                        return True
                    else:
                        break
                else:
                    break

        # Check for king attacks (adjacent squares)
        king_moves = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        for dr, dc in king_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == enemy_color + 'K':
                    return True

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c]
                if turn != "--":
                    if (self.whitetomove and turn[0] == "w") or (not self.whitetomove and turn[0] == "b"):
                        piece = self.board[r][c][1]
                        if piece == 'P':
                            self.getPawnMoves(r,c,moves)
                        elif piece == 'R':
                            self.getRookMoves(r,c,moves)
                        elif piece == 'B':
                            self.getBishopMoves(r,c,moves)
                        elif piece == 'N':
                            self.getKnightMoves(r,c,moves)
                        elif piece == 'Q':
                            self.getQueenMoves(r,c,moves)
                        elif piece == 'K':
                            self.getKingMoves(r,c,moves)

        return moves
    def getPawnMoves(self,r,c,moves):
        if self.whitetomove:
            if r-1>=0 and self.board[r-1][c] =="--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0:
                if r-1>=0 and self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove = True))
            if c+1<=7:
                if r-1>=0 and self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,isEnpassantMove = True))
        else:
            if r+1<=7 and self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0:
                if r+1<=7 and self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board,isEnpassantMove = True))
            if c+1<=7:
                if r+1<=7 and self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c+1),self.board,isEnpassantMove = True))
    def getRookMoves(self,r,c,moves):
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for d in directions:
            for i in range(1,8):
                newRow = r + d[0]*i
                newCol = c + d[1]*i
                if 0 <= newRow < 8 and 0 <= newCol < 8:#check if off the board
                    if self.board[newRow][newCol] == "--": #if empty square, we can move there
                        moves.append(Move((r,c),(newRow,newCol),self.board))
                    elif self.board[newRow][newCol][0] != self.board[r][c][0]:#if enemy on square, we can move there, but then further movement in that direction is stopped
                        moves.append(Move((r,c),(newRow,newCol),self.board))
                        break
                    else:#if ally on piece, we cant move to that square, further movement on that direction if not allowed
                        break
    def getBishopMoves(self,r,c,moves):
        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for d in directions:
            for i in range(1,8):
                newRow = r + d[0]*i
                newCol = c + d[1]*i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    if self.board[newRow][newCol] == "--":
                        moves.append(Move((r,c),(newRow,newCol),self.board))
                    elif self.board[newRow][newCol][0] != self.board[r][c][0]:
                        moves.append(Move((r,c),(newRow,newCol),self.board))
                        break
                    else:
                        break
    def getKnightMoves(self,r,c,moves):
        directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for d in directions:
            newRow = r + d[0]
            newCol = c + d[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if self.board[newRow][newCol] == "--":
                    moves.append(Move((r,c),(newRow,newCol),self.board))
                elif self.board[newRow][newCol][0] != self.board[r][c][0]:
                    moves.append(Move((r,c),(newRow,newCol),self.board))
    def getQueenMoves(self,r,c,moves):
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for d in directions:
            for i in range(1,8):
                newRow = r + d[0]*i
                newCol = c + d[1]*i
                if 0 <= newRow < 8 and 0 <= newCol < 8:
                    if self.board[newRow][newCol] == "--":
                        moves.append(Move((r,c),(newRow,newCol),self.board))
                    elif self.board[newRow][newCol][0] != self.board[r][c][0]:
                        moves.append(Move((r,c),(newRow,newCol),self.board))
                        break
                    else:
                        break
    def getKingMoves(self,r,c,moves):
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for d in directions:
            newRow = r + d[0]
            newCol = c + d[1]
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if self.board[newRow][newCol] == "--":
                    moves.append(Move((r,c),(newRow,newCol),self.board))
                elif self.board[newRow][newCol][0] != self.board[r][c][0]:
                    moves.append(Move((r,c),(newRow,newCol),self.board))

class Move():
    #map keys to values
    #key:value
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board,isEnpassantMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved=="wP" and self.endRow==0) or (self.pieceMoved == "bP" and self.endRow == 7):
            self.isPawnPromotion = True
        self.isEnpassantMove = isEnpassantMove

        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        self.moveId = self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol

    """ Overriding the equals method"""

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,row,col):
        return self.colsToFiles[col] + self.rowsToRanks[row]