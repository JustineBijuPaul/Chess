# Chess Game

A simple chess game implementation using Python and Tkinter. This application provides a graphical user interface for playing chess between two players.

## Project Structure

The project is organized as follows:

```
chess/
├── imgs/
│   ├── b_pawn.png
│   ├── b_knight.png
│   ├── b_bishop.png
│   ├── b_rook.png
│   ├── b_queen.png
│   ├── b_king.png
│   ├── w_pawn.png
│   ├── w_knight.png
│   ├── w_bishop.png
│   ├── w_rook.png
│   └── w_queen.png
├── chess_final.py
├── chess
└── README.md
```

## Features

- Full implementation of standard chess rules
- Graphical user interface using Tkinter
- Move validation for all piece types
- Check and checkmate detection
- Turn-based gameplay
- Move history tracking
- Simple and intuitive interface

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)
- typing module
- copy module

## Installation

1. Ensure you have Python 3.x installed on your system
2. Install Pygame by running:
   ```bash
   pip install pygame typing copy
   ```
3. Run the game using:
   ```bash
   python3 chess_final.py
   ```
   or
   ```bash
   python chess_final.py
   ```

This will start the chess game with the Pygame interface.

## How to Play

1. The game starts with White's turn
2. Enter moves using algebraic notation:
   - Format: `[start_position] [end_position]`
   - Example: `e2 e4` moves the piece from e2 to e4
3. Click the "Submit" button or press Enter to make your move
4. The game alternates between White and Black players
5. Type "quit" to exit the game

## Game Rules

- All standard chess piece movements are implemented:
  - Pawns: Move forward one square, or two squares on their first move
  - Rooks: Move any number of squares horizontally or vertically
  - Knights: Move in L-shape (two squares in one direction, one square perpendicular)
  - Bishops: Move any number of squares diagonally
  - Queens: Move any number of squares in any direction
  - Kings: Move one square in any direction
- Pieces cannot jump over other pieces (except knights)
- Players cannot make moves that leave their king in check
- Game ends when one player achieves checkmate

## Code Structure

- `create_board()`: Initializes the chess board with pieces
- `is_valid_move()`: Validates moves for each piece type
- `is_in_check()`: Determines if a king is in check
- `is_checkmate()`: Checks for checkmate condition
- `make_move()`: Executes a valid move on the board
- `print_board_to_gui()`: Updates the GUI representation
- `on_move_input()`: Handles player move input and game logic

## Error Handling

The game includes error checking for:
- Invalid move formats
- Moving pieces out of turn
- Invalid piece movements
- Moves that leave king in check
- Out of bounds moves

## Technical Notes

- The board is represented as an 8x8 grid of dictionaries
- Each piece is a dictionary containing:
  - type: piece type (P, R, N, B, Q, K)
  - color: piece color (white, black)
  - has_moved: movement tracking for special moves
- The GUI is built using Tkinter buttons and labels
- Move validation is handled through separate functions for each piece type

## Limitations

- No support for special moves like castling or en passant
- No pawn promotion implementation
- No move time limits or game clock
- No save/load game functionality
- No AI opponent option

## Contributing

Feel free to fork this project and submit pull requests for any improvements such as:
- Adding missing chess features (castling, en passant, pawn promotion)
- Implementing an AI opponent
- Adding game save/load functionality
- Improving the user interface
- Adding move time limits
- Adding network play capability