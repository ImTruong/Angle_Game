import pygame

from main import screen
from settings import *
from ui import Text, Button

def start_menu():
    screen.fill(WHITE)
    start_text = Text("Welcome to ANGLE", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100, size=40, color=GREEN, font="freesansbold.ttf")
    game_description_text = Text("Angle your shot to hit the enemy", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50, size=20, color=BLACK, font="freesansbold.ttf")
    tutorial_text = Text("Use arrow keys to move and space to shoot", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20, size=20, color=RED, font="freesansbold.ttf")

    start_button = Button("Start", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    start_over_btn = Button("Start Over", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    quit_button = Button("Quit", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 110, 200, 50)

    while True:
        screen.fill(WHITE)
        start_text.draw()
        game_description_text.draw()
        tutorial_text.draw()
        start_button.draw()
        quit_button.draw()
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


def end_game_screen(winner):
    global game_over

    # Vẽ thông báo người thắng
    font = pygame.font.SysFont(None, 60)
    text = font.render(f"{winner} Wins!", True, (205,133,63))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

    # Tạo các nút
    start_over_button = Button("Start Over", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20, 200, 50,
                               font_color=BLACK)

    # Hiển thị màn hình kết thúc cho đến khi nhấn nút
    while True:
        screen.fill(WHITE)
        screen.blit(text, text_rect)
        start_over_button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif start_over_button.is_clicked(event):
                game_over = False
                return "restart"