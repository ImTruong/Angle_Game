from constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, shooter):
        super().__init__()
        self.image = pygame.transform.scale(image, (20, 20))
        self.rect = self.image.get_rect(center=(shooter.rect.centerx, shooter.rect.centery))
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0
        self.hit_target = False
        self.count = 0

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, camera):
        rect_topleft_with_camera = camera.apply(self.rect.topleft)
        screen.blit(self.image, rect_topleft_with_camera)