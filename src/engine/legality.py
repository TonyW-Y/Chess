from chess_utils import Chess_Utils

class Legality:
    
    def __init__(self, board_obj):
        self.board_obj = board_obj            # full Chess_Board
    @property
    def board(self):
        return self.board_obj.board           # always fetch live board
    @property
    def has_moved(self):
        return self.board_obj.has_moved

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
        knight_moves = [(1,2), (1,-2),
                        (2,1), (2,-1),
                        (-1,2), (-1,-2),
                        (-2,1), (-2,-1)]
        piece_color = self.board[row][col][0]
        
        return Chess_Utils.move_noSlide(self.board,knight_moves,piece_color, row, col)
    
    #return valid moves for bishop
    def get_move_bishop(self,row,col):
        bishop_moves = [(1,1), (1,-1), (-1,1), (-1,-1)]
        piece_color = self.board[row][col][0]
        return Chess_Utils.move_slide(self.board,bishop_moves,piece_color, row, col)
    
    #return valid moves for rook
    def get_move_rook(self,row,col):
        rook_moves = [(1,0), (0,1), (-1,0), (0,-1)]
        piece_color = self.board[row][col][0]
        return Chess_Utils.move_slide(self.board,rook_moves,piece_color, row, col)

    
    #return valid moves for queen
    def get_move_queen(self,row,col):
        queen_moves = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        piece_color = self.board[row][col][0]
        return Chess_Utils.move_slide(self.board,queen_moves,piece_color, row, col)


    #return valid king moves
    def get_move_king(self,row,col, include_castle=True):
        king_moves = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        piece_color = self.board[row][col][0]
        valid_moves = Chess_Utils.move_noSlide(self.board,king_moves,piece_color, row, col)
        if include_castle:
            valid_moves += self.get_castle(row, col)
        return valid_moves
    
    #return valid castle moves
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
    #return valid pawn moves
    def get_move_pawn(self,row,col):
        valid_moves = []
        valid_moves += self.basic_pawn(row,col)
        valid_moves += self.two_move_pawn(row,col)
        valid_moves += self.take_pawn(row,col)
        return valid_moves
        
    #return basic pawn moves(move forward by 1)
    def basic_pawn(self,row,col):
        piece_color = self.board[row][col][0]
        if piece_color == "b":
            pawn_moves = [(1,0)]
        elif piece_color == "w":
            pawn_moves = [(-1,0)]
        return Chess_Utils.move_pawn(self.board,pawn_moves, row, col)

    #return starting pawn moves(move forward by 2)
    def two_move_pawn(self,row,col):
        piece_color = self.board[row][col][0]
        if piece_color == "b":
            pawn_moves = [(2,0)]
            if row == 1:
                return Chess_Utils.move_pawn(self.board,pawn_moves, row, col)
        elif piece_color == "w":
            pawn_moves = [(-2,0)]
            if row == 6:
                return Chess_Utils.move_pawn(self.board,pawn_moves, row, col)
        return []
    
    #return pawn capturing moves
    def take_pawn(self,row,col):
        piece_color = self.board[row][col][0]
        if piece_color == "b":
            pawn_moves = [(1,1),(1,-1)]
            return Chess_Utils.pawn_capture(self.board, pawn_moves, piece_color, row, col)
        elif piece_color == "w":
            pawn_moves = [(-1,1),(-1,-1)]
            return Chess_Utils.pawn_capture(self.board, pawn_moves, piece_color, row, col)
        return []

    def is_check(self, color):
        king_pos = None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == color + "K":
                    king_pos = (row,col)
                    break
        
        if color == "b":
            enemy_color = "w"
        else:
            enemy_color = "b"
            
        
        
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != "--" and self.board[row][col][0] == enemy_color:
                    enemy_moves = self.get_move_king(row, col, include_castle=False)
                    if king_pos in enemy_moves:
                        return True
        return False
        
    def filter_move(self, row, col):
        moves = self.get_legal_moves(row,col)
        color = self.board[row][col][0]
        legal_moves = []
        for i in range(len(moves)):
            self.board_obj.save_move(row, col, moves[i][0], moves[i][1])
    
            if not self.is_check(color):
                legal_moves.append(moves[i])
            self.board_obj.undo_move()
        return legal_moves
    

    