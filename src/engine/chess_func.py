class ChessUtils:
    def move_noSlide(board, piece_move, piece_color, row, col):
        valid_moves = []        
        for i in range(len(piece_move)):
            new_row = row+piece_move[i][0]
            new_col = col+piece_move[i][1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                if board[new_row][new_col] == "--":
                    (valid_moves).append((new_row, new_col))
                elif board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                elif board[new_row][new_col][0] == piece_color:
                    pass
        return valid_moves
    
    def move_slide(board, piece_move, piece_color, row, col):
        valid_moves = []        
        for i in range(len(piece_move)):
            new_row = row+piece_move[i][0]
            new_col = col+piece_move[i][1]
            while True:

                if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col][0] != piece_color:
                    (valid_moves).append((new_row, new_col))
                    if board[new_row][new_col][0] != piece_color and board[new_row][new_col] != "--":
                        break
                    
                else:
                    break
                new_row = new_row+piece_move[i][0]
                new_col = new_col+piece_move[i][1]
        return valid_moves
        
    def move_pawn(board, pawn_moves, row, col):
        valid_moves = []        
        for i in range(len(pawn_moves)):
            new_row = row+pawn_moves[i][0]
            new_col = col+pawn_moves[i][1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                if board[new_row][new_col] == "--":
                    (valid_moves).append((new_row, new_col))
        return valid_moves
    def pawn_capture(board, pawn_moves, piece_color, row, col):
        valid_moves = [] 
        for i in range(len(pawn_moves)):
            new_row = row+pawn_moves[i][0]
            new_col = col+pawn_moves[i][1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                if  board[new_row][new_col] != "--" and board[new_row][new_col][0] != piece_color:
                    valid_moves.append((new_row, new_col))
        return valid_moves