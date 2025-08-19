import pygame
import chess
import sys

def main():
    game_window()

def game_window():
    pygame.init()

    screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Game")


    running = True
    while running:
        screen.fill((255, 255, 255))
        chess_squares(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()



def chess_squares(screen):
    width, height = screen.get_size()
    board_size = min(width, height) * 0.8
    square_size = board_size / 8
    board_start_x = (width - board_size) / 2
    board_start_y = (height - board_size) / 2

    pygame.draw.rect(screen, (101, 67, 33), (board_start_x - 20, board_start_y - 20, board_size + 40, board_size + 40))
    
    for row in range(8):
        for col in range(8):
        # Alternate colors
            if (row + col) % 2 == 0:
                color = (240, 217, 181)  # light
            else:
                color = (181, 136, 99)   # dark

            # Calculate square position
            x = round(board_start_x + col * square_size)
            y = round(board_start_y + row * square_size)

            pygame.draw.rect(screen, color, (x, y, round(square_size), round(square_size)))
     
    coordinates(board_start_x, board_start_y, square_size, screen)
    draw_chess_pieces(board_start_x, board_start_y, square_size, screen)

def coordinates(board_start_x, board_start_y, square_size, screen):
    for row in range(8):
        font = pygame.font.SysFont("timesnewroman", 17)
        if row == 0 or row == 7:
            for col in range(ord('a'), ord('h') + 1):
                text_surface = font.render(chr(col), True, (255,255,255))
                if row == 0:
                    screen.blit(text_surface, (board_start_x + square_size*(col - ord('a')) + square_size/2, board_start_y-20))
                else:
                    screen.blit(text_surface, (board_start_x + square_size*(col - ord('a')) + square_size/2, board_start_y + 8*square_size))
        else:
            for col in range(8):
                col += 1
                text_surface = font.render(str(9-col), True, (255,255,255))
                screen.blit(text_surface, (board_start_x - 14, board_start_y + col*square_size-10-square_size/2))
                screen.blit(text_surface, (board_start_x + square_size*8+6, board_start_y + col*square_size-10-square_size/2))

    
def draw_chess_pieces(board_start_x, board_start_y, square_size, screen):
    board = chess.Board()
    PIECE_IMAGES = {"wP": pygame.image.load("assets/wP.png"),
                    "wN": pygame.image.load("assets/wN.png"),
                    "wB": pygame.image.load("assets/wB.png"),
                    "wR": pygame.image.load("assets/wR.png"),
                    "wQ": pygame.image.load("assets/wQ.png"),
                    "wK": pygame.image.load("assets/wK.png"),
                    "bP": pygame.image.load("assets/bP.png"),
                    "bN": pygame.image.load("assets/bN.png"),
                    "bB": pygame.image.load("assets/bB.png"),
                    "bR": pygame.image.load("assets/bR.png"),
                    "bQ": pygame.image.load("assets/bQ.png"),
                    "bK": pygame.image.load("assets/bK.png")}
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)  # white at bottom
            piece = board.piece_at(square)
            if piece:
                image = PIECE_IMAGES[piece.symbol()]
                x = board_start_x + col * square_size
                y = board_start_y + row * square_size
                screen.blit(image, (x, y))
 

    screen.blit(image, (board_start_x - 14, board_start_y + square_size-10-square_size/2))

if __name__ == "__main__":
    main()