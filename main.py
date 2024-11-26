from constants import *
from menu import start_menu, instruction_page, map_selection_menu
from game_loop import main_game_loop
from game_map import SeaMap, MoonMap, ConstructorMap

pygame.init()
pygame.display.set_caption("Angle_game")

while True:
    selected_option = start_menu()

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
        else :
            continue
        main_game_loop(game_map)
    elif selected_option == "instructions":
        instruction_page()
    elif selected_option == "quit":
        pygame.quit()
        quit()