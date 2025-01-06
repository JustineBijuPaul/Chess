# Chess Project

This is a simple chess game implemented in Python using the Pygame library. The game includes all the basic features such as moving pieces, capturing, and special moves like castling and pawn promotion. The project is structured to be extensible and easily modifiable.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Classes](#classes)
   1. [Piece Class](#piece-class)
   2. [Square Class](#square-class)
   3. [Individual Piece Classes](#individual-piece-classes)
      - [Bishop Class](#bishop-class)
      - [King Class](#king-class)
      - [Knight Class](#knight-class)
      - [Pawn Class](#pawn-class)
      - [Queen Class](#queen-class)
      - [Rook Class](#rook-class)
3. [How to Run](#how-to-run)

## Project Structure

The project is organized as follows:

```
chess/
├── data/
│   ├── imgs/
│   │   ├── b_pawn.png
│   │   ├── b_knight.png
│   │   ├── b_bishop.png
│   │   ├── b_rook.png
│   │   ├── b_queen.png
│   │   ├── b_king.png
│   │   ├── w_pawn.png
│   │   ├── w_knight.png
│   │   ├── w_bishop.png
│   │   ├── w_rook.png
│   │   └── w_queen.png
│   └── classes/
│       ├── board.py
│       ├── piece.py
│       ├── square.py
│       └── pieces/
│           ├── Bishop.py
│           ├── King.py
│           ├── Knight.py
│           ├── Pawn.py
│           ├── Queen.py
│           └── Rook.py
├── main.py
├── requirements.txt
└── README.md
```

- **imgs/**: Contains the image files for each chess piece (both black and white).
- **classes/**: Contains the logic for the chess game, including the board, pieces, and squares.
- **main.py**: Entry point for the game logic and Pygame interface.
- **requirements.txt**: Contains the list of required Python libraries (e.g., Pygame).

## Classes

### Piece Class

The `Piece` class serves as the base class for all the individual chess pieces. It contains common attributes and methods shared by all pieces.

#### Key Attributes:
- `pos`: The position of the piece on the board (tuple of (x, y)).
- `color`: The color of the piece ('white' or 'black').
- `has_moved`: A boolean indicating whether the piece has moved.
- `notation`: A symbol representing the type of piece (e.g., 'K' for King, 'Q' for Queen).

#### Key Methods:
- `move(board, square, force=False)`: Moves the piece to a new square, updates its position, and handles special cases like pawn promotion and castling.
- `get_moves(board)`: Returns a list of valid squares the piece can move to.
- `get_valid_moves(board)`: Filters out moves that would place the current player's king in check.
- `attacking_squares(board)`: Returns a list of squares the piece attacks.

### Square Class

The `Square` class represents a single square on the chessboard.

#### Key Attributes:
- `x, y`: The x and y coordinates of the square.
- `color`: The color of the square ('light' or 'dark').
- `occupying_piece`: The piece occupying this square (if any).
- `highlight`: A boolean indicating whether the square is highlighted.

#### Key Methods:
- `get_coord()`: Returns the coordinate notation of the square (e.g., 'a1', 'b3').
- `draw(display)`: Draws the square and the piece on it using Pygame.

### Individual Piece Classes

Each piece (Bishop, King, Knight, Pawn, Queen, and Rook) inherits from the `Piece` class and overrides the `get_possible_moves` method to define its own movement logic.

#### Bishop Class

- **Movement**: Bishops move diagonally in all four directions. The `get_possible_moves` method generates possible diagonal moves based on the current position.
  
#### King Class

- **Movement**: The King moves one square in any direction.
- **Special Moves**: The King can castle with a rook if neither has moved, and if there are no pieces between them. The `can_castle` method checks if castling is possible.

#### Knight Class

- **Movement**: The Knight moves in an "L" shape: two squares in one direction and one square perpendicular to it. The `get_possible_moves` method generates all eight potential moves.

#### Pawn Class

- **Movement**: Pawns move forward one square but capture diagonally. They can move two squares forward from their starting position.
- **Promotion**: When a pawn reaches the opponent's back rank, it is promoted to a queen, rook, bishop, or knight.

#### Queen Class

- **Movement**: The Queen combines the movement of both the rook and bishop, moving horizontally, vertically, and diagonally.

#### Rook Class

- **Movement**: The Rook moves horizontally or vertically any number of squares.

## How to Run

1. Install Pygame by running:
   ```bash
   pip install pygame
   ```
2. Run the game using:
   ```bash
   python main.py
   ```

This will start the chess game with the Pygame interface.

## Conclusion

This chess project demonstrates the basic mechanics of chess and is built in a modular way using object-oriented principles. Each piece class has its own logic for movement and special behavior. The board and squares are managed separately to allow for easy expansion and customization of the game.

Feel free to modify and extend the game, such as adding features like AI or multiplayer support.