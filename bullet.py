import pygame

from main import screen


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, shooter):
        super().__init__()
        self.image = pygame.transform.scale(image, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0
        self.hit_target = False
        self.shooter = shooter
        self.count = 0

    def update(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect.topleft)