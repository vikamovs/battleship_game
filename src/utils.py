BOARD_SIZE = 10

def inside_board(x, y):
    """
    Checks if the given coordinates are inside the game board
    Returns:
        bool: True if the coordinates are inside the board, False otherwise
    """
    if x < 0 or x >= BOARD_SIZE:
        return False
    if y < 0 or y >= BOARD_SIZE:
        return False
    return True

def neighbors(x, y):
    """
    Returns a list of neighboring cells (8 directions) for a given cell
    Returns:
        List[Tuple[int, int]]: List of coordinates for neighboring cells that are inside the board
    """
    result = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                nx, ny = x + dx, y + dy
                if inside_board(nx, ny):
                    result.append((nx, ny))
    return result

def print_board(board, hide_ships=False):
    """
    Prints the game board to the console
    """
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for y in range(BOARD_SIZE):
        row_display = []
        for x in range(BOARD_SIZE):
            cell = board[y][x]
            if hide_ships and cell == "s":
                row_display.append("-")  
            else:
                row_display.append(cell)
        print(y, " ".join(row_display))
