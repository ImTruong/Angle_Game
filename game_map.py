from constants import *

class GameMap(pygame.sprite.Sprite):
    def __init__(self, x, y, image, background):
        super().__init__()
        self.image = pygame.transform.scale(image, (GAME_MAP_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.background = background

    def draw(self):
        screen.blit(self.background, self.rect.topleft)
        screen.blit(self.image, self.rect.topleft)

    def move(self, speed):
        if (self.rect.right > WINDOW_WIDTH and speed > 0) or (self.rect.left < 0 and speed < 0):
            self.rect.x -= speed

    def update_from_explosion(self, explosion_point):
        pygame.draw.circle(self.image, (255, 255, 255, 0), explosion_point, EXPLODE_RADIUS)
        self.mask = pygame.mask.from_surface(self.image)