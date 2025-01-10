import tkinter as tk    #to create gui for the chess
from typing import List, Tuple, Dict    #to access all the dictonary, list and tuple functions and methods
from copy import deepcopy   #to copy and paste the single repative items


#<<< person 2
# Constants for pieces and colors
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
    return {"type": piece_type, "color": color, "has_moved": False} #creates a dictionary for the peice

'''
create_piece(piece_type: str, color: str):
    The name of the function is create_piece.
    It takes two arguments:
        piece_type: A string that specifies what kind of piece it is (e.g., "pawn", "rook").
        color: A string that specifies the color of the piece (e.g., "white", "black").
    The : str after the arguments is a type hint, which means these inputs are expected to be strings.
-> Dict: This is another type hint. It tells us the function will return a dictionary.
return {"type": piece_type, "color": color, "has_moved": False}:
    The function returns a dictionary with three keys:
        "type": The value is the piece_type you provided.
        "color": The value is the color you provided.
        "has_moved": The value is False by default, meaning the piece hasn't moved yet.
'''


def create_board() -> List[List[Dict]]:
    board = [[None for _ in range(8)] for _ in range(8)]    #creates an 8x8 board
    for col in range(8):    #loops through the columns
        board[1][col] = create_piece("P", BLACK)    #creates the black pawns
        board[6][col] = create_piece("P", WHITE)    #creates the white pawns
    piece_order = ["R", "N", "B", "Q", "K", "B", "N", "R"]  #creates the order of the peices
    for col in range(8):    #loops through the columns
        board[0][col] = create_piece(piece_order[col], BLACK)   #creates the black peices
        board[7][col] = create_piece(piece_order[col], WHITE)   #creates the white peices
    return board

'''
1. What is this code?
    This function, create_board, creates a chessboard in Python as an 8x8 grid (like a matrix). Each square on the board can either be None (empty) or contain a dictionary representing a chess piece.

2. What are the parts of the code?
    def create_board() -> List[List[Dict]]:
        The name of the function is create_board.
        It doesn’t take any arguments (notice the empty ()).
        The -> List[List[Dict]] is a type hint, which tells us the function returns a list of lists (the 8x8 grid), and each cell can contain a dictionary (representing a piece).'''



def parse_position(pos_str: str) -> Tuple[int, int]:  
    col = ord(pos_str[0].lower()) - ord('a')   #converts column letters into numbers, pos_str[0] means parameter's first letter
    row = 8 - int(pos_str[1])  #pos_str[1] means parameter's second letter
    return (row, col)

'''
What does it do?
    It takes a string (e.g., "e2") representing a chessboard position in standard notation.
    Converts the position into a tuple of integers that represent the row and column indices for an 8x8 board.
'''

def print_board_to_gui(board, buttons):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]    #records the peice on the board
            if piece:
                symbol = piece["type"]   #defines each buttons for peices
                if piece["color"] == BLACK:   #makes the black peices lower cases
                    symbol = symbol.lower() 
            else:
                symbol = ""   #sets the text empty for the buttons if there are no peices
            buttons[row][col].config(text=symbol)   #sets the text for the buttons

'''
What Does the Code Do?
    It loops through an 8x8 chessboard (board) and checks what piece is present at each position.
    It updates the corresponding button in the buttons grid to display the appropriate symbol for the piece.
    If a square is empty, the button's text is set to an empty string.'''

#>>> person 2



#persson 1 <<<
def is_valid_pawn_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]], piece: Dict) -> bool:
    """Check if pawn move is valid"""
    start_row, start_col = start  #splits the start parameter into start row and start column
    end_row, end_col = end   #splits the end parameter into end row and end column
    direction = -1 if piece["color"] == WHITE else 1    #reverse the direction movement if the color is white for the row
    
    # Moving straight
    if start_col == end_col:    #checks if starting column is ending column and satisfy the condition then the pawn is in the same column
        if end_row == start_row + direction and not board[end_row][end_col]:    #Checks if the pawn is moving one square forward which should be also empty in the correct direction.
            return True
        if (not piece["has_moved"] and  #checks if the peice is not moved yet
            end_row == start_row + 2 * direction and    #checks if end row is the start row with added direction
            not board[end_row][end_col] and     #checks if the ending square is not the starting square
            not board[start_row + direction][start_col]):   #checks if the peice is not moving diagonally
            
            """         
            Pawns can move two squares forward only if:
                The pawn hasn’t moved yet (piece["has_moved"] is False).
                Both the square directly ahead and the square two squares ahead are empty. """
            return True
    
    # Capturing
    elif (abs(start_col - end_col) == 1 and     #checks if the starting column is not the end column and have only 1 column difference 
          end_row == start_row + direction and  #checks if the end row is the starting row with adding direction
          board[end_row][end_col] and   #checks if there is square on the board
          board[end_row][end_col]["color"] != piece["color"]):  #if the the peice on the square is not the same colour as the moving peice
        return True
    
    return False #else return the move is not valid

""" 
Inputs:
    start: The starting position of the pawn as a tuple (row, column).
    end: The desired ending position as a tuple (row, column).
    board: The chessboard, represented as an 8x8 grid where each square contains:
        A dictionary representing a piece (e.g., {"type": "P", "color": BLACK, "has_moved": False}).
        Or None if the square is empty.
    piece: A dictionary describing the pawn being moved.
Output:
    Returns True if the move is valid for a pawn; otherwise, False. """





def is_valid_rook_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]]) -> bool:
    """Check if rook move is valid"""
    start_row, start_col = start    #splits the start parameter into start row and start column
    end_row, end_col = end  #splits the end parameter into end row and end column
    
    if start_row != end_row and start_col != end_col:   #checks if the peice is moving along side either a row or a column
        return False    #if both condition are false then it returns false
        
    row_step = 0 if start_row == end_row else (end_row - start_row) // abs(end_row - start_row)  #counts the nuber of row the peice has moved along side row
    col_step = 0 if start_col == end_col else (end_col - start_col) // abs(end_col - start_col)  #counts the nuber of column the peice has moved along side column
    
    curr_row, curr_col = start_row + row_step, start_col + col_step     #records the current row snd current column
    while (curr_row, curr_col) != (end_row, end_col):   #checks if the current row and column is not the same as the end row and column
        if board[curr_row][curr_col]:  #checks if the current row and column is not empty
            return False 
        curr_row += row_step   #increments the current row
        curr_col += col_step    #increments the current column
    
    return True

def is_valid_knight_move(start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    """Check if knight move is valid"""
    row_diff = abs(end[0] - start[0])   #finds the difference between the end row and start row
    col_diff = abs(end[1] - start[1])   #finds the difference between the end column and start column
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)   #checks if the difference between the row and column is 2 and 1 or 1 and 2

def is_valid_bishop_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]]) -> bool:
    """Check if bishop move is valid"""
    start_row, start_col = start    #splits the start parameter into start row and start column
    end_row, end_col = end  #splits the end parameter into end row and end column
    
    if abs(end_row - start_row) != abs(end_col - start_col):  #checks if the difference between the end row and start row is not equal to the difference between the end column and start column
        return False
        
    row_step = (end_row - start_row) // abs(end_row - start_row)  #counts the nuber of row the peice has moved along side row
    col_step = (end_col - start_col) // abs(end_col - start_col) #counts the nuber of column the peice has moved along side column
    
    curr_row, curr_col = start_row + row_step, start_col + col_step  #records the current row snd current column
    while (curr_row, curr_col) != (end_row, end_col): #checks if the current row and column is not the same as the end row and column
        if board[curr_row][curr_col]: #checks if the current row and column is not empty
            return False
        curr_row += row_step #increments the current row
        curr_col += col_step #increments the current column
    
    return True

def is_valid_move(start: Tuple[int, int], end: Tuple[int, int], board: List[List[Dict]], piece: Dict) -> bool:
    """Check if a move is valid for given piece"""
    if not (0 <= end[0] < 8 and 0 <= end[1] < 8):   #checks if the end row and column is within the board
        return False
        
    if board[end[0]][end[1]] and board[end[0]][end[1]]["color"] == piece["color"]:  #checks if the end row and column is not empty and the color of the peice is the same as the moving peice
        return False
        
    piece_type = piece["type"]  #records the type of the peice
    
    if piece_type == "P":   #checks if the peice is a pawn
        return is_valid_pawn_move(start, end, board, piece)     #checks if the move is valid for a pawn
    elif piece_type == "R":  #checks if the peice is a rook
        return is_valid_rook_move(start, end, board)  #checks if the move is valid for a rook
    elif piece_type == "N":  #checks if the peice is a knight
        return is_valid_knight_move(start, end)  #checks if the move is valid for a knight
    elif piece_type == "B":     #checks if the peice is a bishop
        return is_valid_bishop_move(start, end, board)  #checks if the move is valid for a bishop
    elif piece_type == "Q":     #checks if the peice is a queen
        return is_valid_rook_move(start, end, board) or is_valid_bishop_move(start, end, board)     #checks if the move is valid for a queen
    elif piece_type == "K":    #checks if the peice is a king
        return abs(end[0] - start[0]) <= 1 and abs(end[1] - start[1]) <= 1  #checks if the difference between the end row and start row is less than or equal to 1 and the difference between the end column and start column is less than or equal to 1
    return False
#>>> person 1

#<<< person 3
def find_king(board: List[List[Dict]], color: str) -> Tuple[int, int]:
    """Find position of king with given color"""
    for row in range(8):    #loops through the rows
        for col in range(8):    #loops through the columns
            piece = board[row][col]    #records the peice on the board
            if piece and piece["type"] == "K" and piece["color"] == color:  #checks if the peice is a king and the color of the peice is the same as the given color
                return (row, col)
    return (-1, -1)

def is_in_check(board: List[List[Dict]], color: str) -> bool:
    """Check if given color's king is in check"""
    king_pos = find_king(board, color)      #finds the position of the king
    opponent_color = BLACK if color == WHITE else WHITE     #records the opponent color
    
    for row in range(8):    #loops through the rows
        for col in range(8):    #loops through the columns
            piece = board[row][col]     #records the peice on the board
            if piece and piece["color"] == opponent_color:      #checks if the peice is not empty and the color of the peice is the same as the opponent color
                if is_valid_move((row, col), king_pos, board, piece):       #checks if the move is valid for the peice
                    return True
    return False
# >>> player 3


#<<< person 2
def make_move(board, start, end):
    piece = board[start[0]][start[1]]   #records the peice on the starting position
    board[end[0]][end[1]] = piece   #records the peice on the ending position
    board[start[0]][start[1]] = None    #sets the starting position empty
    piece["has_moved"] = True   #sets the peice has moved to true

def check_winner(board, current_turn):
    opponent_color = BLACK if current_turn == WHITE else WHITE  #records the opponent color
    king_pos = find_king(board, opponent_color)  #finds the position of the king
    if king_pos == (-1, -1):    #checks if the king is not on the board
        return f"{current_turn.capitalize()} wins!"  #returns the winner
    return None

def is_checkmate(board, color):
    """Check if the given color is in checkmate"""
    opponent_color = BLACK if color == WHITE else WHITE     #records the opponent color
    king_pos = find_king(board, color)  #finds the position of the king
    
    # If king is not in check, it's not checkmate
    if not is_in_check(board, color):   #checks if the king is not in check
        return False

    # Check all possible moves to see if any can prevent check
    for row in range(8):        #loops through the rows
        for col in range(8):    #loops through the columns
            piece = board[row][col]    #records the peice on the board
            if piece and piece["color"] == color:   #checks if the peice is not empty and the color of the peice is the same as the given color
                for r in range(8):  #loops through the rows
                    for c in range(8):  #loops through the columns
                        if is_valid_move((row, col), (r, c), board, piece): #checks if the move is valid for the peice
                            test_board = deepcopy(board)    #copies the board
                            make_move(test_board, (row, col), (r, c))   #makes the move
                            if not is_in_check(test_board, color):  #checks if the king is not in check
                                return False
    return True

def on_move_input(board, buttons, current_turn, move_entry, status_label):  
    move = move_entry.get().strip().lower()  #records the move input
    move_entry.delete(0, tk.END)    #deletes the move input
    if move == "quit":  #checks if the move is quit
        root.destroy()  #closes the window
        return 
    try:
        start_str, end_str = move.split()   #splits the move input into start and end
        start = parse_position(start_str)   #parses the start position
        end = parse_position(end_str)   #parses the end position
        piece = board[start[0]][start[1]]   #records the peice on the starting position
        if not piece or piece["color"] != current_turn[0]:  #checks if the peice is not empty and the color of the peice is the same as the current turn
            status_label.config(text="Invalid move: Wrong piece")   #sets the status label text
            return
        if not is_valid_move(start, end, board, piece):  #checks if the move is valid
            status_label.config(text="Invalid move")    #sets the status label text
            return
        test_board = deepcopy(board)    #copies the board
        make_move(test_board, start, end)   #makes the move
        if is_in_check(test_board, current_turn[0]):    #checks if the king is in check
            status_label.config(text="Move leaves king in check")   #sets the status label text
            return
        make_move(board, start, end)    #makes the move
        board[end[0]][end[1]]["has_moved"] = True   #sets the peice has moved to true
        
        # Check for checkmate
        opponent_color = BLACK if current_turn[0] == WHITE else WHITE   #records the opponent color
        if is_checkmate(board, opponent_color):  #checks if the opponent is in checkmate
            status_label.config(text=f"{current_turn[0].capitalize()} wins by checkmate!")  #sets the status label text
            for row in buttons:  #loops through the rows
                for button in row:  #loops through the buttons
                    button.config(state=tk.DISABLED)    #disables the buttons
            return
        
        # Switch turn
        current_turn[0] = BLACK if current_turn[0] == WHITE else WHITE  #switches the turn
        print_board_to_gui(board, buttons)  #prints the board to the gui   
        status_label.config(text=f"{current_turn[0].capitalize()}'s turn")  #sets the status label text
    except Exception as e:  #checks if there is an exception
        status_label.config(text=f"Error: {e}") #sets the status label text
# >>> person2

#<<< person 3
root = tk.Tk()  #creates a window
root.title("Chess") #sets the title of the window

board = create_board()  #creates the board
current_turn = [WHITE]  #sets the current turn

frame = tk.Frame(root)  #creates a frame
frame.grid(row=0, column=0) #sets the frame position

buttons = [[None for _ in range(8)] for _ in range(8)]  #creates the buttons
for row in range(8):    #loops through the rows
    for col in range(8):    #loops through the columns
        buttons[row][col] = tk.Button(frame, width=4, height=2, font=("Arial", 14)) #creates the buttons
        buttons[row][col].grid(row=row + 1, column=col + 1) #sets the buttons position

for i in range(8):  #loops through the range of 8
    tk.Label(frame, text=chr(ord('A') + i), font=("Arial", 12)).grid(row=0, column=i + 1)   #creates the labels for the columns
    tk.Label(frame, text=str(8 - i), font=("Arial", 12)).grid(row=i + 1, column=0)  #creates the labels for the rows


tk.Label(frame, text=" ").grid(row=9, column=0) #creates a label

move_frame = tk.Frame(root) #creates a frame
move_frame.grid(row=1, column=0)    #sets the frame position

move_label = tk.Label(move_frame, text="Enter your move: ") #creates a label
move_label.pack(side=tk.LEFT)   #sets the label position

move_entry = tk.Entry(move_frame, width=10) #creates an entry
move_entry.pack(side=tk.LEFT)   #sets the entry position

status_label = tk.Label(root, text=f"{current_turn[0].capitalize()}'s turn", font=("Arial", 12))    #creates a label
status_label.grid(row=2, column=0)  #sets the label position

def on_submit():
    on_move_input(board, buttons, current_turn, move_entry, status_label)   #calls the on_move_input function

submit_button = tk.Button(move_frame, text="Submit", command=on_submit)     #creates a button
submit_button.pack(side=tk.LEFT)    #sets the button position

