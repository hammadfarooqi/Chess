import pygame
from Pieces import *
#Position is always row, column
#Top left = 0, 0

class Board:
    #white = "w"
    #black = "b"
    
    # pawn = "p" - En Pasante
    # knight = "n"
    # bishop = "b"
    # rook = "r"
    # queen = "q"
    # king = "k"
    
    def __init__(self):
        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(None)

    def check_move(self, initial, final):
        pass

    def make_move(self, initial, final):
        pass

    def reset_board(self):
        for r in range(8):
            for c in range(8):
                self.board[r][c] = None

    def new_position(self, fen):
        self.reset_board()
        
        row = 0
        column = 0
        for char in fen[0: fen.find(" ")]:
            if char.isdigit():
                column += 1
            elif char == '/':
                row += 1
                column = 0
            elif char.isupper():
                self.add_piece(char.lower(), 'w', (row, column))
                column += 1
            else:
                self.add_piece(char, 'b', (row, column))
                column += 1
            

    def get_moves(self, pos):
        moves = []
        piece = self.board[pos[0]][pos[1]]
        if not piece:
            return []

        if piece.type == "p":
            if not self.board[pos[0] - 1][pos[1]]:
                moves.append((pos[0] - 1, pos[1]))
                if (not piece.moved) and (not self.board[pos[0] - 2][pos[1]]):
                    moves.append((pos[0] - 2, pos[1]))
            if self.board[pos[0] - 1][pos[1] - 1] and self.board[pos[0] - 1][pos[1] - 1].color == piece.enemy:
                moves.append((pos[0] - 1, pos[1] - 1))
            if self.board[pos[0] - 1][pos[1] + 1] and self.board[pos[0] - 1][pos[1] + 1].color == piece.enemy:
                moves.append((pos[0] - 1, pos[1] + 1))

        if piece.type == "r":
            #Going up from the piece
            for r in range(pos[0] - 1, -1, -1):
                if self.board[r][pos[1]]:
                    if self.board[r][pos[1]].color == piece.enemy:
                        moves.append((r, pos[1]))
                    break
                else:
                    moves.append((r, pos[1]))

            #Going down from the piece
            for r in range(pos[0] + 1, 8, 1):
                if self.board[r][pos[1]]:
                    if self.board[r][pos[1]].color == piece.enemy:
                        moves.append((r, pos[1]))
                    break
                else:
                    moves.append((r, pos[1]))

            #Going left from the piece
            for c in range(pos[1] - 1, -1, -1):
                if self.board[pos[0]][c]:
                    if self.board[pos[0]][c].color == piece.enemy:
                        moves.append((pos[0], c))
                    break
                else:
                    moves.append((pos[0], c))

            #Going right from the piece
            for c in range(pos[1] + 1, 8, 1):
                if self.board[pos[0]][c]:
                    if self.board[pos[0]][c].color == piece.enemy:
                        moves.append((pos[0], c))
                    break
                else:
                    moves.append((pos[0], c))
        
        return moves

    def add_piece(self, piece, color, pos):
        self.board[pos[0]][pos[1]] = Piece(piece, color)

def printBoard(board_object):
    board = board_object.board
    for row in board:
        for element in row:
            print(str(element), end = "")
        print()

if __name__ == "__main__":
    test_board = Board()
    test_board.add_piece("p", "w", (6, 1))
    test_board.add_piece("p", "b", (5, 2))
    printBoard(test_board)
    print(test_board.get_moves((6, 1)))

    print()
    test_board.new_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    test_board.add_piece("r", "w", (3, 4))
    test_board.add_piece("r", "w", (3, 2))
    test_board.add_piece("r", "b", (3, 6))
    printBoard(test_board)
    
    print(test_board.get_moves((3, 4)))
