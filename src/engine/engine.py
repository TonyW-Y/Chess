from legality import Legality
from make_unmake import Make_Unmake
from chess_utils import Chess_Utils
from chess_board import Chess_Board


class Engine:
    def __init__(self, board):
        self.board = board
        self.has_moved = board.has_moved
        self.legality = Legality(self.board)
        self.utils = Chess_Utils()
    
    def play_turn(self, row, col, new_row, new_col):
        legal_moves = self.legality.filter_move(row,col)
        
        if (new_row, new_col) in legal_moves:
            move_color = self.board.color
            make_unmake = Make_Unmake(self.board.board, self.board.has_moved, move_color)
            if make_unmake.turn(row, col) == self.board.board[row][col][0]:
                self.board.save_move(row, col, new_row, new_col)
                print("move made!")
            elif make_unmake.turn(row, col) == "n":
                print("wat")
            
            else:
                print("not your turn!")
        else:
            print("not a legal move!")
        
    def undo(self):
        self.board.undo_move()
        
if __name__ == "__main__":
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
    engine.play_turn(6, 4, 5, 4)
    print_board(board)

    print("Move black pawn (1,4) -> (2,4):")
    engine.play_turn(1, 4, 2, 4)
    print_board(board)


    print(engine.legality.get_legal_moves(7,3))

    print(engine.legality.get_legal_moves(0,3))


