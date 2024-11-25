import pygame
from constants import *
class Camera:
    def __init__(self, x, y):
        self.camera = pygame.Rect(0, 0, x, y)
        self.x = x
        self.y = y

    def apply(self, entity):
        if hasattr(entity, 'rect'):
            return entity.rect.move(self.camera.topleft)
        else:
            return (entity[0] + self.camera.x, entity[1] + self.camera.y)

    def update(self, target):
        x = -target.rect.centerx + int(WINDOW_WIDTH / 2)
        y = -target.rect.centery + int(WINDOW_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.x - WINDOW_WIDTH), x)
        y = max(-(self.y - WINDOW_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.x, self.y)