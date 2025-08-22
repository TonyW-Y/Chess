from legality import Legality
from chess_utils import Chess_Utils


class Make_Unmake:
    
    def __init__(self, board, has_moved):
        self.board = board
        self.has_moved = has_moved
        self.color = "b"
        
    def turn(self):
        return self.color
        
    def make_move(self, row, col, new_row, new_col):
        if self.board[row][col][0] == "b" and self.color == "b":
            self.check_move(row, col, new_row, new_col)
            self.color = "w"
            return self.board
        elif self.board[row][col][0] == "w" and self.color == "w":
            self.check_move(row, col, new_row, new_col)
            self.color = "b"
            return self.board
        else:
            return self.board

                
            
        
    def check_move(self, row, col, new_row, new_col):
        peice = self.board[row][col]
        self.board[row][col] = "--"
        
        if self.board[new_row][new_col] != "--":
            captured = self.board[new_row][new_col] 
            self.board[new_row][new_col] = peice
                
        elif peice[1] == "K":
            if abs(new_col-col) == 2:
                self.check_castle(peice, row, col, new_row, new_col)
            else:
                if peice[0] == "b":
                    self.board[new_row][new_col] = peice
                    self.has_moved["bK"] = 1
                elif peice[0] == "w":
                    self.board[new_row][new_col] = peice
                    self.has_moved["wK"] = 1
        elif peice[1] == "R":
            self.check_rook(peice, row, col, new_row, new_col)
            
        else:
            self.board[new_row][new_col] = peice
        
        return self.board
        
    def check_castle(self, peice, row, col, new_row, new_col):
        
        if peice[0] == "b":
            if self.has_moved["bK"] == 0 and self.has_moved["bR1"] == 0 and new_col - col == -2:
                self.board[0][0] = "--"
                self.board[new_row][new_col] = peice
                self.board[0][3] = "bR"
                self.has_moved["bK"] = 1
                self.has_moved["bR1"] = 1
            elif self.has_moved["bK"] == 0 and self.has_moved["bR2"] == 0 and new_col - col == 2:
                self.board[0][7] = "--"
                self.board[new_row][new_col] = peice
                self.board[0][5] = "bR"
                self.has_moved["bK"] = 1
                self.has_moved["bR2"] = 1
                
            
        elif peice[0] == "w":
            if self.has_moved["wK"] == 0 and self.has_moved["wR1"] == 0 and new_col - col == -2:
                self.board[7][0] = "--"
                self.board[new_row][new_col] = peice
                self.board[7][3] = "wR"
                self.has_moved["wK"] = 1
                self.has_moved["wR1"] = 1
            elif self.has_moved["wK"] == 0 and self.has_moved["wR2"] == 0 and new_col - col == 2:
                self.board[7][7] = "--"
                self.board[new_row][new_col] = peice
                self.board[7][5] = "wR"
                self.has_moved["wK"] = 1
                self.has_moved["wR2"] = 1
    
    def check_rook(self, peice, row, col, new_row, new_col):
        if peice[0] == "b":
            if self.has_moved["bR1"] == 0 and col == 0:
                self.board[new_row][new_col] = peice
                self.has_moved["bR1"] = 1
                
            elif self.has_moved["bR2"] == 0 and col == 7:
                self.board[new_row][new_col] = peice
                self.has_moved["bR2"] = 1
            else:
                self.board[new_row][new_col] = peice
            
        elif peice[0] == "w":     
            if self.has_moved["wR1"] == 0 and col == 0:
                self.board[new_row][new_col] = peice
                self.has_moved["wR1"] = 1
                
            elif self.has_moved["wR2"] == 0 and col == 7:
                self.board[new_row][new_col] = peice
                self.has_moved["wR2"] = 1  
            else:
                self.board[new_row][new_col] = peice 
                    
        return self.board
