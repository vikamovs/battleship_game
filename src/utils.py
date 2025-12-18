BOARD_SIZE = 10

def inside_board(x, y):
    if x < 0 or x >= BOARD_SIZE:
        return False
    if y < 0 or y >= BOARD_SIZE:
        return False
    return True

def neighbors(x, y):
    result = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                nx, ny = x + dx, y + dy
                if inside_board(nx, ny):
                    result.append((nx, ny))
    return result

def print_board(board, hide_ships=False):
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

