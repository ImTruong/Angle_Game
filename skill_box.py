import pygame

from constants import RED, ORANGE


class skill_box:
    def __init__(self, x, y, width, height, skill_image, skill_name):
        self.rect = pygame.Rect(x, y, width, height)
        self.skill_image = skill_image
        self.skill_name = skill_name
        self.is_used = False

    def draw(self, screen, selected = False,used = False):
        """Vẽ kỹ năng lên màn hình với viền đặc biệt nếu được nhấn hoặc sử dụng."""
        skill_surface = self.skill_image.copy()

        # Vẽ hình ảnh kỹ năng
        screen.blit(skill_surface, self.rect.topleft)

        # Thay đổi màu viền dựa trên trạng thái
        border_color = ORANGE if selected else RED  # Cam nếu được chọn, đỏ nếu không
        pygame.draw.rect(screen, border_color, self.rect, 2)

        if used:
            pygame.draw.line(screen, RED, self.rect.topleft, self.rect.bottomright, 2)

    def mark_as_used(self):
        """Đánh dấu kỹ năng đã được sử dụng."""
        self.is_used = True
