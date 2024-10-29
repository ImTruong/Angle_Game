import pygame
import math
from settings import *
from bullet import Bullet

class Character(pygame.sprite.Sprite):
    def __init__(self, display_image, real_image, x, y):
        super().__init__()
        self.display_image = pygame.transform.scale(display_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.real_image = pygame.transform.scale(real_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.rect = self.real_image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.real_image)
        self.face_right = True
        self.shoot_angle = MIN_SHOOT_ANGLE_DISPLAY
        self.speed = 0
        self.on_ground = False
        self.jumping = False
        self.velocity = BASE_VELOCITY
        self.power = 0
        self.shooting = False

    def angle(self, game_map):
        if not self.on_ground:
            return 0
        for i in range(0, game_map.rect.bottom):
            overlap_pos = self.mask.overlap(game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y - i))
            if overlap_pos:
                break
        left_y_point = 0
        right_y_point = 0
        for i in range(self.rect.centery, game_map.rect.bottom):
            if game_map.mask.get_at((self.rect.left, i)):
                left_y_point = i
                break
        for i in range(self.rect.centery, game_map.rect.bottom):
            if game_map.mask.get_at((self.rect.right, i)):
                right_y_point = i
                break
        slope = (left_y_point - right_y_point) / (self.rect.left - self.rect.right)
        return -math.atan(slope) * 180 / (math.pi)

    def draw(self, screen, angle, current_player, moving, shooting, character_angle_line_image):
        flipped_image = pygame.transform.flip(self.display_image, not self.face_right, False)
        rotated_image = pygame.transform.rotate(flipped_image, angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        if not moving and current_player == self and not shooting:
            rotated_angle = angle + self.shoot_angle
            if not self.face_right:
                rotated_angle = angle - self.shoot_angle
            rotated_angle_line_image = pygame.transform.rotate(character_angle_line_image, rotated_angle)
            angle_line_rect = rotated_angle_line_image.get_rect(center=self.rect.center)
            if self.face_right:
                cover_rect = pygame.Rect(0, 0, rotated_angle_line_image.get_width() // 2, rotated_angle_line_image.get_height())
            else:
                cover_rect = pygame.Rect(rotated_angle_line_image.get_width() // 2, 0, rotated_angle_line_image.get_width() // 2, rotated_angle_line_image.get_height())
            pygame.draw.rect(rotated_angle_line_image, (255, 255, 255, 0), cover_rect)
            screen.blit(rotated_angle_line_image, angle_line_rect.topleft)
        screen.blit(rotated_image, new_rect.topleft)

    def move(self, game_map):
        self.rect.x += self.speed
        if self.rect.x < game_map.rect.left:
            self.rect.x = game_map.rect.left
        if self.rect.left > game_map.rect.right:
            self.rect.left = game_map.rect.right

    def update(self, game_map):
        self.handle_falling(game_map)
        self.check_on_ground(game_map)
        self.jump(game_map)

    def handle_falling(self, game_map):
        if not self.jumping and not self.mask.overlap(game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y)):
            down = 0
            for i in range(0, int(self.velocity)):
                down = i
                if self.mask.overlap(game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y - i)):
                    break
            self.rect.y += down
            if self.velocity + GRAVITY < MAX_FALL_SPEED:
                self.velocity += GRAVITY
            self.on_ground = False

    def check_on_ground(self, game_map):
        if self.mask.overlap(game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y)):
            self.velocity = BASE_VELOCITY
            self.on_ground = True

    def jump(self, game_map):
        if self.jumping:
            if self.velocity >= JUMP_HEIGHT or self.mask.overlap(game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y + self.velocity)):
                self.jumping = False
                self.velocity = JUMP_HEIGHT
            else:
                self.rect.y -= self.velocity
                self.velocity += GRAVITY

    def check_collision_with_game_map_y(self, game_map):
        movable = False
        sign = 1 if self.speed > 0 else -1
        self.speed = DEFAULT_CHARACTER_SPEED * sign
        for i in range(1, int(abs(self.speed) + 1)):
            overlap_pos = self.mask.overlap(game_map.mask, (game_map.rect.x - self.rect.x - i * sign, game_map.rect.y - self.rect.y))
            if overlap_pos == None or CHARACTER_HEIGHT - overlap_pos[1] <= HEIGHT_DIFF_ALLOWED:
                movable = True
                speed = i * sign
                if overlap_pos != None:
                    self.rect.y -= (CHARACTER_HEIGHT - overlap_pos[1])
        return movable

    def shoot(self, bullet, game_map):
        angle = self.shoot_angle
        if self.face_right:
            angle += self.angle(game_map)
        else:
            angle += -self.angle(game_map)
        direction = 1 if self.face_right else -1
        theta, accel, t = angle * math.pi / 180, BULLET_ACCEL, bullet.time
        scale = POWER_SCALE
        V = scale * self.power
        x0, y0 = self.rect.center
        x = x0 + direction * V * math.cos(theta) * t
        y = y0 + (-V * math.sin(theta) * t + accel * t ** 2 / 2)
        bullet.update(x, y)