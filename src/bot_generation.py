import csv
import random
from src.utils import inside_board, neighbors

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def generate_bot_ships():
    ships = []
    occupied = set()

    for size in SHIP_SIZES:
        while True:
            orientation = random.choice(["horizontal", "vertical"])

            if orientation == "horizontal":
                x_start = random.randint(0, 10 - size)
                y_start = random.randint(0, 9)
                ship_cells = [(x_start + i, y_start) for i in range(size)]
            else:
                x_start = random.randint(0, 9)
                y_start = random.randint(0, 10 - size)
                ship_cells = [(x_start, y_start + i) for i in range(size)]

            ships_touch = False
            for x, y in ship_cells:
                if (x, y) in occupied:
                    ships_touch = True
                for nx, ny in neighbors(x, y):
                    if (nx, ny) in occupied:
                        ships_touch = True

            if ships_touch:
                continue

            for s in ship_cells:
                occupied.add(s)
            ships.append(ship_cells)
            break

    with open("data/bot_ships.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for ship in ships:
            for x, y in ship:
                writer.writerow([x, y])
            writer.writerow([])

    return ships

if __name__ == "__main__":
    bot_ships = generate_bot_ships()
    print("Bot ships generated:")
    for ship in bot_ships:
        print(ship)
