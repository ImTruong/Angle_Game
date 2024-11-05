import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, pos: tuple[int, int], direction: pygame.math.Vector2, speed: float, time_life: int):
        super().__init__(groups)
        self.pos = pos
        self.direction = direction
        self.speed = speed
        self.time_life = time_life
        self.image = pygame.image.load('./image/Fire0.png')
        self.rect = self.image.get_rect()
        self.current_tick = 0
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.move()
        self.check_time_life()

    def move(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_time_life(self):
        self.current_tick = pygame.time.get_ticks()
        if self.current_tick - self.start_time >= self.time_life * 1000:
            self.kill()