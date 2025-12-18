import csv
import random
from src.utils import inside_board, print_board, neighbors

BOARD_SIZE = 10

def read_ships(file_path):
    """
    Reads ship coordinates from a CSV file
    Returns:
        List[List[Tuple[int, int]]]: List of ships, each ship is a list of (x, y) coordinates
    """
    ships = []
    with open(file_path, newline="") as f:
        reader = csv.reader(f)
        current_ship = []
        for row in reader:
            if not row:
                if current_ship:
                    ships.append(current_ship)
                    current_ship = []
            else:
                x, y = map(int, row)
                current_ship.append((x, y))
        if current_ship:
            ships.append(current_ship)
    return ships

def create_empty_board():
    """
    Creates an empty game board
    Returns:
        List[List[str]]: 2D list representing the board filled with '-'
    """
    return [["-" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def mark_ship_on_board(board, ships):
    """
    Places ships on the board by marking their positions with 's'
    """
    for ship in ships:
        for x, y in ship:
            board[y][x] = "s"

def get_player_move(board):
    """
    Prompts the player to enter a valid move (coordinates)
    Returns:
        Valid (x, y) coordinates entered by the player
    """
    while True:
        raw = input("Enter your shot (x y): ")
        try:
            x, y = map(int, raw.split())
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                if board[y][x] in ["X", "."]:
                    print("Already targeted")
                else:
                    return x, y
            else:
                print("Coordinates out of board")
        except:
            print("Invalid input, try again")

def get_bot_move(board):
    """
    Randomly selects a valid move for the bot
    Returns:
        Valid (x, y) coordinates for the bot's move
    """
    available_coords = []
    for column in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            if board[row][column] not in ["X", "."]:
                available_coords.append((column, row))
    return random.choice(available_coords)

def is_ship_destroyed(ship, hits):
    """
    Checks if a ship is completely destroyed
    Returns:
        bool: True if the ship is destroyed, False otherwise
    """
    for cell in ship:
        if cell not in hits:
            return False
    return True

def mark_misses_around_ship(board, ship):
    """
    Marks '.' around a destroyed ship to indicate missed cells
    """
    for x, y in ship:
        for nx, ny in neighbors(x, y):
            if inside_board(nx, ny) and board[ny][nx] == "-":
                board[ny][nx] = "."

def apply_move(board, ships, hits, destroyed_ships, x, y):
    """
    Applies a move to the board, updating hits and checking for destroyed ships
    Returns:
        str: "hit", "miss", or "destroyed" depending on the result of the move
    """
    hits.add((x, y))

    for ship_id, ship in enumerate(ships):
        if (x, y) in ship:
            board[y][x] = "X"

            if ship_id not in destroyed_ships and is_ship_destroyed(ship, hits):
                destroyed_ships.add(ship_id)
                mark_misses_around_ship(board, ship)
                return "destroyed"

            return "hit"

    board[y][x] = "."
    return "miss"


def all_ships_sunk(destroyed_ships, ships):
    """
    Checks if all ships are destroyed
    Returns:
        bool: True if all ships are destroyed, False otherwise
    """
    return len(destroyed_ships) == len(ships)


def save_game_state(turn, player_move, bot_move, player_board, bot_board, file_path="data/game_state.csv"):
    """
    Saves the current game state to a CSV file
    """
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([turn, player_move, bot_move])
        writer.writerow(["Player Board"])
        for row in player_board:
            writer.writerow(row)
        writer.writerow(["Bot Board"])
        for row in bot_board:
            writer.writerow(row)
        writer.writerow([])

bot_targets = []  
bot_shots_taken = set()

def start_game(player_ships, bot_ships):
    """
    Starts the main game loop for Battleship, handling turns for player and bot
    """
    player_board = create_empty_board()
    bot_board = create_empty_board()

    mark_ship_on_board(player_board, player_ships)
    mark_ship_on_board(bot_board, bot_ships)

    player_hits = set()
    bot_hits = set()
    destroyed_player_ships = set()
    destroyed_bot_ships = set()

    turn = 1

    while True:
        print(f"\nTurn {turn}")
        print("Bot Board:")
        print_board(bot_board, hide_ships=True)
        print("Player Board:")
        print_board(player_board)

        # Player move
        while True:
            px, py = get_player_move(bot_board)
            player_result = apply_move(
                bot_board,
                bot_ships,
                player_hits,
                destroyed_bot_ships,
                px,
                py
            )

            if player_result == "miss":
                print("Miss!")
                break
            elif player_result == "hit":
                print("Hit!")
            else:
                print("Ship destroyed!")

            if all_ships_sunk(destroyed_bot_ships, bot_ships):
                print("Player wins!")
                return

        # Bot move
        while True:
            if bot_targets:
                while bot_targets:
                    bx, by = bot_targets.pop(0)
                    if (bx, by) not in bot_shots_taken:
                        break
                else:
                    available_coords = [
                        (x, y)
                        for y in range(BOARD_SIZE)
                        for x in range(BOARD_SIZE)
                        if (x, y) not in bot_shots_taken
                    ]
                    bx, by = random.choice(available_coords)
            else:
                available_coords = [
                    (x, y)
                    for y in range(BOARD_SIZE)
                    for x in range(BOARD_SIZE)
                    if (x, y) not in bot_shots_taken
                ]
                bx, by = random.choice(available_coords)

            bot_shots_taken.add((bx, by))
            bot_result = apply_move(
                player_board,
                player_ships,
                bot_hits,
                destroyed_player_ships,
                bx,
                by
            )

            if bot_result == "miss":
                print("Bot miss.")
                break

            elif bot_result == "hit":
                print("Bot hit your ship!")
                for nx, ny in neighbors(bx, by):
                    if (nx, ny) not in bot_shots_taken and (nx, ny) not in bot_targets:
                        bot_targets.append((nx, ny))
            else:
                print("Bot destroyed your ship!")

        save_game_state(
            turn,
            (px, py, player_result),
            (bx, by, bot_result),
            player_board,
            bot_board
        )

        turn += 1