import random

def findRandomMove(validMoves):
    if not validMoves:
        return None
    return validMoves[random.randint(0,len(validMoves)-1)]