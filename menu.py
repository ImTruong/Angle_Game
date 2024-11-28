import pygame
from constants import *
from text import Text
from button import Button

def start_menu():
    pygame.init()
    pygame.mixer_music.play(-1)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image = pygame.image.load("image/menu_background.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    start_text = Text("Welcome to ANGLE", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200, size=50, color=RED, font="freesansbold.ttf")
    game_description_text = Text("A 2D shooting game", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 150, size=25, color=BLACK, font="freesansbold.ttf")

    start_button = Button("Start", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 20, 200, 50)
    instruction_button = Button("Instructions", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    quit_button = Button("Quit", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 100, 200, 50)

    while True:
        screen.blit(background_image, (0, 0))
        start_text.draw()
        game_description_text.draw()
        start_button.draw()
        instruction_button.draw()
        quit_button.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer_music.stop()
                pygame.quit()
                quit()

            if start_button.is_clicked(event):
                return "start"
            if instruction_button.is_clicked(event):
                return "instructions"
            if quit_button.is_clicked(event):
                pygame.mixer_music.stop()
                pygame.quit()
                quit()

def instruction_page():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image = pygame.image.load("image/menu_background.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    instruction_text = Text("Instructions", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200, size=50, color=RED, font="freesansbold.ttf")
    details_lines = [
        "Use arrow keys to move and change the angle, space to jump",
        "LCTRL to power up the shot and release when you are ready to shoot",
        "LALT will make you control the screen with your mouse"
    ]
    details_texts = [Text(line, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100 + i * 30, size=25, color=BLACK, font="freesansbold.ttf") for i, line in enumerate(details_lines)]
    back_button = Button("Back", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 100, 200, 50)

    while True:
        screen.blit(background_image, (0, 0))
        instruction_text.draw()
        for details_text in details_texts:
            details_text.draw()
        back_button.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if back_button.is_clicked(event):
                return "back"

def map_selection_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image = pygame.image.load("image/menu_background.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    select_map_text = Text("Select a Map", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200, size=50, color=RED, font="freesansbold.ttf")

    sea_map_button = Button("Sea Map", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 20, 200, 50)
    moon_map_button = Button("Moon Map", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    constructor_map_button = Button("Constructor Map", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 100, 200, 50)
    back_button = Button("Back", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 160, 200, 50)

    while True:
        screen.blit(background_image, (0, 0))
        select_map_text.draw()
        sea_map_button.draw()
        moon_map_button.draw()
        constructor_map_button.draw()
        back_button.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer_music.stop()
                pygame.quit()
                quit()

            if sea_map_button.is_clicked(event):
                pygame.mixer_music.stop()
                return "SeaMap"
            if moon_map_button.is_clicked(event):
                pygame.mixer_music.stop()
                return "MoonMap"
            if constructor_map_button.is_clicked(event):
                pygame.mixer_music.stop()
                return "ConstructorMap"
            if back_button.is_clicked(event):
                return "back"

def number_of_player_selection_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image = pygame.image.load("image/menu_background.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    select_map_text = Text("Select a Number of player", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200, size=50, color=RED, font="freesansbold.ttf")

    two_player_button = Button("2 PLayer", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 20, 200, 50)
    four_player_button = Button("4 PLayer", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    back_button = Button("Back", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 160, 200, 50)

    while True:
        screen.blit(background_image, (0, 0))
        select_map_text.draw()
        two_player_button.draw()
        four_player_button.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer_music.stop()
                pygame.quit()
                quit()

            if two_player_button.is_clicked(event):
                pygame.mixer_music.stop()
                return "2"
            if four_player_button.is_clicked(event):
                pygame.mixer_music.stop()
                return "4"
            if back_button.is_clicked(event):
                return "back"


def end_menu(message):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image = pygame.image.load("image/menu_background.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    font_large = pygame.font.Font("freesansbold.ttf", 74)

    quit_button = Button("Quit", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
    start_menu_button = Button("Start Menu", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 120, 200, 50)

    while True:
        screen.blit(background_image, (0, 0))

        text = font_large.render(message, True, BLACK)
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2 - 100))

        quit_button.draw()
        start_menu_button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if quit_button.is_clicked(event):
                pygame.quit()
                quit()
            if start_menu_button.is_clicked(event):
                return

def stop_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image = pygame.image.load("image/menu_background.jpg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    font_large = pygame.font.Font("freesansbold.ttf", 74)

    resume_button = Button("Resume", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20, 200, 50)
    quit_button = Button("Quit", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)

    while True:
        screen.blit(background_image, (0, 0))

        text = font_large.render("Paused", True, BLACK)
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2 - 100))

        resume_button.draw()
        quit_button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if resume_button.is_clicked(event):
                return
            if quit_button.is_clicked(event):
                pygame.quit()
                quit()