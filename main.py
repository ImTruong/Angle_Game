from game_loop import main_game_loop
from menu import *
from game_map import SeaMap, MoonMap, ConstructorMap

pygame.init()
pygame.display.set_caption("Angle_game")

while True:
    selected_option = start_menu()
    game_map = None
    number_of_player = None
    if selected_option == "start":
        selected_map = map_selection_menu()
        if selected_map == "back":
            continue
        if selected_map == "SeaMap":
            game_map = SeaMap(0, 0)
        elif selected_map == "MoonMap":
            game_map = MoonMap(0, 0)
        elif selected_map == "ConstructorMap":
            game_map = ConstructorMap(0, 0)
    elif selected_option == "instructions":
        instruction_page()
    elif selected_option == "quit":
        pygame.quit()
        quit()
    if game_map:
        number_of_player = number_of_player_selection_menu()
        if number_of_player == "back":
            continue
        elif number_of_player == "2":
            main_game_loop(game_map, 2)
        elif number_of_player == "4":
            main_game_loop(game_map, 4)