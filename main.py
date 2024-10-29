import pygame
from settings import *
from menu import start_menu
from game_loop import main_game_loop

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gunny")
clock = pygame.time.Clock()

start_menu(screen, clock)
main_game_loop(screen, clock)