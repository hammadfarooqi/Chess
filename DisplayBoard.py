import pygame
import sys
from BoardObject import *
from pygame.locals import *

pygame.init()

win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

pieces_img = pygame.image.load('PieceImages.png').convert_alpha()
pieces_dict = {
    " wk ": pygame.transform.scale(pieces_img.subsurface((0, 0, 200, 200)), (100, 100)),
    " wq ": pygame.transform.scale(pieces_img.subsurface((200, 0, 200, 200)), (100, 100)),
    " wb ": pygame.transform.scale(pieces_img.subsurface((400, 0, 200, 200)), (100, 100)),
    " wn ": pygame.transform.scale(pieces_img.subsurface((600, 0, 200, 200)), (100, 100)),
    " wr ": pygame.transform.scale(pieces_img.subsurface((800, 0, 200, 200)), (100, 100)),
    " wp ": pygame.transform.scale(pieces_img.subsurface((1000, 0, 200, 200)), (100, 100)),
    " bk ": pygame.transform.scale(pieces_img.subsurface((0, 200, 200, 200)), (100, 100)),
    " bq ": pygame.transform.scale(pieces_img.subsurface((200, 200, 200, 200)), (100, 100)),
    " bb ": pygame.transform.scale(pieces_img.subsurface((400, 200, 200, 200)), (100, 100)),
    " bn ": pygame.transform.scale(pieces_img.subsurface((600, 200, 200, 200)), (100, 100)),
    " br ": pygame.transform.scale(pieces_img.subsurface((800, 200, 200, 200)), (100, 100)),
    " bp ": pygame.transform.scale(pieces_img.subsurface((1000, 200, 200, 200)), (100, 100))    
}

def refresh(board, need_promotion):
    win.fill((210, 180, 140))
    for i, row in enumerate(board.board):
        for j, item in enumerate(row):
            if (i+j) % 2 != 0:
                win.fill((150, 75, 0), (j*100, i*100, 100, 100))
            if str(item) != 'None':
                win.blit(pieces_dict[str(item)], (j*100, i*100))
    if need_promotion:
        win.fill((255, 255, 255), (175, 275, 450, 150))
        win.blit((pieces_dict[" wn "]), (200, 300))
        win.blit((pieces_dict[" wb "]), (300, 300))
        win.blit((pieces_dict[" wr "]), (400, 300))
        win.blit((pieces_dict[" wq "]), (500, 300))
    pygame.display.update()

if __name__=='__main__':
    normal = Board()
    normal.new_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    initial = (0, 0)
    final = (0, 0)
    need_promotion = False
    
    play = True
    while play:
        refresh(normal, need_promotion)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            real_pos = (pos[1]//100, pos[0]//100)
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                initial = real_pos
            if event.type == MOUSEBUTTONUP:
                final = real_pos
                
                promotion = ""
                if need_promotion and final[0] == 3:
                    match final[1]:
                        case 2:
                            promotion = "n"
                        case 3:
                            promotion = "b"
                        case 4:
                            promotion = "r"
                        case 5:
                            promotion = "q"
                move_result = normal.make_move(initial, final, promotion)
                need_promotion = move_result[2]
                if move_result[1]:
                    print(move_result[1]+" lost!")
                    play = False
                    break
                if not move_result[0]:
                    print("invalid move")

        
        

    