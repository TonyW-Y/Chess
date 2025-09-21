from .chess_utils import Chess_Utils

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
            # Only add castle squares that are not through check and king not in check
            for r,c in self.get_castle(row, col):
                # Determine intermediate squares the king passes through (including destination)
                path = []
                if c == 6:  # king side
                    path = [(row, 5), (row, 6)]
                elif c == 2:  # queen side
                    path = [(row, 3), (row, 2)]
                color = piece_color
                # King cannot castle out of, through, or into check
                if not self.is_square_attacked(color, (row, col)) and all(not self.is_square_attacked(color, sq) for sq in path):
                    valid_moves.append((r, c))
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
                # both intermediate and destination must be empty
                if self.board[row+1][col] == "--" and self.board[row+2][col] == "--":
                    return [(row+2, col)]
        elif piece_color == "w":
            pawn_moves = [(-2,0)]
            if row == 6:
                if self.board[row-1][col] == "--" and self.board[row-2][col] == "--":
                    return [(row-2, col)]
        return []
    
    #return pawn capturing moves
    def take_pawn(self,row,col):
        piece_color = self.board[row][col][0]
        if piece_color == "b":
            pawn_moves = [(1,1),(1,-1)]
            moves = Chess_Utils.pawn_capture(self.board, pawn_moves, piece_color, row, col)
            # en passant: target square is one rank down and diagonal
            ep = self.board_obj.en_passant_target
            if ep:
                for dc in (1, -1):
                    r, c = row + 1, col + dc
                    if 0 <= c < 8 and ep == (r, c) and self.board[r][c] == "--" and self.board[row][c] == "wP":
                        moves.append((r, c))
            return moves
        elif piece_color == "w":
            pawn_moves = [(-1,1),(-1,-1)]
            moves = Chess_Utils.pawn_capture(self.board, pawn_moves, piece_color, row, col)
            ep = self.board_obj.en_passant_target
            if ep:
                for dc in (1, -1):
                    r, c = row - 1, col + dc
                    if 0 <= c < 8 and ep == (r, c) and self.board[r][c] == "--" and self.board[row][c] == "bP":
                        moves.append((r, c))
            return moves
        return []

    def is_check(self, color):
        # Find king position
        king_pos = None
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == color + "K":
                    king_pos = (r, c)
                    break
            if king_pos:
                break
        if king_pos is None:
            return False
        return self.is_square_attacked(color, king_pos)

    def is_square_attacked(self, color, square):
        # Returns True if square for side `color` is attacked by opponent
        enemy = "w" if color == "b" else "b"
        rK, cK = square
        # Check knight attacks
        knight_moves = [(1,2), (1,-2), (2,1), (2,-1), (-1,2), (-1,-2), (-2,1), (-2,-1)]
        for dr, dc in knight_moves:
            r, c = rK + dr, cK + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == enemy + "N":
                return True
        # Check king adjacency (for completeness, not for castle)
        king_moves = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dr, dc in king_moves:
            r, c = rK + dr, cK + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == enemy + "K":
                return True
        # Check rook/queen lines
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            r, c = rK + dr, cK + dc
            while 0 <= r < 8 and 0 <= c < 8:
                sq = self.board[r][c]
                if sq != "--":
                    if sq[0] == enemy and (sq[1] == "R" or sq[1] == "Q"):
                        return True
                    break
                r += dr
                c += dc
        # Check bishop/queen diagonals
        for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            r, c = rK + dr, cK + dc
            while 0 <= r < 8 and 0 <= c < 8:
                sq = self.board[r][c]
                if sq != "--":
                    if sq[0] == enemy and (sq[1] == "B" or sq[1] == "Q"):
                        return True
                    break
                r += dr
                c += dc
        # Check pawn attacks (white pawns attack up: row-1; black pawns attack down: row+1)
        pawn_dirs = [(-1,1), (-1,-1)] if enemy == "w" else [(1,1), (1,-1)]
        for dr, dc in pawn_dirs:
            r, c = rK + dr, cK + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == enemy + "P":
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

    def get_all_legal_moves_for_color(self, color):
        """Return a list of all legal moves for the side to move `color`.
        Each move is represented as a tuple: (row, col, new_row, new_col).
        """
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "--" and piece[0] == color:
                    for nr, nc in self.filter_move(r, c):
                        moves.append((r, c, nr, nc))
        return moves

    def is_checkmate(self, color):
        """Return True if `color` is currently checkmated."""
        # If there are any legal moves, it's not mate
        if self.get_all_legal_moves_for_color(color):
            return False
        # No legal moves: if in check, it's checkmate
        return self.is_check(color)

    def is_stalemate(self, color):
        """Return True if `color` is stalemated (no legal moves and not in check)."""
        if self.get_all_legal_moves_for_color(color):
            return False
        return not self.is_check(color)