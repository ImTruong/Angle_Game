
from constants import *
from menu import start_menu
from game_loop import main_game_loop

pygame.init()
pygame.display.set_caption("Angle_game")

start_menu()
main_game_loop()