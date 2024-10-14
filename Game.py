import math
import pygame

pygame.init()

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
CHARACTER_WIDTH = 40
CHARACTER_HEIGHT = 40
GAME_MAP_WIDTH = 1500
SPEED = 3
GRAVITY = 0.3
HEIGHT_DIFF_ALLOWED = 5
JUMP_HEIGHT = 7
MAX_FALL_SPEED = 13
BASE_VELOCITY = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gunny")
clock = pygame.time.Clock()

class GameMap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.transform.scale(game_map_image, (GAME_MAP_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def move(self, speed):
        if (self.rect.right > WINDOW_WIDTH and speed > 0) or (self.rect.left < 0 and speed < 0):
            self.rect.x -= speed

class Character(pygame.sprite.Sprite):
    def __init__(self, display_image, real_image, x, y):
        self.display_image = pygame.transform.scale(display_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.real_image = pygame.transform.scale(real_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.rect = self.real_image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.real_image)
    def draw(self):
        screen.blit(self.display_image, self.rect)

    def move(self, speed):
        self.rect.x += speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WINDOW_WIDTH - CHARACTER_WIDTH:
            self.rect.x = WINDOW_WIDTH - CHARACTER_WIDTH

class Text:
    def __init__(self, text, x, y, font=None, size=36, color=BLACK):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.text, self.rect)

class Button:
    def __init__(self, text, x, y, width, height, font=None, font_size=36, font_color=BLACK, color=GREEN, hover_color=DARK_GREEN):
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = Text(text, x + width // 2, y + height // 2, font=font, size=font_size, color=font_color)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        self.text.draw()

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

character_display_image = pygame.image.load("./image/clipart1580513.png").convert_alpha()
character_real_image = pygame.image.load("./image/clipart1580513 (3).png").convert_alpha()
game_map_image = pygame.image.load("./image/Reloaded_Jurassic_small.png").convert_alpha()

character = Character(character_display_image, character_real_image, 400, 0)
game_map = GameMap(0, 0)

def start_menu():
    screen.fill(WHITE)
    start_text = Text("Welcome to ANGLE", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100, size=40, color=GREEN, font="freesansbold.ttf")
    game_description_text = Text("Angle your shot to hit the enemy", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50, size=20, color=BLACK, font="freesansbold.ttf")
    tutorial_text = Text("Use arrow keys to move and space to shoot", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20, size=20, color=RED, font="freesansbold.ttf")

    start_button = Button("Start", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
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

def main_game_loop():
    move_left, move_right = False, False
    speed = SPEED
    jumping = False
    velocity = BASE_VELOCITY
    on_ground = True

    def handle_movement():
        handle_falling()
        check_on_ground()
        jump()
        if move_left or move_right:
            if check_collision_with_game_map():
                if (game_map.rect.right <= WINDOW_WIDTH and character.rect.centerx >= WINDOW_HEIGHT / 2) or (game_map.rect.left >= 0 and character.rect.centerx <= WINDOW_HEIGHT / 2):
                    character.move(speed)
                else:
                    game_map.move(speed)
                    character.rect.centerx = WINDOW_HEIGHT / 2

    def handle_falling():
        nonlocal velocity
        nonlocal on_ground
        if not jumping and not character.mask.overlap(game_map.mask, (game_map.rect.x - character.rect.x, game_map.rect.y - character.rect.y)):
            down = 0
            for i in range(0, int(velocity)):
                down = i
                if character.mask.overlap(game_map.mask, (game_map.rect.x - character.rect.x, game_map.rect.y - character.rect.y - i )):
                    break
            character.rect.y += down
            if velocity + GRAVITY < MAX_FALL_SPEED:
                velocity += GRAVITY
            on_ground = False

    def check_on_ground():
        nonlocal velocity
        nonlocal on_ground
        if character.mask.overlap(game_map.mask, (game_map.rect.x - character.rect.x, game_map.rect.y - character.rect.y )):
            velocity = BASE_VELOCITY
            on_ground = True

    def jump():
        nonlocal velocity
        nonlocal jumping
        if jumping:
            if velocity >= JUMP_HEIGHT or character.mask.overlap(game_map.mask, (game_map.rect.x - character.rect.x, game_map.rect.y - character.rect.y + velocity)):
                jumping = False
                velocity = JUMP_HEIGHT
            else:
                character.rect.y -= velocity
                velocity += GRAVITY

    def check_collision_with_game_map():
        nonlocal speed
        movable = False
        sign = 1 if speed > 0 else -1
        speed = SPEED * sign
        for i in range(1, int(abs(speed)+1)):
            overlap_pos = character.mask.overlap(game_map.mask, (game_map.rect.x - character.rect.x - i * sign, game_map.rect.y - character.rect.y ))
            if overlap_pos==None or CHARACTER_HEIGHT-overlap_pos[1] <= HEIGHT_DIFF_ALLOWED:
                movable = True
                speed = i * sign
                if overlap_pos!=None: character.rect.y -= (CHARACTER_HEIGHT-overlap_pos[1])
        return movable
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if speed > 0:
                        speed *= -1
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    if speed < 0:
                        speed *= -1
                    move_right = True
                if event.key == pygame.K_SPACE:
                    if not jumping and on_ground:
                        jumping = True
                        on_ground = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False

        screen.fill(WHITE)
        handle_movement()

        game_map.draw()
        character.draw()

        pygame.display.update()
        clock.tick(60)

start_menu()
main_game_loop()