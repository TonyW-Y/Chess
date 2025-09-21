import pygame
import sys
import os

# Ensure engine package is importable when running this file directly
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from engine.chess_board import Chess_Board
from engine.engine import Engine


def main():
    game_window()


def game_window():
    pygame.init()

    screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Chess Game")

    # Initialize engine and board
    board = Chess_Board()
    engine = Engine(board)
    game_over = False
    winner = None           # 'w' or 'b' (or None)
    status = "in_progress"
    clock = pygame.time.Clock()

    # Piece dragging/selection state
    selected_piece = None
    selected_pos = None
    legal_moves = []

    # Load piece images (robust path handling)
    piece_images = load_piece_images()

    # End-screen fade animation (0→200)
    animation_alpha = 0

    running = True
    while running:
        clock.tick(60)
        screen.fill((255, 255, 255))

        width, height = screen.get_size()
        board_size = int(min(width, height) * 0.8)
        square_size = board_size / 8
        board_start_x = (width - board_size) / 2
        board_start_y = (height - board_size) / 2

        chess_squares(screen)
        draw_chess_pieces(
            screen,
            engine.board.board,
            piece_images,
            board_start_x,
            board_start_y,
            square_size
        )

        # Highlight legal moves for selected piece
        if selected_piece and legal_moves:
            highlight_legal_moves(
                screen, legal_moves, board_start_x, board_start_y, square_size
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over:
                # Handle end-screen interactions
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    btn_w, btn_h = 160, 44
                    center_x, base_y = width // 2, int(height * 0.6)
                    restart_rect = pygame.Rect(center_x - btn_w - 10, base_y, btn_w, btn_h)
                    quit_rect = pygame.Rect(center_x + 10, base_y, btn_w, btn_h)

                    if restart_rect.collidepoint(mx, my):
                        # Reset game
                        board = Chess_Board()
                        engine = Engine(board)
                        game_over = False
                        winner = None
                        status = "in_progress"
                        selected_piece = None
                        selected_pos = None
                        legal_moves = []
                        animation_alpha = 0
                    elif quit_rect.collidepoint(mx, my):
                        running = False

            else:
                # ---- Gameplay input (only when not game over) ----
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    col = int((mx - board_start_x) // square_size)
                    row = int((my - board_start_y) // square_size)
                    if 0 <= row < 8 and 0 <= col < 8:
                        piece = engine.board.board[row][col]
                        if piece != "--" and piece[0] == engine.board.color:
                            selected_piece = piece
                            selected_pos = (row, col)
                            legal_moves = engine.legality.filter_move(row, col)
                        else:
                            selected_piece = None
                            selected_pos = None
                            legal_moves = []

                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_piece and selected_pos:
                        mx, my = pygame.mouse.get_pos()
                        col = int((mx - board_start_x) // square_size)
                        row = int((my - board_start_y) // square_size)

                        if 0 <= row < 8 and 0 <= col < 8 and (row, col) in legal_moves:
                            from_row, from_col = selected_pos
                            ok, _msg = engine.play_turn(from_row, from_col, row, col)

                            # Check game status immediately after a successful move
                            if ok:
                                current_status, win_info = engine.get_game_status()
                                if current_status != "in_progress":
                                    game_over = True
                                    winner = win_info
                                    status = current_status

                        # Clear selection state regardless
                        selected_piece = None
                        selected_pos = None
                        legal_moves = []

        # Draw end screen (with fade-in) if game is over
        if game_over:
            animation_alpha = min(animation_alpha + 12, 200)  # fade in
            draw_end_screen(screen, status, winner, animation_alpha)

        pygame.display.update()

    pygame.quit()


def chess_squares(screen):
    width, height = screen.get_size()
    board_size = min(width, height) * 0.8
    square_size = board_size / 8
    board_start_x = (width - board_size) / 2
    board_start_y = (height - board_size) / 2

    pygame.draw.rect(
        screen,
        (101, 67, 33),
        (board_start_x - 20, board_start_y - 20, board_size + 40, board_size + 40),
    )

    for row in range(8):
        for col in range(8):
            color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
            x = int(round(board_start_x + col * square_size))
            y = int(round(board_start_y + row * square_size))
            pygame.draw.rect(screen, color, (x, y, int(round(square_size)), int(round(square_size))))

    coordinates(board_start_x, board_start_y, square_size, screen)


def load_piece_images():
    """
    Tries a couple of common asset paths. Falls back to a magenta placeholder if missing.
    """
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    images = {}
    for piece in pieces:
        candidates = [
            os.path.join(PARENT_DIR, "assets", f"{piece}.png"),
            os.path.join(CURRENT_DIR, "..", "..", "assets", f"{piece}.png"),
            os.path.join(CURRENT_DIR, "assets", f"{piece}.png"),
        ]
        path = next((p for p in candidates if os.path.exists(p)), candidates[0])
        try:
            images[piece] = pygame.image.load(path)
        except Exception as e:
            print(f"[assets] Error loading {piece} at {path}: {e}")
            surf = pygame.Surface((40, 40))
            surf.fill((255, 0, 255))  # Bright placeholder
            images[piece] = surf
    return images


def highlight_legal_moves(screen, moves, board_start_x, board_start_y, square_size):
    # draw semi-transparent indicators on an alpha surface
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    r = int(square_size / 6)
    for (rr, cc) in moves:
        cx = int(board_start_x + cc * square_size + square_size / 2)
        cy = int(board_start_y + rr * square_size + square_size / 2)
        pygame.draw.circle(overlay, (0, 255, 0, 110), (cx, cy), r)
    screen.blit(overlay, (0, 0))


def draw_chess_pieces(screen, board_state, images, board_start_x, board_start_y, square_size):
    for r in range(8):
        for c in range(8):
            piece = board_state[r][c]
            if piece != "--":
                img = images.get(piece)
                if img:
                    scaled = pygame.transform.scale(img, (int(square_size), int(square_size)))
                    x = int(board_start_x + c * square_size)
                    y = int(board_start_y + r * square_size)
                    screen.blit(scaled, (x, y))


def draw_end_screen(screen, status, winner, alpha=180):
    width, height = screen.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, int(alpha)))  # semi-transparent dark overlay
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("timesnewroman", 48, bold=True)
    sub_font = pygame.font.SysFont("timesnewroman", 24)

    if status == "checkmate":
        win_text = f"Checkmate! {'White' if winner == 'w' else 'Black'} wins"
    elif status == "stalemate":
        win_text = "Stalemate! Draw"
    else:
        win_text = "Game Over"

    title_surf = title_font.render(win_text, True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(width // 2, int(height * 0.4)))
    screen.blit(title_surf, title_rect)

    # Buttons
    btn_w, btn_h = 160, 44
    center_x = width // 2
    base_y = int(height * 0.6)
    restart_rect = pygame.Rect(center_x - btn_w - 10, base_y, btn_w, btn_h)
    quit_rect = pygame.Rect(center_x + 10, base_y, btn_w, btn_h)

    def draw_button(rect, text, mouse_pos):
        hovered = rect.collidepoint(mouse_pos)
        bg = (240, 240, 240) if hovered else (220, 220, 220)
        border = (100, 100, 100) if hovered else (80, 80, 80)
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        pygame.draw.rect(screen, border, rect, 2, border_radius=8)
        label = sub_font.render(text, True, (20, 20, 20))
        screen.blit(label, label.get_rect(center=rect.center))

    mouse_pos = pygame.mouse.get_pos()
    draw_button(restart_rect, "Restart", mouse_pos)
    draw_button(quit_rect, "Quit", mouse_pos)


def coordinates(board_start_x, board_start_y, square_size, screen):
    # file/rank labels
    font = pygame.font.SysFont("timesnewroman", 17)
    for row in range(8):
        if row in (0, 7):
            for col in range(ord("a"), ord("h") + 1):
                text_surface = font.render(chr(col), True, (255, 255, 255))
                x = board_start_x + square_size * (col - ord("a")) + square_size / 2
                if row == 0:
                    screen.blit(text_surface, (x, board_start_y - 20))
                else:
                    screen.blit(text_surface, (x, board_start_y + 8 * square_size))
        else:
            for col in range(8):
                n = col + 1
                text_surface = font.render(str(9 - n), True, (255, 255, 255))
                screen.blit(
                    text_surface,
                    (board_start_x - 14, board_start_y + n * square_size - 10 - square_size / 2),
                )
                screen.blit(
                    text_surface,
                    (
                        board_start_x + square_size * 8 + 6,
                        board_start_y + n * square_size - 10 - square_size / 2,
                    ),
                )


if __name__ == "__main__":
    main()
