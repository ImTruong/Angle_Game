import math

import pygame.image

from skill_box import skill_box
from sprite_animated import SpriteAnimated
from bullet import *
from constants import *

class Character(pygame.sprite.Sprite):
    def __init__(self, display_image, real_image, x, y, width, height):
        super().__init__()
        self.display_image = pygame.transform.scale(display_image, (width, height))
        self.real_image = pygame.transform.scale(real_image, (width, height))
        self.rect = self.real_image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.real_image)
        self.face_right = True
        self.shoot_angle = MIN_SHOOT_ANGLE_DISPLAY
        self.speed = 0
        self.on_ground = False
        self.jumping = False
        self.velocity = BASE_VELOCITY
        self.power = 0
        self.teleport = True
        self.freeze = 0
        self.frozen_bullet = True
        self.heal_bullet = True
        self.continuous_bullet = True
        self.shooting = False
        self.HP = 100
        self.max_HP = 100
        self.screen = screen
        self.width = width
        self.height = height
        self.character_animation = SpriteAnimated(screen, "idle", 0.1)
        self.turn = False

        # Khởi tạo các kỹ năng
        tele_img = pygame.image.load("image/teleport_skill.jpg")
        freeze_img = pygame.image.load("image/freeze_skill.png")
        heal_img = pygame.image.load("image/healing.jpg")
        continous_img = pygame.image.load("image/continuous_bullet.png")


        skill1 = skill_box(20, 100, SKILL_BOX_SIZE, SKILL_BOX_SIZE, tele_img, "Teleport")
        skill2 = skill_box(20, 175, SKILL_BOX_SIZE, SKILL_BOX_SIZE, freeze_img, "Frozen Bullet")
        skill3 = skill_box(20, 250, SKILL_BOX_SIZE, SKILL_BOX_SIZE, heal_img, "Heal Bullet")
        skill4 = skill_box(20, 325, SKILL_BOX_SIZE, SKILL_BOX_SIZE, continous_img, "Continuous Bullet")

        self.skills = [skill1, skill2, skill3, skill4]

    def draw_skills(self, screen, selected_skill):
        """Vẽ tất cả kỹ năng của nhân vật."""
        for skill in self.skills:
            skill_name = skill.skill_name.lower().replace(" ", "_")
            used = not getattr(self, skill_name, True)  # Chiêu đã dùng nếu trạng thái là False
            selected = skill.skill_name == selected_skill  # Được chọn nếu khớp với selected_skill
            skill.draw(screen, selected=selected, used=used)

    def angle(self, game_map):
        if not self.on_ground:
            return 0
        for i in range(0, game_map.rect.bottom):
            overlap_pos = self.mask.overlap(game_map.mask,
                                            (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y - i))
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

    def draw(self, screen, camera, angle, current_player, moving, shooting, character_angle_line_image, charging, delay_time, freeze_image):
        self.display_image = self.character_animation.image
        flipped_image = pygame.transform.flip(self.display_image, not self.face_right, False)
        rotated_image = pygame.transform.rotate(flipped_image, angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)

        new_rect.topleft = camera.apply(self).topleft

        if not moving and current_player == self and not shooting and not self.jumping and delay_time is None:
            rotated_angle = angle + self.shoot_angle if self.face_right else angle - self.shoot_angle

            rotated_angle_line_image = pygame.transform.rotate(character_angle_line_image, rotated_angle)
            angle_line_rect = rotated_angle_line_image.get_rect(center=self.rect.center)

            angle_line_rect.center = camera.apply(self).center

            if (self.face_right and rotated_angle < 90) or (not self.face_right and rotated_angle < -90):
                cover_rect = pygame.Rect(0, 0, rotated_angle_line_image.get_width() // 2,
                                         rotated_angle_line_image.get_height())
            else:
                cover_rect = pygame.Rect(rotated_angle_line_image.get_width() // 2, 0,
                                         rotated_angle_line_image.get_width() // 2,
                                         rotated_angle_line_image.get_height())

            pygame.draw.rect(rotated_angle_line_image, (0, 0, 0, 0), cover_rect)
            screen.blit(rotated_angle_line_image, angle_line_rect.topleft)

        if not moving and current_player == self and not shooting and not self.jumping and not self.falling and not charging:
            self.character_animation.state = "idle"
        elif moving and current_player == self and not shooting and not self.jumping and not self.falling:
            self.character_animation.state = "move"
            self.character_animation.setCenterPos(self.rect.center)
        elif self.jumping and current_player == self and not shooting:
            self.character_animation.state = "jump"
            self.character_animation.setCenterPos(self.rect.center)
        elif self.falling and not shooting:
            self.character_animation.state = "jump"
            self.character_animation.setCenterPos(self.rect.center)
        elif not self.falling and not moving and not charging and not self.jumping:
            self.character_animation.state = "idle"
            self.character_animation.setCenterPos(self.rect.center)
        elif charging and current_player == self:
            self.character_animation.state = "shooting"
            self.character_animation.setCenterPos(self.rect.center)

        screen.blit(rotated_image, new_rect.topleft)
        if self.freeze > 0:
            flipped_freeze_image = pygame.transform.flip(freeze_image, not self.face_right, False)
            rotated_freeze_image = pygame.transform.rotate(flipped_freeze_image, angle)
            freeze_rect = rotated_freeze_image.get_rect(center=new_rect.center)
            screen.blit(rotated_freeze_image, freeze_rect.topleft)
    def move(self, game_map):
        self.rect.x += self.speed

        if self.rect.x < 1:
            self.rect.x = game_map.rect.left
        if self.rect.left > game_map.rect.right - LIMIT_MOVING_RIGHT:
            self.rect.left = game_map.rect.right - LIMIT_MOVING_RIGHT

    def update(self, game_map):
        self.character_animation.update()
        self.handle_falling(game_map)
        self.check_on_ground(game_map)
        self.jump(game_map)

    def handle_falling(self, game_map):
        if not self.jumping and not self.mask.overlap(game_map.mask,
                                                      (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y)):
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
            self.falling = False
        else:
            self.falling = True

    def jump(self, game_map):
        if self.jumping:
            if self.velocity >= -JUMP_HEIGHT and not self.mask.overlap(
                    game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y + self.velocity)):
                self.rect.y -= self.velocity + 2
                self.velocity -= GRAVITY
            else:
                self.jumping = False
                self.velocity = JUMP_HEIGHT  # Reset vận tốc cho lần nhảy sau

    def check_collision_with_game_map_y(self, game_map):
        movable = False
        sign = 1 if self.speed > 0 else -1
        self.speed = DEFAULT_CHARACTER_SPEED * sign
        for i in range(1, int(abs(self.speed) + 1)):
            overlap_pos = self.mask.overlap(game_map.mask,
                                            (game_map.rect.x - self.rect.x - i * sign, game_map.rect.y - self.rect.y))
            if overlap_pos == None or self.height - overlap_pos[1] <= HEIGHT_DIFF_ALLOWED:
                movable = True
                speed = i * sign
                if overlap_pos != None:
                    self.rect.y -= (self.height - overlap_pos[1])
        return movable

    def shoot(self, bullet, game_map):
        angle = self.shoot_angle
        if self.face_right:
            angle += self.angle(game_map)
        else:
            angle += -self.angle(game_map)

        direction = 1 if self.face_right else -1

        if isinstance(bullet, ContinuousBullet):
            theta = angle * math.pi / 180
            t = bullet.time
            x0, y0 = self.rect.center
            V = 50
            x0, y0 = (
                self.rect.topleft if not self.face_right else self.rect.topright
            )
            x = x0 + direction * V * math.cos(theta) * t
            y = y0 + -V * math.sin(theta) * t
            bullet.update(x, y)
        else:
            theta = angle * math.pi / 180
            accel = BULLET_ACCEL
            t = bullet.time
            scale = POWER_SCALE
            V = scale * self.power
            x0, y0 = (
                self.rect.topleft if not self.face_right else self.rect.topright
            )
            x = x0 + direction * V * math.cos(theta) * t
            y = y0 + (-V * math.sin(theta) * t + accel * t ** 2 / 2)
            bullet.update(x, y)

    def check_collision_with_explode_point(self, bullet, explosion_center):
        explosion_mask = pygame.mask.Mask((EXPLODE_RADIUS * 2, EXPLODE_RADIUS * 2), fill=True)
        explosion_rect = explosion_mask.get_rect(center=explosion_center)

        if self.mask.overlap(explosion_mask, (explosion_rect.x - self.rect.x, explosion_rect.y - self.rect.y)):
            return True
        return False

    def draw_health_bar(self, camera):
        bar_x = self.rect.centerx - BAR_WIDTH // 2
        bar_y = self.rect.bottom + BAR_OFFSET_Y

        bar_x, bar_y = camera.apply((bar_x, bar_y))

        current_health_width = int(BAR_WIDTH * (self.HP / self.max_HP))

        pygame.draw.rect(screen, HEALTH_BAR_BG_COLOR, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, HEALTH_BAR_COLOR, (bar_x, bar_y, current_health_width, BAR_HEIGHT))

    def draw_power_bar(self):
        power_ratio = self.power / 100
        power_bar_x = (WINDOW_WIDTH - POWER_BAR_WIDTH) // 2
        power_bar_y = WINDOW_HEIGHT - POWER_BAR_Y_OFFSET

        pygame.draw.rect(screen, POWER_BAR_BG_COLOR, (power_bar_x, power_bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT))
        pygame.draw.rect(screen, POWER_BAR_COLOR,
                         (power_bar_x, power_bar_y, POWER_BAR_WIDTH * power_ratio, POWER_BAR_HEIGHT))

        font = pygame.font.Font(None, POWER_BAR_FONT_SIZE)
        for i in range(0, 101, 10):
            x_position = power_bar_x + (i / 100) * POWER_BAR_WIDTH
            text_surface = font.render(str(i), True, BLACK)
            text_rect = text_surface.get_rect(center=(x_position, power_bar_y + POWER_BAR_HEIGHT + 10))
            screen.blit(text_surface, text_rect.topleft)

    def draw_turn_marker(self, player_name, is_turn, camera):
        """Vẽ chỉ báo lượt chơi phía trên nhân vật."""
        # Tọa độ của tam giác
        pointer_x = self.rect.centerx
        pointer_y = self.rect.top - 30

        # Áp dụng camera
        pointer_x, pointer_y = camera.apply((pointer_x, pointer_y))

        # Cài đặt màu sắc và font tùy thuộc vào lượt
        if is_turn:
            triangle_color = (255, 0, 0)  # Tam giác màu đỏ
            text_color = (0, 0, 0)  # Chữ màu đen
        else:
            triangle_color = (169, 169, 169)  # Tam giác màu xám (DarkGray)
            text_color = (105, 105, 105)  # Chữ màu xám (DimGray)

        triangle_points = [
            (pointer_x, pointer_y + 10),
            (pointer_x - 10, pointer_y),
            (pointer_x + 10, pointer_y)
        ]
        pygame.draw.polygon(self.screen, triangle_color, triangle_points)


        font = pygame.font.Font(None, PLAY_MARKER_FONT_SIZE)

        text_surface = font.render(player_name, True, text_color)
        text_rect = text_surface.get_rect(center=(pointer_x, pointer_y - 10))
        self.screen.blit(text_surface, text_rect)


