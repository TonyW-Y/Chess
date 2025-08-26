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

print("Move black pawn (1,4) -> (2,4):")
engine.play_turn(1, 4, 2, 4)
print_board(board)

print("Move white knight (7,6) -> (5,5):")
engine.play_turn(7, 6, 5, 5)
print_board(board)

print("Move black knight (0,6) -> (2,5):")
engine.play_turn(0, 6, 2, 5)
print_board(board)
