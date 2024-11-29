import pygame
from constants import RED, ORANGE, GRAY  # Màu xám thêm vào

class skill_box:
    def __init__(self, x, y, width, height, skill_image, skill_name):
        self.rect = pygame.Rect(x, y, width, height)
        self.skill_image = skill_image
        self.skill_name = skill_name
        self.is_used = False

    def draw(self, screen, selected=False, used=False):
        skill_surface = self.skill_image.copy()


        screen.blit(skill_surface, self.rect.topleft)
        if used:
            border_color = GRAY
        else:
            border_color = ORANGE if selected else RED

        pygame.draw.rect(screen, border_color, self.rect, 2)

        if used:
            pygame.draw.line(screen, RED, self.rect.topleft, self.rect.bottomright, 2)

    def mark_as_used(self):
        self.is_used = True
