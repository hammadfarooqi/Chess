# from BoardObject import *
#Position is always row, column
#Top left = 0, 0

class Piece:
    #white = "w"
    #black = "b"
    
    # pawn = "p"
    # knight = "n"
    # bishop = "b"
    # rook = "r"
    # queen = "q"
    # king = "k"
    
    def __init__(self, type, color):
        self.type = type
        self.color = color
        if color == "w":
            self.enemy = "b"
        else:
            self.enemy = "w"
        self.moved = False
        self.first_move = False
    
    def __str__(self):
        return " "+self.color+self.type+" "