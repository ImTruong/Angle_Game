import pygame
from settings import *
from ui import Text, Button

def start_menu(screen, clock):
    screen.fill(WHITE)
    start_text = Text("Welcome to ANGLE", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100, size=40, color=GREEN, font="freesansbold.ttf")
    game_description_text = Text("Angle your shot to hit the enemy", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50, size=20, color=BLACK, font="freesansbold.ttf")
    tutorial_text = Text("Use arrow keys to move and space to shoot", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20, size=20, color=RED, font="freesansbold.ttf")

    start_button = Button("Start", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    quit_button = Button("Quit", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 110, 200, 50)

    while True:
        screen.fill(WHITE)
        start_text.draw(screen)
        game_description_text.draw(screen)
        tutorial_text.draw(screen)
        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if start_button.is_clicked(event):
                return
            if quit_button.is_clicked(event):
                pygame.quit()
                quit()