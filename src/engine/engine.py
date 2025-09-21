from typing import Optional, Tuple
from .legality import Legality
from .make_unmake import Make_Unmake
from .chess_utils import Chess_Utils
from .chess_board import Chess_Board


class Engine:
    def __init__(self, board):
        self.board = board
        self.has_moved = board.has_moved
        self.legality = Legality(self.board)
        self.utils = Chess_Utils()
    
    def play_turn(self, row: int, col: int, new_row: int, new_col: int, promotion: Optional[str] = None) -> Tuple[bool, str]:
        legal_moves = self.legality.filter_move(row,col)
        if (new_row, new_col) in legal_moves:
            make_unmake = Make_Unmake(self.board)
            turn_check = make_unmake.turn(row, col)
            if turn_check == self.board.board[row][col][0]:
                self.board.save_move(row, col, new_row, new_col, promotion)
                return True, "move made"
            elif turn_check == "n":
                return False, "invalid move (turn)"
            else:
                return False, "not your turn"
        else:
            return False, "not a legal move"
        
    def undo(self):
        self.board.undo_move()
    
    def get_game_status(self):
        """Return a tuple (status, info) where:
        - status is one of: 'in_progress', 'checkmate', 'stalemate'
        - info for checkmate is the winner color: 'w' or 'b'; otherwise None
        """
        color_to_move = self.board.color
        if self.legality.is_checkmate(color_to_move):
            winner = 'w' if color_to_move == 'b' else 'b'
            return 'checkmate', winner
        if self.legality.is_stalemate(color_to_move):
            return 'stalemate', None
        return 'in_progress', None
        
    def reset(self):
        """Reset the game to the initial state."""
        self.board.reset_board()
        self.has_moved = self.board.has_moved
        
if __name__ == "__main__":
    def print_board(board):
        for row in board.board:  # board.board is your 2D list
            print(" ".join(row))
        print("\n")

    # Setup
    board = Chess_Board()
    engine = Engine(board)

    print("Initial position:")
    print_board(board)

    # Test moves
    print("Move white pawn (6,4) -> (5,4):")
    engine.play_turn(6, 4, 5, 4)
    print_board(board)

    print("Move black pawn (1,4) -> (2,4):")
    engine.play_turn(1, 4, 2, 4)
    print_board(board)


    print(engine.legality.get_legal_moves(7,3))

    print(engine.legality.get_legal_moves(0,3))


