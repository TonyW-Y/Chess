class ChessUtils:
    def move_no_slide(board, piece_move, piece_color, row, col):
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