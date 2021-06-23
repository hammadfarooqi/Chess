import pygame
from Pieces import *
#Position is always row, column
#Top left = 0, 0

class Board:
    #white = "w"
    #black = "b"
    
    # pawn = "p" - Needs En Pasante
    # knight = "n" - Done
    # bishop = "b" - Done
    # rook = "r" - Done
    # queen = "q" - Done
    # king = "k" - 
    
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
            moves.extend(get_rook_moves(self.board, pos, piece))
        
        if piece.type == "b":
            moves.extend(get_bishop_moves(self.board, pos, piece))

        if piece.type == "n":
            #Up and left
            if pos[0]-2 >= 0 and pos[1]-1 >= 0:
                if not self.board[pos[0]-2][pos[1]-1] or self.board[pos[0]-2][pos[1]-1].color == piece.enemy:
                    moves.append((pos[0]-2, pos[1]-1))
            if pos[0]-1 >= 0 and pos[1]-2 >= 0:
                if not self.board[pos[0]-1][pos[1]-2] or self.board[pos[0]-1][pos[1]-2].color == piece.enemy:
                    moves.append((pos[0]-1, pos[1]-2))

            #Up and right
            if pos[0]-2 >= 0 and pos[1]+1 <= 7:
                if not self.board[pos[0]-2][pos[1]+1] or self.board[pos[0]-2][pos[1]+1].color == piece.enemy:
                    moves.append((pos[0]-2, pos[1]+1))
            if pos[0]-1 >= 0 and pos[1]+2 <= 7:
                if not self.board[pos[0]-1][pos[1]+2] or self.board[pos[0]-1][pos[1]+2].color == piece.enemy:
                    moves.append((pos[0]-1, pos[1]+2))
            
            #Down and right
            if pos[0]+2 <= 7 and pos[1]+1 <= 7:
                if not self.board[pos[0]+2][pos[1]+1] or self.board[pos[0]+2][pos[1]+1].color == piece.enemy:
                    moves.append((pos[0]+2, pos[1]+1))
            if pos[0]+1 <= 7 and pos[1]+2 <= 7:
                if not self.board[pos[0]+1][pos[1]+2] or self.board[pos[0]+1][pos[1]+2].color == piece.enemy:
                    moves.append((pos[0]+1, pos[1]+2))
            
            #Down and left
            if pos[0]+2 <= 7 and pos[1]-1 >= 0:
                if not self.board[pos[0]+2][pos[1]-1] or self.board[pos[0]+2][pos[1]-1].color == piece.enemy:
                    moves.append((pos[0]+2, pos[1]-1))
            if pos[0]+1 <= 7 and pos[1]-2 >= 0:
                if not self.board[pos[0]+1][pos[1]-2] or self.board[pos[0]+1][pos[1]-2].color == piece.enemy:
                    moves.append((pos[0]+1, pos[1]-2))

        if piece.type == "q":
            moves.extend(get_rook_moves(self.board, pos, piece))
            moves.extend(get_bishop_moves(self.board, pos, piece))

        return moves

    def add_piece(self, piece, color, pos):
        self.board[pos[0]][pos[1]] = Piece(piece, color)
    
    def remove_piece(self, pos):
        self.board[pos[0]][pos[1]] = None

def get_bishop_moves(board, pos, piece):
    moves = []
    
    #Going down and right
    for i in range (1, min(8 - pos[0], 8 - pos[1]), 1):
        if board[pos[0]+i][pos[1]+i]:
            if board[pos[0]+i][pos[1]+i].color == piece.enemy:
                moves.append((pos[0]+i, pos[1]+i))
            break
        else:
            moves.append((pos[0]+i, pos[1]+i))

    #Going up and right
    for i in range (1, min(pos[0]+1, 8 - pos[1]), 1):
        if board[pos[0]-i][pos[1]+i]:
            if board[pos[0]-i][pos[1]+i].color == piece.enemy:
                moves.append((pos[0]-i, pos[1]+i))
            break
        else:
            moves.append((pos[0]-i, pos[1]+i))

    #Going down and left
    for i in range (1, min(8 - pos[0], pos[1]+1), 1):
        if board[pos[0]+i][pos[1]-i]:
            if board[pos[0]+i][pos[1]-i].color == piece.enemy:
                moves.append((pos[0]+i, pos[1]-i))
            break
        else:
            moves.append((pos[0]+i, pos[1]-i))

    #Going up and right
    for i in range (1, min(pos[0]+1, pos[1]+1), 1):
        if board[pos[0]-i][pos[1]-i]:
            if board[pos[0]-i][pos[1]-i].color == piece.enemy:
                moves.append((pos[0]-i, pos[1]-i))
            break
        else:
            moves.append((pos[0]-i, pos[1]-i))
    
    return moves

def get_rook_moves(board, pos, piece):
    moves = []

    #Going up from the piece
    for r in range(pos[0] - 1, -1, -1):
        if board[r][pos[1]]:
            if board[r][pos[1]].color == piece.enemy:
                moves.append((r, pos[1]))
            break
        else:
            moves.append((r, pos[1]))

    #Going down from the piece
    for r in range(pos[0] + 1, 8, 1):
        if board[r][pos[1]]:
            if board[r][pos[1]].color == piece.enemy:
                moves.append((r, pos[1]))
            break
        else:
            moves.append((r, pos[1]))

    #Going left from the piece
    for c in range(pos[1] - 1, -1, -1):
        if board[pos[0]][c]:
            if board[pos[0]][c].color == piece.enemy:
                moves.append((pos[0], c))
            break
        else:
            moves.append((pos[0], c))

    #Going right from the piece
    for c in range(pos[1] + 1, 8, 1):
        if board[pos[0]][c]:
            if board[pos[0]][c].color == piece.enemy:
                moves.append((pos[0], c))
            break
        else:
            moves.append((pos[0], c))
    
    return moves

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
    # printBoard(test_board)
    # print(test_board.get_moves((6, 1)))

    # print()
    test_board.new_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    test_board.add_piece("n", "w", (4, 6))
    test_board.add_piece("r", "w", (3, 2))
    test_board.add_piece("r", "b", (3, 4))
    printBoard(test_board)
    
    print(test_board.get_moves((3, 4)))
