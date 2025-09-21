class Make_Unmake:
    
    def __init__(self, board_obj):
        # board_obj is Chess_Board
        self.board_obj = board_obj
        self.board = board_obj.board
        self.has_moved = board_obj.has_moved
        self.color = board_obj.color
        
    def turn(self, row, col):
        if self.board[row][col][0] == "b" and self.color == "b":
            self.color = "b"
            self.color_change()
            return "b"

        elif self.board[row][col][0] == "w" and self.color == "w":
            self.color = "w"
            self.color_change()
            return "w"
        
        else:
            return "n"
        
    
    def color_change(self):
        if self.color == "b":
            self.color = "w"
            return self.color
        elif self.color == "w":
            self.color = "b"
            return self.color

                
    def make_move(self, row, col, new_row, new_col, promotion: str | None = None):
        # Clear en passant target by default (will set if a double pawn push occurs)
        self.board_obj.en_passant_target = None
        if self.board[row][col][0] == "b" and self.color == "b":
            self.check_move(row, col, new_row, new_col, promotion)
            self.color_change()
            return self.board
        elif self.board[row][col][0] == "w" and self.color == "w":
            self.check_move(row, col, new_row, new_col, promotion)
            self.color_change()
            return self.board
        else:
            self.check_move(row, col, new_row, new_col, promotion)
            self.color_change()
            return self.board
                
            
        
    def check_move(self, row, col, new_row, new_col, promotion: str | None = None):
        peice = self.board[row][col]
        self.board[row][col] = "--"
        
        # En passant capture: moving pawn diagonally to empty square that equals en_passant_target
        if peice[1] == "P" and self.board[new_row][new_col] == "--" and col != new_col and self.board_obj.en_passant_target == (new_row, new_col):
            # Capture the pawn that moved two steps last move
            if peice[0] == "w":
                self.board[new_row+1][new_col] = "--"
            else:
                self.board[new_row-1][new_col] = "--"
            self.board[new_row][new_col] = peice
            # Handle promotion after en passant (rare/impossible in standard, but keep consistent)
            if peice[0] == "w" and new_row == 0:
                self.board[new_row][new_col] = "w" + (promotion or "Q")
            elif peice[0] == "b" and new_row == 7:
                self.board[new_row][new_col] = "b" + (promotion or "Q")
            return self.board

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
            # normal move, also handle pawn promotion
            self.board[new_row][new_col] = peice
            if peice[1] == "P":
                # Set en passant target if double advance
                if peice[0] == "w" and row == 6 and new_row == 4 and col == new_col:
                    self.board_obj.en_passant_target = (5, col)
                elif peice[0] == "b" and row == 1 and new_row == 3 and col == new_col:
                    self.board_obj.en_passant_target = (2, col)
                # promotion ranks: black to row 7, white to row 0
                if peice[0] == "b" and new_row == 7:
                    self.board[new_row][new_col] = "b" + (promotion or "Q")
                elif peice[0] == "w" and new_row == 0:
                    self.board[new_row][new_col] = "w" + (promotion or "Q")
        
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
