import pygame
from Pieces import *
#Position is always row, column
#Top left = 0, 0

class Board:
    #white = "w"
    #black = "b"
    
    # Check for checking - Done
    # Check for checkmate - Done
    # pawn = "p" - Done
    # knight = "n" - Done
    # bishop = "b" - Done
    # rook = "r" - Done
    # queen = "q" - Done
    # king = "k" - Done
    
    def __init__(self):
        self.turn = "w"
        self.need_promotion = []
        self.board = []
        self.promotion_pieces = ("q", "r", "b", "n")
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(None)

    def check_move(self, initial, final):
        piece = self.board[initial[0]][initial[1]]
        if piece and piece.color == self.turn:
            in_moves = self.move_in_get_moves(initial, final)
            if in_moves[0]:
                if len(in_moves) == 1:
                    old_final = self.board[final[0]][final[1]]
                    self.board[final[0]][final[1]] = self.board[initial[0]][initial[1]]
                    self.board[initial[0]][initial[1]] = None
                    if piece.type == "k":
                        if not self.check_check(final, self.turn):
                            self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
                            self.board[final[0]][final[1]] = old_final
                            return True,
                    else:
                        if not self.check_check(self.find_king(self.turn), self.turn):
                            self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
                            self.board[final[0]][final[1]] = old_final
                            return True,
                    self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
                    self.board[final[0]][final[1]] = old_final
                else:
                    if in_moves[1] == "ep":
                        old_final = self.board[final[0]][final[1]]
                        self.board[final[0]][final[1]] = self.board[initial[0]][initial[1]]
                        self.board[initial[0]][initial[1]] = None
                        
                        if self.turn == "w":
                            color_factor = 1
                        else:
                            color_factor = -1
                        old_enemy = self.board[final[0]+1*color_factor][final[1]]
                        self.board[final[0]+1*color_factor][final[1]] = None
                        if not self.check_check(self.find_king(self.turn), self.turn):
                            self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
                            self.board[final[0]][final[1]] = old_final
                            self.board[final[0]+1*color_factor][final[1]] = old_enemy
                            return True, color_factor
                        self.board[initial[0]][initial[1]] = self.board[final[0]][final[1]]
                        self.board[final[0]][final[1]] = old_final
                        self.board[final[0]+1*color_factor][final[1]] = old_enemy
                    else:
                        if in_moves[1] == "cr":
                            color_factor = 1
                        else:
                            color_factor = -1
                        if not self.check_check(initial, self.turn):
                            old_piece = self.board[initial[0]][initial[1]]
                            self.board[initial[0]][initial[1]+1*color_factor] = self.board[initial[0]][initial[1]]
                            self.board[initial[0]][initial[1]] = None
                            if not self.check_check((initial[0],initial[1]+1*color_factor), self.turn):
                                self.board[final[0]][final[1]] = self.board[initial[0]][initial[1]+1*color_factor]
                                self.board[initial[0]][initial[1]+1*color_factor] = None
                                if not self.check_check(final, self.turn):
                                    self.board[initial[0]][initial[1]] = old_piece
                                    self.board[initial[0]][initial[1]+1*color_factor] = None
                                    self.board[initial[0]][initial[1]+2*color_factor] = None
                                    return True, color_factor*2
                            self.board[initial[0]][initial[1]] = old_piece
                            self.board[initial[0]][initial[1]+1*color_factor] = None
                            self.board[initial[0]][initial[1]+2*color_factor] = None

        return False,

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
                if item and item.color == color and self.move_in_get_moves((i,j), position)[0]:
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

    def check_promotion(self):
        if self.turn == "w":
            for i, piece in enumerate(self.board[0]):
                if piece and piece.type == "p":
                    self.need_promotion = [0, i]
                    return True
        else:
            for i, piece in enumerate(self.board[7]):
                if piece and piece.type == "p":
                    self.need_promotion = [7, i]
                    return True
        return False

    def make_move(self, initial, final, promotion = ""):
        if self.need_promotion:
            if promotion.lower() in self.promotion_pieces:
                self.add_piece(promotion.lower(), self.turn, self.need_promotion)
                self.board[self.need_promotion[0]][self.need_promotion[1]].moved = True
                self.turn = self.board[self.need_promotion[0]][self.need_promotion[1]].enemy
                self.need_promotion = []
                return True, self.check_result(), self.need_promotion
        else:
            check_move = self.check_move(initial, final)
            if self.check_move(initial, final)[0]:
                self.board[final[0]][final[1]] = self.board[initial[0]][initial[1]]
                self.board[initial[0]][initial[1]] = None
                if len(check_move) == 2:
                    if check_move[1] == -1 or check_move[1] == 1:
                        self.board[final[0]+1*check_move[1]][final[1]] = None
                    elif check_move[1] == 2:
                        self.board[initial[0]][initial[1]+1] = self.board[initial[0]][initial[1]+3]
                        self.board[initial[0]][initial[1]+3] = None
                    else:
                        self.board[initial[0]][initial[1]-1] = self.board[initial[0]][initial[1]-4]
                        self.board[initial[0]][initial[1]-4] = None

                #Dealing with first_move attribute for en passant
                for i, row in enumerate(self.board):
                    for j, item in enumerate(row):
                        if item and item.first_move:
                            item.first_move = False
                if not self.board[final[0]][final[1]].moved:
                    self.board[final[0]][final[1]].moved = True
                    self.board[final[0]][final[1]].first_move = True

                if not self.check_promotion():
                    self.turn = self.board[final[0]][final[1]].enemy
                
                return True, self.check_result(), self.need_promotion
        return False, "", self.need_promotion

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
                if (pos[0] * color_factor == 3 or pos[0] * color_factor == -4) and (not self.board[pos[0] - 1 * color_factor][pos[1] - 1]) and self.board[pos[0]][pos[1] - 1] and self.board[pos[0]][pos[1] - 1].color == piece.enemy and self.board[pos[0]][pos[1] - 1].type == "p" and self.board[pos[0]][pos[1] - 1].first_move:
                    moves.append((pos[0] - 1 * color_factor, pos[1] - 1, "ep"))
            if pos[1]+1 <= 7:
                if self.board[pos[0] - 1 * color_factor][pos[1] + 1] and self.board[pos[0] - 1 * color_factor][pos[1] + 1].color == piece.enemy:
                    moves.append((pos[0] - 1 * color_factor, pos[1] + 1))
                if (pos[0] * color_factor == 3 or pos[0] * color_factor == -4) and (not self.board[pos[0] - 1 * color_factor][pos[1] + 1]) and self.board[pos[0]][pos[1] + 1] and self.board[pos[0]][pos[1] + 1].color == piece.enemy and self.board[pos[0]][pos[1] + 1].type == "p" and self.board[pos[0]][pos[1] + 1].first_move:
                    moves.append((pos[0] - 1 * color_factor, pos[1] + 1, "ep"))

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
                if not piece.moved and not self.board[pos[0]][pos[1]-1] and not self.board[pos[0]][pos[1]-2] and not self.board[pos[0]][pos[1]-3] and self.board[pos[0]][pos[1]-4] and not self.board[pos[0]][pos[1]-4].moved:
                    moves.append((pos[0], pos[1]-2, "cl"))
            
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
                if not piece.moved and not self.board[pos[0]][pos[1]+1] and not self.board[pos[0]][pos[1]+2] and self.board[pos[0]][pos[1]+3] and not self.board[pos[0]][pos[1]+3].moved:
                    moves.append((pos[0], pos[1]+2, "cr"))
            
            #Up right
            if pos[0]-1 >= 0 and pos[1]+1 <= 7:
                if not self.board[pos[0]-1][pos[1]+1] or self.board[pos[0]-1][pos[1]+1].color == piece.enemy:
                    moves.append((pos[0]-1, pos[1]+1))

        return moves

    def move_in_get_moves(self, pos, move):
        for item in self.get_moves(pos):
            if move[0] == item[0] and move[1] == item[1]:
                if len(item) == 3:
                    return True, item[2]
                return True,
        return False,

    def get_legal_moves(self, pos):
        moves = self.get_moves(pos)
        final_moves = []
        for move in moves:
            if self.check_move(pos, move)[0]:
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

