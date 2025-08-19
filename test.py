import chess

# Create a new board
board = chess.Board()

# Play a few moves
board.push_san("e4")
board.push_san("e5")
board.push_san("Nf3")
board.push_san("Nc6")

# Check if the game is over or in checkmate
if board.is_checkmate():
    print("Checkmate!")
elif board.is_stalemate():
    print("Stalemate!")
else:
    print("Game in progress.")

# Print the current board
print(board)