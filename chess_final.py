import tkinter as tk
from typing import List, Tuple, Dict
from copy import deepcopy

WHITE = "white"
BLACK = "black"

PIECES = {
    "P": "pawn",
    "R": "rook",
    "N": "knight",
    "B": "bishop",
    "Q": "queen",
    "K": "king"
}

def create_piece(piece_type: str, color: str) -> Dict:
    return {"type": piece_type, "color": color, "has_moved": False}

def create_board() -> List[List[Dict]]:
    board = [[None for _ in range(8)] for _ in range(8)]
    for col in range(8):
        board[1][col] = create_piece("P", BLACK) 
        board[6][col] = create_piece("P", WHITE)
    piece_order = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    for col in range(8):
        board[0][col] = create_piece(piece_order[col], BLACK)
        board[7][col] = create_piece(piece_order[col], WHITE)
    return board

def parse_position(pos_str: str) -> Tuple[int, int]:  
    col = ord(pos_str[0].lower()) - ord('a')
    row = 8 - int(pos_str[1])
    return (row, col)

def print_board_to_gui(board, buttons):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                symbol = piece["type"]
                if piece["color"] == BLACK:
                    symbol = symbol.lower() 
            else:
                symbol = ""
            buttons[row][col].config(text=symbol)

def is_valid_pawn_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]], piece: Dict) -> bool:
    start_row, start_col = start
    end_row, end_col = end
    direction = -1 if piece["color"] == WHITE else 1
    
    if start_col == end_col:
        if end_row == start_row + direction and not board[end_row][end_col]:
            return True
        if (not piece["has_moved"] and
            end_row == start_row + 2 * direction and
            not board[end_row][end_col] and
            not board[start_row + direction][start_col]):
            
            return True
    
    elif (abs(start_col - end_col) == 1 and
          end_row == start_row + direction and
          board[end_row][end_col] and
          board[end_row][end_col]["color"] != piece["color"]):
        return True
    
    return False

def is_valid_rook_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]]) -> bool:
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
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def is_valid_bishop_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]]) -> bool:
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
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece["type"] == "K" and piece["color"] == color:
                return (row, col)
    return (-1, -1)

def is_in_check(board: List[List[Dict]], color: str) -> bool:
    king_pos = find_king(board, color)
    opponent_color = BLACK if color == WHITE else WHITE

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece["color"] == opponent_color:
                if is_valid_move((row, col), king_pos, board, piece):
                    return True
    return False

def make_move(board, start, end):
    piece = board[start[0]][start[1]]
    board[end[0]][end[1]] = piece
    board[start[0]][start[1]] = None
    piece["has_moved"] = True

def check_winner(board, current_turn):
    opponent_color = BLACK if current_turn == WHITE else WHITE
    king_pos = find_king(board, opponent_color)
    if king_pos == (-1, -1):
        return f"{current_turn.capitalize()} wins!"
    return None

def is_checkmate(board, color):
    opponent_color = BLACK if color == WHITE else WHITE
    king_pos = find_king(board, color)
    if not is_in_check(board, color):
        return False

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece["color"] == color:
                for r in range(8):
                    for c in range(8):
                        if is_valid_move((row, col), (r, c), board, piece):
                            test_board = deepcopy(board)
                            make_move(test_board, (row, col), (r, c))
                            if not is_in_check(test_board, color):
                                return False
    return True

def on_move_input(board, buttons, current_turn, move_entry, status_label):  
    move = move_entry.get().strip().lower()
    move_entry.delete(0, tk.END)
    if move == "quit":
        root.destroy()
        return 
    try:
        start_str, end_str = move.split()
        start = parse_position(start_str)
        end = parse_position(end_str)
        piece = board[start[0]][start[1]]
        if not piece or piece["color"] != current_turn[0]:
            status_label.config(text="Invalid move: Wrong piece")
            return
        if not is_valid_move(start, end, board, piece):
            status_label.config(text="Invalid move")
            return
        test_board = deepcopy(board)
        make_move(test_board, start, end)
        if is_in_check(test_board, current_turn[0]):
            status_label.config(text="Move leaves king in check")
            return
        make_move(board, start, end)
        board[end[0]][end[1]]["has_moved"] = True
        
        opponent_color = BLACK if current_turn[0] == WHITE else WHITE
        if is_checkmate(board, opponent_color):
            status_label.config(text=f"{current_turn[0].capitalize()} wins by checkmate!")
            for row in buttons:
                for button in row:
                    button.config(state=tk.DISABLED)
            return
        
        current_turn[0] = BLACK if current_turn[0] == WHITE else WHITE
        print_board_to_gui(board, buttons)   
        status_label.config(text=f"{current_turn[0].capitalize()}'s turn")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

root = tk.Tk()
root.title("Chess")

board = create_board()
current_turn = [WHITE]

frame = tk.Frame(root)
frame.grid(row=0, column=0)

buttons = [[None for _ in range(8)] for _ in range(8)]
for row in range(8):
    for col in range(8):
        buttons[row][col] = tk.Button(frame, width=4, height=2, font=("Arial", 14))
        buttons[row][col].grid(row=row + 1, column=col + 1)

for i in range(8):
    tk.Label(frame, text=chr(ord('A') + i), font=("Arial", 12)).grid(row=0, column=i + 1)
    tk.Label(frame, text=str(8 - i), font=("Arial", 12)).grid(row=i + 1, column=0)


tk.Label(frame, text=" ").grid(row=9, column=0)

move_frame = tk.Frame(root)
move_frame.grid(row=1, column=0)

move_label = tk.Label(move_frame, text="Enter your move: ")
move_label.pack(side=tk.LEFT)

move_entry = tk.Entry(move_frame, width=10)
move_entry.pack(side=tk.LEFT)

status_label = tk.Label(root, text=f"{current_turn[0].capitalize()}'s turn", font=("Arial", 12))
status_label.grid(row=2, column=0)

def on_submit():
    on_move_input(board, buttons, current_turn, move_entry, status_label)

submit_button = tk.Button(move_frame, text="Submit", command=on_submit)
submit_button.pack(side=tk.LEFT)
