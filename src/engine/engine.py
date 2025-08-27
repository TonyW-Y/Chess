from legality import Legality
from make_unmake import Make_Unmake
from chess_utils import Chess_Utils

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