import os
from src.ship_input import read_player_ships
from src.bot_generation import generate_bot_ships
from src.gameplay import start_game

def main():
    print("~~~ Battleship Game ~~~")
    
    if os.path.exists("data/player_ships.csv"):
        os.remove("data/player_ships.csv")
    if os.path.exists("data/bot_ships.csv"):
        os.remove("data/bot_ships.csv")

    print("Player ship setup")
    player_ships = read_player_ships()  

    print("Bot ship generation")
    bot_ships = generate_bot_ships()   

    print("Starting game")
    start_game(player_ships, bot_ships)

if __name__ == "__main__":
    main()
