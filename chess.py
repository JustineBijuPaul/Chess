from typing import List, Tuple, Dict
from copy import deepcopy

# Constants for pieces and colors
WHITE = "white"
BLACK = "black"

# Piece symbols
#dictonary
PIECES = {
    "P": "pawn",
    "R": "rook", 
    "N": "knight",
    "B": "bishop",
    "Q": "queen",
    "K": "king"
}

def create_piece(piece_type: str, color: str) -> Dict:
    """Create a piece dictionary with type, color and moved status"""
    return {
        "type": piece_type,
        "color": color,
        "has_moved": False
    }

def create_board() -> List[List[Dict]]:
    """Create and initialize chess board"""
    board = [[None for _ in range(8)] for _ in range(8)]
    
    # Set up pawns
    for col in range(8):
        board[1][col] = create_piece("P", BLACK)
        board[6][col] = create_piece("P", WHITE)
    
    # Set up other pieces
    piece_order = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    for col in range(8):
        board[0][col] = create_piece(piece_order[col], BLACK)
        board[7][col] = create_piece(piece_order[col], WHITE)
        
    return board

def is_valid_pawn_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]], piece: Dict) -> bool:
    """Check if pawn move is valid"""
    start_row, start_col = start
    end_row, end_col = end
    direction = -1 if piece["color"] == WHITE else 1
    
    # Moving straight
    if start_col == end_col:
        if end_row == start_row + direction and not board[end_row][end_col]:
            return True
        if (not piece["has_moved"] and 
            end_row == start_row + 2 * direction and 
            not board[end_row][end_col] and 
            not board[start_row + direction][start_col]):
            return True
    
    # Capturing
    elif (abs(start_col - end_col) == 1 and 
          end_row == start_row + direction and 
          board[end_row][end_col] and 
          board[end_row][end_col]["color"] != piece["color"]):
        return True
    
    return False

def is_valid_rook_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]]) -> bool:
    """Check if rook move is valid"""
    start_row, start_col = start
    end_row, end_col = end
    
    if start_row != end_row and start_col != end_col:
        return False
        
    row_step = 0 if start_row == end_row else (end_row - start_row) // abs(end_row - start_row)
    col_step = 0 if start_col == end_col else (end_col - start_col) // abs(end_col - start_col)
    
    curr_row, curr_col = start_row + row_step, start_col + col_step
    while (curr_row, curr_col) != (end_row, end_col):
        if board[curr_row][curr_col]:
            return False
        curr_row += row_step
        curr_col += col_step
    
    return True

def is_valid_knight_move(start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    """Check if knight move is valid"""
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def is_valid_bishop_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]]) -> bool:
    """Check if bishop move is valid"""
    start_row, start_col = start
    end_row, end_col = end
    
    if abs(end_row - start_row) != abs(end_col - start_col):
        return False
        
    row_step = (end_row - start_row) // abs(end_row - start_row)
    col_step = (end_col - start_col) // abs(end_col - start_col)
    
    curr_row, curr_col = start_row + row_step, start_col + col_step
    while (curr_row, curr_col) != (end_row, end_col):
        if board[curr_row][curr_col]:
            return False
        curr_row += row_step
        curr_col += col_step
    
    return True

def is_valid_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]], piece: Dict) -> bool:
    """Check if a move is valid for given piece"""
    if not (0 <= end[0] < 8 and 0 <= end[1] < 8):
        return False
        
    if board[end[0]][end[1]] and board[end[0]][end[1]]["color"] == piece["color"]:
        return False
        
    piece_type = piece["type"]
    
    if piece_type == "P":
        return is_valid_pawn_move(start, end, board, piece)
    elif piece_type == "R":
        return is_valid_rook_move(start, end, board)
    elif piece_type == "N":
        return is_valid_knight_move(start, end)
    elif piece_type == "B":
        return is_valid_bishop_move(start, end, board)
    elif piece_type == "Q":
        return is_valid_rook_move(start, end, board) or is_valid_bishop_move(start, end, board)
    elif piece_type == "K":
        return abs(end[0] - start[0]) <= 1 and abs(end[1] - start[1]) <= 1
    
    return False

def find_king(board: List[List[Dict]], color: str) -> Tuple[int, int]:
    """Find position of king with given color"""
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece["type"] == "K" and piece["color"] == color:
                return (row, col)
    return (-1, -1)

def is_in_check(board: List[List[Dict]], color: str) -> bool:
    """Check if given color's king is in check"""
    king_pos = find_king(board, color)
    opponent_color = BLACK if color == WHITE else WHITE
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece["color"] == opponent_color:
                if is_valid_move((row, col), king_pos, board, piece):
                    return True
    return False

def parse_position(pos_str: str) -> Tuple[int, int]:
    """Convert chess notation to board coordinates"""
    if len(pos_str) != 2:
        raise ValueError("Position should be letter + number (e.g., 'e2')")
    
    col = ord(pos_str[0].lower()) - ord('a')
    row = 8 - int(pos_str[1])
    
    if not (0 <= row < 8 and 0 <= col < 8):
        raise ValueError("Position must be between a1 and h8")
        
    return (row, col)

def print_board(board: List[List[Dict]]):
    """Display the chess board"""
    print("\n  a b c d e f g h")
    for row in range(8):
        print(f"{8-row}", end=" ")
        for col in range(8):
            piece = board[row][col]
            if piece:
                symbol = piece["type"]
                if piece["color"] == BLACK:
                    symbol = symbol.lower()
            else:
                symbol = "."
            print(symbol, end=" ")
        print(f"{8-row}")
    print("  a b c d e f g h")

def play_chess():
    """Main game function"""
    board = create_board()
    current_turn = WHITE
    
    print("\nWelcome to Python Chess!")
    print("Enter moves like: e2 e4")
    print("Type 'quit' to end game")
    print("\nPieces: P=Pawn, R=Rook, N=Knight, B=Bishop, Q=Queen, K=King")
    print("White pieces are uppercase, black pieces are lowercase")
    
    while True:
        print_board(board)
        print(f"\n{current_turn}'s turn")
        
        move = input("Enter move (e.g., 'e2 e4'): ").lower().strip()
        if move == "quit":
            break
            
        try:
            start_str, end_str = move.split()
            start = parse_position(start_str)
            end = parse_position(end_str)
            
            piece = board[start[0]][start[1]]
            if not piece:
                print("No piece at starting position")
                continue
                
            if piece["color"] != current_turn:
                print(f"It's {current_turn}'s turn")
                continue
            
            # Test move
            test_board = deepcopy(board)
            if not is_valid_move(start, end, test_board, piece):
                print("Invalid move for this piece")
                continue
                
            test_board[end[0]][end[1]] = test_board[start[0]][start[1]]
            test_board[start[0]][start[1]] = None
            
            if is_in_check(test_board, current_turn):
                print("Move would put/leave king in check")
                continue
            
            # Make actual move
            board[end[0]][end[1]] = board[start[0]][start[1]]
            board[start[0]][start[1]] = None
            board[end[0]][end[1]]["has_moved"] = True
            
            current_turn = BLACK if current_turn == WHITE else WHITE
            
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")

if __name__ == "__main__":
    play_chess()