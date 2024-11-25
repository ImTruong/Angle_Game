from constants import *

class GameMap(pygame.sprite.Sprite):
    def __init__(self, x, y, image, background,
                 game_map_width,
                 game_map_height,
                 character_width,
                 character_height,
                 bullet_size):
        super().__init__()
        self.image = pygame.transform.scale(image, (game_map_width, game_map_height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.background = pygame.transform.scale(background, (game_map_width, game_map_height))
        self.GAME_MAP_WIDTH = game_map_width
        self.GAME_MAP_HEIGHT = game_map_height
        self.CHARACTER_WIDTH = character_width
        self.CHARACTER_HEIGHT = character_height
        self.BULLET_SIZE = bullet_size

    def draw(self, camera):
        screen.blit(self.background, camera.apply(self))
        screen.blit(self.image, camera.apply(self))


    def update_from_explosion(self, explosion_point):
        pygame.draw.circle(self.image, (255, 255, 255, 0), explosion_point, EXPLODE_RADIUS)
        self.mask = pygame.mask.from_surface(self.image)


class SeaMap(GameMap):
    def __init__(self, x, y):
        self.game_map_width = 1900
        self.game_map_height = 800
        self.character_width = 40
        self.character_height = 40
        self.bullet_size = 20

        super().__init__(
            x, y,
            pygame.image.load("image/sea_map.png").convert_alpha(),
            pygame.image.load("./image/sea_background.png"),
            self.game_map_width,
            self.game_map_height,
            self.character_width,
            self.character_height,
            self.bullet_size
        )


class SonicMap(GameMap):
    def __init__(self, x, y):
        self.game_map_width = 8000
        self.game_map_height = 3000
        self.character_width = 40
        self.character_height = 40
        self.bullet_size = 20

        super().__init__(
            x, y,
            pygame.image.load("image/sonic_map.png").convert_alpha(),
            pygame.image.load("./image/sea_background.png"),
            self.game_map_width,
            self.game_map_height,
            self.character_width,
            self.character_height,
            self.bullet_size
        )
