class Chess:
    def __init__(self):
        self.board = [
            ["--","--","--","--","bK","--","--","bR"], 
            ["bP","bP","bP","bP","bP","bP","bP","bP"], 
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"], 
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        #R1 is queen side rook
        #R2 is king side rook
        self.has_moved = {"bR1":0, "bR2":0, "bK":0,
                          "wR1":0, "wR1":0, "wK":0
                          }
    
    #print the chess board
    def __str__(self):
        return "\n".join(" ".join(self.board[row]) for row in range(len(self.board)))
    

    def get_legal_moves(self, row, col):
        piece = self.board[row][col]
        if piece == "--":
            return []
        elif piece[1] == "P":
            return self.get_move_pawn(row,col)
        elif piece[1] == "R":
            return self.get_move_rook(row,col)
        elif piece[1] == "N":
            return self.get_move_knight(row,col)
        elif piece[1] == "B":
            return self.get_move_bishop(row,col)
        elif piece[1] == "Q":
            return self.get_move_queen(row,col)
        elif piece[1] == "K":
            return self.get_move_king(row,col)
    
    #return valid moves for knight
    def get_move_knight(self, row, col):
        valid_moves = []
        knight_moves = [(1,2), (1,-2),
                        (2,1), (2,-1),
                        (-1,2), (-1,-2),
                        (-2,1), (-2,-1)]
        piece_color = self.board[row][col][0]
        
        for i in range(len(knight_moves)):
            new_row = row+knight_moves[i][0]
            new_col = col+knight_moves[i][1]
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                if self.board[new_row][new_col] == "--":
                    (valid_moves).append((new_row, new_col))

                elif self.board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                elif self.board[new_row][new_col][0] == piece_color:
                    pass
        return valid_moves
    
    #return valid moves for bishop
    def get_move_bishop(self,row,col):
        valid_moves = []
        bishop_moves = [(1,1), (1,-1), (-1,1), (-1,-1)]
        piece_color = self.board[row][col][0]
        for i in range(len(bishop_moves)):
            new_row = row+bishop_moves[i][0]
            new_col = col+bishop_moves[i][1]
            while True:

                if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]) and self.board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                    if self.board[new_row][new_col][0] != piece_color and self.board[new_row][new_col] != "--":
                        break
                    
                else:
                    break
                new_row = new_row+bishop_moves[i][0]
                new_col = new_col+bishop_moves[i][1]
        return valid_moves
    
    #return valid moves for rook
    def get_move_rook(self,row,col):
        valid_moves = []
        rook_moves = [(1,0), (0,1), (-1,0), (0,-1)]
        piece_color = self.board[row][col][0]
        for i in range(len(rook_moves)):
            new_row = row+rook_moves[i][0]
            new_col = col+rook_moves[i][1]
            while True:

                if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]) and self.board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                    if self.board[new_row][new_col][0] != piece_color and self.board[new_row][new_col] != "--":
                        break
                    
                else:
                    break
                new_row = new_row+rook_moves[i][0]
                new_col = new_col+rook_moves[i][1]
        return valid_moves
    
    #return valid moves for queen
    def get_move_queen(self,row,col):
        valid_moves = []
        queen_moves = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        piece_color = self.board[row][col][0]
        for i in range(len(queen_moves)):
            new_row = row+queen_moves[i][0]
            new_col = col+queen_moves[i][1]
            while True:

                if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]) and self.board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                    if self.board[new_row][new_col][0] != piece_color and self.board[new_row][new_col] != "--":
                        break
                    
                else:
                    break
                new_row = new_row+queen_moves[i][0]
                new_col = new_col+queen_moves[i][1]
        return valid_moves

    #return valid king moves
    def get_move_king(self,row,col):
        valid_moves = []
        king_moves = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        piece_color = self.board[row][col][0]
        for i in range(len(king_moves)):
            new_row = row+king_moves[i][0]
            new_col = col+king_moves[i][1]
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                if self.board[new_row][new_col] == "--":
                    (valid_moves).append((new_row, new_col))
                elif self.board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                elif self.board[new_row][new_col][0] == piece_color:
                    pass
        valid_moves.append(self.get_castle(row,col))
        return valid_moves
    
    def get_castle(self,row,col):
        valid_moves = []
        piece_color = self.board[row][col][0]
        if piece_color == "b":
            if self.has_moved["bK"] == 0 and self.has_moved["bR1"] == 0: #R1 is queen side rook
                if self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--":
                    valid_moves.append((0,2))
                    
            if self.has_moved["bK"] == 0 and self.has_moved["bR2"] == 0: #R2 is king side rook
                if self.board[0][5] == "--" and self.board[0][6] == "--":
                    valid_moves.append((0,6))
        if piece_color == "w":  
            if self.has_moved["wK"] == 0 and self.has_moved["wR1"] == 0: #R1 is queen side rook
                if self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--":
                    valid_moves.append((7,2))
                
            if self.has_moved["wK"] == 0 and self.has_moved["wR2"] == 0: #R2 is king side rook
                if self.board[7][5] == "--" and self.board[7][6] == "--":
                    valid_moves.append((7,6))
            
        return valid_moves

    def get_move_pawn(self,row,col):
        valid_moves = []
        pawn_moves = [(1,0),(-1,0)]
        piece_color = self.board[row][col][0]
        for i in range(len(pawn_moves)):
            new_row = row+pawn_moves[i][0]
            new_col = col+pawn_moves[i][1]
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                if self.board[new_row][new_col] == "--":
                    (valid_moves).append((new_row, new_col))

                elif self.board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                elif self.board[new_row][new_col][0] == piece_color:
                    pass
        return valid_moves
        
        
        
chess = Chess()
moves = chess.get_legal_moves(1, 4)
print(moves)