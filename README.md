Battleship Game
Overview

This is a simplified console version of the classic Battleship game.
Players can place their ships manually, and the bot automatically generates ships randomly. The game alternates turns until all ships of one side are destroyed.

Input Format

Player enters ships via the console when prompted.

Ships are defined as a sequence of coordinates (x y).

Each ship must follow these rules:

Length corresponds to the ship size (e.g., 4, 3, 2, 1).

Ships must be straight (either horizontal or vertical).

Ships cannot touch each other, even diagonally.

Coordinates must be within the board (0–9 for both x and y).

Example input for a ship of size 3: 1 2 1 3 1 4

Ship Placement Validation

The program checks:

Ship size matches the expected size.

Ship is inside the board.

Ship is straight (either horizontal or vertical).

Ship does not touch other ships (including diagonally).

If any rule is broken, the user is prompted to re-enter the ship.

Game State Updates

The board is a 10x10 grid. Symbols:

s — ship

X — hit

. — miss

- — empty cell

Player sees their own ships and hits/misses; the bot board hides ships until hit.

Each move (player and bot) updates the board and is logged.

Bot chooses random coordinates, and targets neighbors after hitting a ship.

Run the game: python main.py
