import copy
from .make_unmake import Make_Unmake
from .legality import Legality

class Chess_Board:
    def __init__(self):
        #starting board
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"], 
            ["bP","bP","bP","bP","bP","bP","bP","bP"], 
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"], 
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.color = "w"
        #board history
        self.history = []
        # en passant target square (row, col) valid only for the immediate next move
        self.en_passant_target = None
        
        #R1 is queen side rook
        #R2 is king side rook
        self.has_moved = {"bR1":0, "bR2":0, "bK":0,
                          "wR1":0, "wR2":0, "wK":0
                          }
    
    #print the chess board
    def __str__(self):
        return "\n".join(" ".join(self.board[row]) for row in range(len(self.board)))
    
    
    def save_move(self, row, col, new_row, new_col, promotion: str | None = None):
        move = Make_Unmake(self)  # pass board object for full state access
        (self.history).append((copy.deepcopy(self.board), copy.deepcopy(self.has_moved), self.color, self.en_passant_target))
        self.board = move.make_move(row, col, new_row, new_col, promotion)
        self.color = move.color
        return self.board
    
    def undo_move(self):
        if self.history:
            last_board, last_has_moved, last_color, last_ep = self.history.pop()
            self.board = last_board
            self.has_moved = last_has_moved
            self.color = last_color
            self.en_passant_target = last_ep
        return self.board
    
if __name__ == "__main__": 
    board = Chess_Board()
    legal = Legality(board)
    print(legal.get_legal_moves(0, 3))
    print(legal.get_legal_moves(7, 3))