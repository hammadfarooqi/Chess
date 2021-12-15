import pygame
from Pieces import *
#Position is always row, column
#Top left = 0, 0

class Board:
    #white = "w"
    #black = "b"
    
    # Check for checking - Done
    # Check for checkmate - Done
    # pawn = "p" - Needs En Pasante and promotion
    # knight = "n" - Done
    # bishop = "b" - Done
    # rook = "r" - Done
    # queen = "q" - Done
    # king = "k" - Needs Castle
    
    def __init__(self):
        self.turn = "w"
        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(None)

    def check_move(self, initial, final):
        piece = self.board[initial[0]][initial[1]]
        if piece and piece.color == self.turn and final in self.get_moves(initial):
            old_final = self.board[final[0]][final[1]]
            self.board[final[0]][final[1]] = self.board[initial[0]][initial[1]]
            self.board[initial[0]][initial[1]] = None
            if piece.type == "k":
                if not self.check_check(final, self.turn):
                    self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
                    self.board[final[0]][final[1]] = old_final
                    return True
            else:
                if not self.check_check(self.find_king(self.turn), self.turn):
                    self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
                    self.board[final[0]][final[1]] = old_final
                    return True
            self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
            self.board[final[0]][final[1]] = old_final

    def check_check(self, position, color):
        old_piece = self.board[position[0]][position[1]]
        if color == "w":
            self.board[position[0]][position[1]] = Piece('k', 'w')
            color = "b"
        else:
            self.board[position[0]][position[1]] = Piece('k', 'b')
            color = "w"
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if item and item.color == color and position in self.get_moves((i,j)):
                    self.board[position[0]][position[1]] = old_piece
                    return True
        self.board[position[0]][position[1]] = old_piece

    def check_result(self):
        gameover = ""
        if self.check_check(self.find_king(self.turn), self.turn):
            gameover = self.turn
            for i, row in enumerate(self.board):
                for j, item in enumerate(row):
                    if item and item.color == self.turn and len(self.get_legal_moves((i,j))) > 0:
                        gameover = ""
                        break
                if not gameover:
                    break
        return gameover

    def make_move(self, initial, final):
        if self.check_move(initial, final):
            self.board[final[0]][final[1]] = self.board[initial[0]][initial[1]]
            self.board[initial[0]][initial[1]] = None
            self.board[final[0]][final[1]].moved = True
            self.turn = self.board[final[0]][final[1]].enemy
            
            return True, self.check_result()

    def find_king(self, color):
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if item and item.type == "k" and item.color == color:
                    return (i, j)

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
            if piece.color == "w":
                color_factor = 1
            else:
                color_factor = -1
            
            if not self.board[pos[0] - 1 * color_factor][pos[1]]:
                moves.append((pos[0] - 1 * color_factor, pos[1]))
                if (not piece.moved) and (not self.board[pos[0] - 2 * color_factor][pos[1]]):
                    moves.append((pos[0] - 2 * color_factor, pos[1]))
            if pos[1]-1 >= 0:
                if self.board[pos[0] - 1 * color_factor][pos[1] - 1] and self.board[pos[0] - 1 * color_factor][pos[1] - 1].color == piece.enemy:
                    moves.append((pos[0] - 1 * color_factor, pos[1] - 1))
            if pos[1]+1 <= 7:
                if self.board[pos[0] - 1 * color_factor][pos[1] + 1] and self.board[pos[0] - 1 * color_factor][pos[1] + 1].color == piece.enemy:
                    moves.append((pos[0] - 1 * color_factor, pos[1] + 1))

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

        if piece.type == "k":
            #Up
            if pos[0]-1 >= 0:
                if not self.board[pos[0]-1][pos[1]] or self.board[pos[0]-1][pos[1]].color == piece.enemy:
                    moves.append((pos[0]-1, pos[1]))
            
            #Up left
            if pos[0]-1 >= 0 and pos[1]-1 >= 0:
                if not self.board[pos[0]-1][pos[1]-1] or self.board[pos[0]-1][pos[1]-1].color == piece.enemy:
                    moves.append((pos[0]-1, pos[1]-1))

            #Left
            if pos[1]-1 >= 0:
                if not self.board[pos[0]][pos[1]-1] or self.board[pos[0]][pos[1]-1].color == piece.enemy:
                    moves.append((pos[0], pos[1]-1))
            
            #Down left
            if pos[0]+1 <= 7 and pos[1]-1 >= 0:
                if not self.board[pos[0]+1][pos[1]-1] or self.board[pos[0]+1][pos[1]-1].color == piece.enemy:
                    moves.append((pos[0]+1, pos[1]-1))
            
            #Down
            if pos[0]+1 <= 7:
                if not self.board[pos[0]+1][pos[1]] or self.board[pos[0]+1][pos[1]].color == piece.enemy:
                    moves.append((pos[0]+1, pos[1]))
            
            #Down right
            if pos[0]+1 <= 7 and pos[1]+1 <= 7:
                if not self.board[pos[0]+1][pos[1]+1] or self.board[pos[0]+1][pos[1]+1].color == piece.enemy:
                    moves.append((pos[0]+1, pos[1]+1))

            #Right
            if pos[1]+1 <= 7:
                if not self.board[pos[0]][pos[1]+1] or self.board[pos[0]][pos[1]+1].color == piece.enemy:
                    moves.append((pos[0], pos[1]+1))
            
            #Up right
            if pos[0]-1 >= 0 and pos[1]+1 <= 7:
                if not self.board[pos[0]-1][pos[1]+1] or self.board[pos[0]-1][pos[1]+1].color == piece.enemy:
                    moves.append((pos[0]-1, pos[1]+1))

        return moves

    def get_legal_moves(self, pos):
        moves = self.get_moves(pos)
        final_moves = []
        for move in moves:
            if self.check_move(pos, move):
                final_moves.append(move)
        return final_moves

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
    # board = board_object.board
    board = board_object
    for row in board:
        for element in row:
            if element:
                print(str(element), end = "")
            else:
                print(" ** ", end = "")
        print()

if __name__ == "__main__":
    test_board = Board()
    test_board.add_piece("p", "w", (6, 1))
    test_board.add_piece("p", "b", (5, 2))
    # printBoard(test_board)
    # print(test_board.get_moves((6, 1)))

    # print()
    test_board.new_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # test_board.add_piece("n", "w", (4, 6))
    # test_board.add_piece("r", "w", (3, 2))
    # test_board.add_piece("r", "b", (3, 4))
    # printBoard(test_board)
    # test_board.check_move((7,1), (5,2))
    # test_board.check_move((1,7), (3,7))
    
    # print(test_board.get_moves((3, 4)))
    while True:
        printBoard(test_board.board)
        user_move = input("Give move: ")
        
        while True:
            move = user_move.split(",")
            initial = (int(move[0]), int(move[1]))
            final = (int(move[2]), int(move[3]))
            if test_board.make_move(initial, final):
                break
            user_move = input("Invalid move. Give another move: ")

