from text import Text
from constants import *

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