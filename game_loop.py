import pygame
from settings import *
from character import Character
from game_map import GameMap
from bullet import Bullet

def main_game_loop(screen, clock):
    character_display_image = pygame.image.load("./image/clipart1580513.png").convert_alpha()
    character_real_image = pygame.image.load("./image/clipart1580513 (1).png").convert_alpha()
    game_map_image = pygame.image.load("./image/Reloaded_Jurassic_small.png").convert_alpha()
    character_angle_line_image = pygame.image.load("./image/Dotted-Line-PNG-Pic.png").convert_alpha()
    character_angle_line_image = pygame.transform.scale(character_angle_line_image, (89, 10))
    bullet_image = pygame.image.load("./image/CannonBullet1.png").convert_alpha()

    player1 = Character(character_display_image, character_real_image,screen ,400, 0)
    player2 = Character(character_display_image, character_real_image,screen, 600, 0)

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

    while True:
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
                        bullet = Bullet(current_player.rect.centerx, current_player.rect.centery, bullet_image)

        screen.fill(WHITE)
        if shooting:
            move_down = move_up = move_left = move_right = current_player.jumping = False
            current_player.shoot(bullet, game_map)
            bullet.draw(screen)
            bullet.time += BULLET_SPEED
            if bullet.rect.right < 0 or bullet.rect.left > GAME_MAP_WIDTH or bullet.rect.top > WINDOW_HEIGHT or bullet.mask.overlap(game_map.mask, (game_map.rect.x - bullet.rect.x, game_map.rect.y - bullet.rect.y)):
                if pygame.sprite.collide_mask(bullet, game_map):
                    game_map.update_from_explosion(bullet.rect.center)
                    bullet.kill()
                bullet.kill()
                shooting = False
                current_player.power = 0
                switch_turn()

        characters.update(game_map)
        handle_movement(current_player)
        for character in characters:
            character_angle = character.angle(game_map)
            character.draw(screen, character_angle, current_player, (move_left or move_right), shooting, character_angle_line_image)

        game_map.draw(screen)
        pygame.display.update()
        clock.tick(60)