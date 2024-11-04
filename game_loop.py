import pygame

from main import screen, clock
from menu import end_game_screen
from settings import *
from random import uniform
from character import Character
from game_map import GameMap
from bullet import Bullet
from particle import Particle
from ui import Text

character_display_image = pygame.image.load("./image/clipart1580513.png").convert_alpha()
character_real_image = pygame.image.load("./image/clipart1580513 (1).png").convert_alpha()
game_map_image = pygame.image.load("./image/Reloaded_Jurassic_small.png").convert_alpha()
character_angle_line_image = pygame.image.load("./image/Dotted-Line-PNG-Pic.png").convert_alpha()
character_angle_line_image = pygame.transform.scale(character_angle_line_image, (89, 10))
bullet_image = pygame.image.load("./image/CannonBullet1.png").convert_alpha()

particle_groups=pygame.sprite.Group()
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
    def spawm_particle(pos):
        for _ in range(20):
            direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
            direction = direction.normalize()
            speed = uniform(0.25,0.75)
            Particle(particle_groups, pos, direction, speed, 2)
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
                    spawm_particle(bullet.rect.center)
                    game_map.update_from_explosion(bullet.rect.center)
                    bullet.kill()
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
        particle_groups.update()
        particle_groups.draw(screen)
        characters.update(game_map)
        handle_movement(current_player)
        # Vẽ nhân vật
        for character in characters:
            character_angle = character.angle(game_map)
            character.draw(screen, character_angle, current_player, (move_left or move_right), shooting,character_angle_line_image, charging)
            character.draw_health_bar(screen)
            if character == current_player:
                character.draw_power_bar()  # vẽ thanh power
        time_left_text.draw()
        pygame.display.update()
        clock.tick(60)