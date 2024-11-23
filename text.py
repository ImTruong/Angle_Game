import pygame
from constants import *

class Text:
    def __init__(self, text, x, y, font=None, size=36, color=BLACK):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.text, self.rect)