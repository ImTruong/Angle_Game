import math

import pygame

pygame.init()

BULLET_DAMAGE = 25

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
CHARACTER_WIDTH = 40
CHARACTER_HEIGHT = 40
GAME_MAP_WIDTH = 1500
DEFAULT_CHARACTER_SPEED = 3
GRAVITY = 0.3
HEIGHT_DIFF_ALLOWED = 5
JUMP_HEIGHT = 7
MAX_FALL_SPEED = 13
BASE_VELOCITY = 3
MIN_SHOOT_ANGLE_DISPLAY = 16
MAX_SHOOT_ANGLE_DISPLAY = 45
BULLET_SPEED = 0.1
BULLET_ACCEL = 5
POWER_SCALE = 1
EXPLODE_RADIUS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gunny")
clock = pygame.time.Clock()

character_display_image = pygame.image.load("./image/clipart1580513.png").convert_alpha()
character_real_image = pygame.image.load("./image/clipart1580513 (1).png").convert_alpha()
game_map_image = pygame.image.load("./image/Reloaded_Jurassic_small.png").convert_alpha()
character_angle_line_image = pygame.image.load("./image/Dotted-Line-PNG-Pic.png").convert_alpha()
character_angle_line_image = pygame.transform.scale(character_angle_line_image, (89, 10))
bullet_image = pygame.image.load("./image/CannonBullet1.png").convert_alpha()

class GameMap(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (GAME_MAP_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def move(self, speed):
        if (self.rect.right > WINDOW_WIDTH and speed > 0) or (self.rect.left < 0 and speed < 0):
            self.rect.x -= speed

    def update_from_explosion(self, explosion_point):
        pygame.draw.circle(self.image, (255, 255, 255, 0), explosion_point, EXPLODE_RADIUS)
        self.mask = pygame.mask.from_surface(self.image)

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
        self.HP = 100
        self.max_HP = 100

    def angle(self, game_map):
        if not self.on_ground:
            return 0
        for i in range(0, game_map.rect.bottom):
            overlap_pos = self.mask.overlap(game_map.mask,(game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y - i))
            if overlap_pos:
                break
        left_y_point = 0
        right_y_point = 0
        for i in range(self.rect.centery,game_map.rect.bottom):
            if game_map.mask.get_at((self.rect.left, i)):
                left_y_point = i
                break
        for i in range(self.rect.centery,game_map.rect.bottom):
            if game_map.mask.get_at((self.rect.right, i)):
                right_y_point = i
                break
        slope = (left_y_point - right_y_point) / (self.rect.left - self.rect.right)

        return -math.atan(slope) * 180 / (math.pi)

    def draw(self, angle, current_player, moving, shooting):
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
                cover_rect = pygame.Rect(0, 0, rotated_angle_line_image.get_width() // 2,
                                         rotated_angle_line_image.get_height())
            else:
                cover_rect = pygame.Rect(rotated_angle_line_image.get_width() // 2, 0,
                                         rotated_angle_line_image.get_width() // 2,
                                         rotated_angle_line_image.get_height())
            pygame.draw.rect(rotated_angle_line_image, (255, 255, 255, 0), cover_rect)
            screen.blit(rotated_angle_line_image, angle_line_rect.topleft)
        screen.blit(rotated_image, new_rect.topleft)


    def draw_health_bar(self, screen):
        bar_width = 50  # Chiều rộng của thanh máu
        bar_height = 6  # Chiều cao của thanh máu
        bar_x = self.rect.centerx - bar_width // 2  # Tâm thanh máu dưới chân nhân vật
        bar_y = self.rect.bottom + 5  # Cách phần đáy nhân vật 5px

        # Tính toán chiều dài thanh máu dựa trên HP hiện tại
        current_health_width = int(bar_width * (self.HP / self.max_HP))

        # Vẽ thanh nền (màu xám)
        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))

        # Vẽ thanh máu (màu xanh lá)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_health_width, bar_height))

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
        if not self.jumping and not self.mask.overlap(
                game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y)):
            down = 0
            for i in range(0, int(self.velocity)):
                down = i
                if self.mask.overlap(game_map.mask,
                                     (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y - i)):
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
            if self.velocity >= JUMP_HEIGHT or self.mask.overlap(
                    game_map.mask, (game_map.rect.x - self.rect.x, game_map.rect.y - self.rect.y + self.velocity)):
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
            overlap_pos = self.mask.overlap(game_map.mask, (
            game_map.rect.x - self.rect.x - i * sign, game_map.rect.y - self.rect.y))
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
        theta, accel, t = angle * math.pi / 180 , BULLET_ACCEL, bullet.time
        scale = POWER_SCALE
        V = scale * self.power
        x0, y0 = self.rect.center
        x = x0 + direction * V * math.cos(theta) * t
        y = y0 + (-V * math.sin(theta) * t + accel * t ** 2 / 2)
        bullet.update(x, y)


    #check for collision with bullet
    def check_collision_with_bullet(self, bullet):
        # Kiểm tra nếu có sự chồng lấn giữa mask của đạn và mask của nhân vật
        if self.mask.overlap(bullet.mask, (bullet.rect.x - self.rect.x, bullet.rect.y - self.rect.y)):
            return True
        return False

    # vẽ thanh power
    def draw_power_bar(self):
        power_bar_width = 300  # chiều rộng của thanh power
        power_bar_height = 30  # chiều cao của thanh power
        power_ratio = self.power / 100

        # vị trí của thanh power
        power_bar_x = (WINDOW_WIDTH - power_bar_width) // 2
        power_bar_y = WINDOW_HEIGHT - 100

        # vẽ thanh nền màu xám
        pygame.draw.rect(screen, (169, 169, 169), (power_bar_x, power_bar_y, power_bar_width, power_bar_height))
        # vẽ thanh power màu vàng
        pygame.draw.rect(screen, (255, 255, 0),
                         (power_bar_x, power_bar_y, power_bar_width * power_ratio, power_bar_height))

        # Vẽ các vạch số từ 0 đến 100
        font = pygame.font.Font(None, 24)
        for i in range(0, 101, 10):  # từ 0 đến 100, với bước là 10
            x_position = power_bar_x + (i / 100) * power_bar_width
            text_surface = font.render(str(i), True, BLACK)
            text_rect = text_surface.get_rect(center=(x_position, power_bar_y + power_bar_height + 10))  # vị trí chỉ số
            screen.blit(text_surface, text_rect.topleft)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, shooter):
        super().__init__()
        self.image = pygame.transform.scale(image, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0
        self.hit_target = False
        self.shooter = shooter
        self.count = 0

    def update(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect.topleft)



class Text:
    def __init__(self, text, x, y, font=None, size=36, color=BLACK):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.text, self.rect)

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

def start_menu():
    screen.fill(WHITE)
    start_text = Text("Welcome to ANGLE", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100, size=40, color=GREEN, font="freesansbold.ttf")
    game_description_text = Text("Angle your shot to hit the enemy", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50, size=20, color=BLACK, font="freesansbold.ttf")
    tutorial_text = Text("Use arrow keys to move and space to shoot", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20, size=20, color=RED, font="freesansbold.ttf")

    start_button = Button("Start", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    start_over_btn = Button("Start Over", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 40, 200, 50)
    quit_button = Button("Quit", WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 110, 200, 50)

    while True:
        screen.fill(WHITE)
        start_text.draw()
        game_description_text.draw()
        tutorial_text.draw()
        start_button.draw()
        quit_button.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if start_button.is_clicked(event):
                return
            if quit_button.is_clicked(event):
                pygame.quit()
                quit()


def end_game_screen(winner):
    global game_over

    # Vẽ thông báo người thắng
    font = pygame.font.SysFont(None, 60)
    text = font.render(f"{winner} Wins!", True, (205,133,63))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

    # Tạo các nút
    start_over_button = Button("Start Over", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20, 200, 50,
                               font_color=BLACK)

    # Hiển thị màn hình kết thúc cho đến khi nhấn nút
    while True:
        screen.fill(WHITE)
        screen.blit(text, text_rect)
        start_over_button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif start_over_button.is_clicked(event):
                game_over = False
                return "restart"

def main_game_loop():
    player1 = Character(character_display_image, character_real_image, 400, 0)
    player2 = Character(character_display_image, character_real_image, 600, 0)

    game_map = GameMap(0, 0, game_map_image)

    characters = pygame.sprite.Group()
    characters.add(player1)
    characters.add(player2)

    current_player = player2

    move_left = False
    move_right = False
    move_up = False
    move_down = False
    angle_adjust = 1
    shooting = False
    charging = False
    charging_status = "increasing"
    game_over = False
    time_limit = 15  # mỗi người có 15 giây để chơi
    start_ticks = pygame.time.get_ticks()
    time_left_text = Text("Time Left: 15", 100, 50, size=30, color=BLACK)  # hiển thị thời gian

    def switch_turn():
        nonlocal current_player
        current_player = player1 if current_player == player2 else player2
        current_player.speed = DEFAULT_CHARACTER_SPEED
    def handle_movement(current_character):
        nonlocal move_left, move_right, move_up, move_down, angle_adjust, shooting, charging, charging_status
        if charging:
            if charging_status == "increasing":
                current_character.power += 1
                if current_character.power >= 100:
                    charging_status = "decreasing"
            else:
                current_character.power -= 1
                if current_character.power <= 0:
                    charging_status = "increasing"
        if move_up or move_down:
            current_character.shoot_angle += angle_adjust
            if current_character.shoot_angle >= MAX_SHOOT_ANGLE_DISPLAY:
                current_character.shoot_angle = MAX_SHOOT_ANGLE_DISPLAY
            if current_character.shoot_angle <= MIN_SHOOT_ANGLE_DISPLAY:
                current_character.shoot_angle = MIN_SHOOT_ANGLE_DISPLAY
        if move_left or move_right:
            if (current_character.speed > 0 and move_left) or (current_character.speed < 0 and move_right):
                current_character.speed *= -1
            if (current_character.check_collision_with_game_map_y(game_map)):
                current_character.move(game_map)

    while not game_over:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Tính toán thời gian đã trôi
        time_left = time_limit - seconds  # Tính thời gian còn lại
        time_left_text.text = time_left_text.font.render(f"Time Left: {int(time_left)}", True,
                                                         BLACK)  # Cập nhật thời gian
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not current_player.jumping and current_player.on_ground:
                        current_player.jumping = True
                        current_player.on_ground = False
                if event.key == pygame.K_UP:
                    angle_adjust = 1
                    move_up = True
                if event.key == pygame.K_DOWN:
                    angle_adjust = -1
                    move_down = True
                if event.key == pygame.K_LEFT:
                    move_left = True
                    current_player.face_right = False
                if event.key == pygame.K_RIGHT:
                    move_right = True
                    current_player.face_right = True
                if event.key == pygame.K_LCTRL:
                    charging = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_LCTRL:
                    if not shooting:
                        charging = False
                        shooting = True
                        bullet = Bullet(current_player.rect.centerx, current_player.rect.centery, bullet_image,current_player)

        screen.fill(WHITE)
        game_map.draw()

        if time_left <= 0:  # nếu đã thời gian chơi
            move_down = move_up = move_left = move_right = current_player.jumping = False
            start_ticks = pygame.time.get_ticks()  # đặt lại thời gian bắt đầu lượt
            time_left = time_limit  # đặt lại thời gian còn lại
            switch_turn()
        elif shooting:
            shooted = False
            move_down = move_up = move_left = move_right = current_player.jumping = False
            current_player.shoot(bullet, game_map)
            bullet.draw()
            bullet.time += BULLET_SPEED
            # Kiểm tra va chạm với địa hình hoặc ra khỏi màn hình
            if bullet.rect.right < 0 or bullet.rect.left > GAME_MAP_WIDTH or bullet.rect.top > WINDOW_HEIGHT or bullet.mask.overlap(
                    game_map.mask, (game_map.rect.x - bullet.rect.x, game_map.rect.y - bullet.rect.y)):
                if pygame.sprite.collide_mask(bullet, game_map):
                    game_map.update_from_explosion(bullet.rect.center)
                start_ticks = pygame.time.get_ticks()  # đặt lại thời gian bắt đầu lượt
                time_left = time_limit  # đặt lại thời gian còn lại
                bullet.kill()
                shooting = False
                current_player.power = 0
                if not shooted :
                    switch_turn()
                    shooted = True
                print("Trung dia hinh")

            # Kiểm tra va chạm với nhân vật
            for character in characters:
                if character != current_player and character.check_collision_with_bullet(bullet) and not bullet.hit_target:
                    bullet.hit_target = True
                    character.HP -= BULLET_DAMAGE
                    if character.HP <= 0:
                        winner = "Player 1" if character == player2 else "Player 2"
                        end_game_screen(winner)
                        game_over = True
                        break
                    # Gây nổ địa hình tại vị trí của nhân vật khi bị trúng đạn
                    game_map.update_from_explosion(character.rect.center)
                    bullet.kill()
                    shooting = False
                    current_player.power = 0
                    print("Trung nguoi")
                    if not shooted :
                        switch_turn()
                        shooted = True
                    break
            shooted = False
        characters.update(game_map)
        handle_movement(current_player)
        # Vẽ nhân vật
        for character in characters:
            character_angle = character.angle(game_map)
            character.draw(character_angle, current_player, (move_left or move_right), shooting)
            character.draw_health_bar(screen)
            if character == current_player:
                character.draw_power_bar()  # vẽ thanh power
        time_left_text.draw()
        pygame.display.update()
        clock.tick(60)

start_menu()
main_game_loop()