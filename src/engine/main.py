from chess_board import Chess_Board
from engine import Engine

def print_board(board):
    for row in board.board:  # board.board is your 2D list
        print(" ".join(row))
    print("\n")

# Setup
board = Chess_Board()
engine = Engine(board)

print("Initial position:")
print_board(board)

# Test moves
print("Move white pawn (6,4) -> (5,4):")
engine.play_turn(6, 4, 4, 4)
print_board(board)

print("Move black pawn (1,4) -> (2,4):")
engine.play_turn(1, 4, 3, 4)
print_board(board)

print("Move white knight (7,6) -> (5,5):")
engine.play_turn(6, 5, 4, 5)
print_board(board)

moves = engine.legality.get_legal_moves(0,3)
print("moves",moves)
print("Move black knight (0,6) -> (2,5):")
engine.play_turn(0, 3, 4, 7)
print_board(board)

