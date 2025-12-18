import csv
from src.utils import inside_board, neighbors

SHIP_SIZES = [4,3,3,2,2,2,1,1,1,1]

def read_player_ships():
    ships = []
    occupied = set()

    for size in SHIP_SIZES:
        while True:
            raw = input(f"Enter ship of size {size}: ")
            coordinates = list(map(int, raw.split()))
            ship_cells = [(coordinates[i], coordinates[i+1]) for i in range(0, len(coordinates), 2)]

            if len(ship_cells) != size:
                print("Wrong ship size")
                continue

            outside_board = False
            for x, y in ship_cells:
                if not inside_board(x, y):
                    outside_board = True
                    break
                
            if outside_board:
                print("Ship outside board")
                continue

            x_coords = {x for x, y in ship_cells}
            y_coords = {y for x, y in ship_cells}
            if not (len(x_coords) == 1 or len(y_coords) == 1):
                print("Ship must be straight")
                continue

            ships_touch = False
            for x, y in ship_cells:
                if (x, y) in occupied:
                    ships_touch = True
                for nx, ny in neighbors(x, y):
                    if (nx, ny) in occupied:
                        ships_touch = True

            if ships_touch:
                print("Ships touch")
                continue

            for s in ship_cells:
                occupied.add(s)
            ships.append(ship_cells)
            break

    with open("data/player_ships.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for ship in ships:
            for x, y in ship:
                writer.writerow([x, y])
            writer.writerow([])

    return ships
