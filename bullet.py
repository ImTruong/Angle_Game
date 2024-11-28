from constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, shooter, size):
        super().__init__()
        self.image = pygame.transform.scale(image, (size, size))
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

class NormalBullet(Bullet):
    def __init__(self, shooter):
        super().__init__(pygame.image.load("./image/CannonBullet.png").convert_alpha(), shooter, 20)

class IceBullet(Bullet):
    def __init__(self, shooter):
        super().__init__(pygame.image.load("./image/ice_bullet.png").convert_alpha(), shooter, 25)

class TeleportBullet(Bullet):
    def __init__(self, shooter):
        super().__init__(pygame.image.load("./image/plane_bullet.png").convert_alpha(), shooter, 20)

class HealBullet(Bullet):
    def __init__(self, shooter):
        super().__init__(pygame.image.load("./image/heal_bullet.png").convert_alpha(), shooter, 20)

class ContinuousBullet(Bullet):
    def __init__(self, shooter):
        super().__init__(pygame.image.load("./image/continuous_bullet.png").convert_alpha(), shooter, 20)