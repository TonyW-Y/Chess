from engine import Engine
from chess_board import Chess_Board

board = Chess_Board()
engine = Engine(board)

engine.play_turn(1, 4, 2, 5)
engine.play_turn(6,4,4,4)

for row in range(len(board.board)):
    for col in range(len(board.board)):
        print(f"{board.board[row][col]} ", end="")
    print()