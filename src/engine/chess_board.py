import copy
from legality import Legality
from chess_utils import Chess_Utils
from make_unmake import Make_Unmake
class Chess_Board:
    def __init__(self):
        #starting board
        self.board = [
            ["--","--","--","--","bK","--","--","bR"], 
            ["bP","bP","bP","bP","bP","bP","bP","bP"], 
            ["--","--","--","--","--","wP","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"], 
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        
        #board history
        self.history = []
        
        #R1 is queen side rook
        #R2 is king side rook
        self.has_moved = {"bR1":0, "bR2":0, "bK":0,
                          "wR1":0, "wR2":0, "wK":0
                          }
    
    #print the chess board
    def __str__(self):
        return "\n".join(" ".join(self.board[row]) for row in range(len(self.board)))
    
    
    def save_move(self, row, col, new_row, new_col):
        move = Make_Unmake(self.board, self.has_moved)
        (self.history).append(copy.deepcopy(self.board))
        self.board = move.make_move(row, col, new_row, new_col)
        return self.board
    
    def undo_move(self):
        self.history.pop()
        if self.history:
            self.board = self.history[-1]
        return self.board
    
    
"""board = Chess_Board()
legal = Legality(board.board, board.has_moved)
print(legal.get_legal_moves(1,4))"""