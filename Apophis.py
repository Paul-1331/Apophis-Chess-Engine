import random

def findRandomMove(validMoves):
    if not validMoves:
        return None
    return validMoves[random.randint(0,len(validMoves)-1)]


pieceScore = {
    'K': 0, 'Q': 9, 'R': 5,
    'B': 3, 'N': 3, 'P': 1
}

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score


CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3

def findBestMove(gs, validMoves, depth):
    global nextMove
    nextMove = None
    minimax(gs, validMoves, depth, -CHECKMATE, CHECKMATE, gs.whitetomove)
    return nextMove if nextMove else findRandomMove(validMoves)

def minimax(gs, validMoves, depth, alpha, beta, whiteToMove):
    global nextMove

    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            score = minimax(gs, gs.getValidMoves(), depth-1, alpha, beta, False)
            gs.undoMove()
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            alpha = max(alpha, maxScore)
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            score = minimax(gs, gs.getValidMoves(), depth-1, alpha, beta, True)
            gs.undoMove()
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            beta = min(beta, minScore)
            if beta <= alpha:
                break
        return minScore
