import pygame.mouse
from debugpy.common.timestamp import current

from bullet import *
from random import uniform
import pygame.mixer
from Sound import *
from character import Character
from particle import Particle
from text import Text
from camera import *

particle_groups = pygame.sprite.Group()

def main_game_loop(game_map):

    camera = Camera(game_map.game_map_width, game_map.game_map_height)

    BULLET_SIZE = game_map.bullet_size
    GAME_MAP_WIDTH = game_map.game_map_width
    GAME_MAP_HEIGHT = game_map.game_map_height
    CHARACTER_WIDTH = game_map.character_width
    CHARACTER_HEIGHT = game_map.character_height

    character_display_image = pygame.transform.scale(pygame.image.load("image/character_display_image.png").convert_alpha(), (CHARACTER_WIDTH, CHARACTER_HEIGHT))
    character_real_image = pygame.transform.scale(pygame.image.load("image/character_block.png").convert_alpha(), (CHARACTER_WIDTH, CHARACTER_HEIGHT))
    character_angle_line_image = pygame.image.load("image/Dotted_Line_Angle.png").convert_alpha()
    character_angle_line_image = pygame.transform.scale(character_angle_line_image, (89, 10))
    player1 = Character(character_display_image, character_real_image, 800, 70, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    player2 = Character(character_display_image, character_real_image, 400, 70, CHARACTER_WIDTH, CHARACTER_HEIGHT)


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
    delay_time = None
    mouse_view_active = False
    mouse_view_pos = (0, 0)
    charging_status = "increasing"
    game_over = False
    time_limit = 20
    teleport = False
    start_ticks = pygame.time.get_ticks()
    time_left_text = Text(f"Time Left: {time_limit}", 100, 50, size=30, color=BLACK)

    def switch_turn():
        nonlocal current_player
        current_player = player1 if current_player == player2 else player2
        current_player.speed = DEFAULT_CHARACTER_SPEED

    def handle_movement(current_character):
        nonlocal move_left, move_right, move_up, move_down, angle_adjust, shooting, charging, charging_status
        if charging:
            if charging_status == "increasing":
                current_character.power += 0.5
                if current_character.power >= 100:
                    charging_status = "decreasing"
            else:
                current_character.power -= 1
                if current_character.power <= 0:
                    charging_status = "increasing"
        else:
            if move_up or move_down:
                current_character.shoot_angle += angle_adjust
                if current_character.shoot_angle >= MAX_SHOOT_ANGLE_DISPLAY:
                    current_character.shoot_angle = MAX_SHOOT_ANGLE_DISPLAY
                if current_character.shoot_angle <= MIN_SHOOT_ANGLE_DISPLAY:
                    current_character.shoot_angle = MIN_SHOOT_ANGLE_DISPLAY
            if move_left or move_right:
                current_character.face_right = False if move_left else True

                if (current_character.speed > 0 and move_left) or (current_character.speed < 0 and move_right):
                    current_character.speed *= -1
                if (current_character.check_collision_with_game_map_y(game_map)):
                    current_character.move(game_map)

    def spawm_particle(pos):
        for _ in range(15):
            direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
            direction = direction.normalize()
            speed = uniform(0.25, 0.75)
            Particle(particle_groups, pos, direction, speed, 1)

    def update_mouse_camera():
        nonlocal mouse_view_pos
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] <= RANGE_MOUSE_VIEW and mouse_view_pos[0] >= MOUSE_VIEW_SPEED:
            mouse_view_pos = (mouse_view_pos[0] - MOUSE_VIEW_SPEED, mouse_view_pos[1])
        if mouse_pos[0] >= WINDOW_WIDTH - RANGE_MOUSE_VIEW and mouse_view_pos[0] <= GAME_MAP_WIDTH - MOUSE_VIEW_SPEED:
            mouse_view_pos = (mouse_view_pos[0] + MOUSE_VIEW_SPEED, mouse_view_pos[1])
        if mouse_pos[1] <= RANGE_MOUSE_VIEW and mouse_view_pos[1] >= MOUSE_VIEW_SPEED:
            mouse_view_pos = (mouse_view_pos[0], mouse_view_pos[1] - MOUSE_VIEW_SPEED)
        if mouse_pos[1] >= WINDOW_HEIGHT - RANGE_MOUSE_VIEW and mouse_view_pos[1] <= GAME_MAP_HEIGHT - MOUSE_VIEW_SPEED:
            mouse_view_pos = (mouse_view_pos[0], mouse_view_pos[1] + MOUSE_VIEW_SPEED)
        camera.update(mouse_view_pos)

    while not game_over:


        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = time_limit - seconds
        time_left_text.text = time_left_text.font.render(f"Time Left: {int(time_left)}", True, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_sfx.play()
                    move_sfx.stop()
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
                    move_sfx.play(-1)
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_sfx.play(-1)
                    move_right = True
                if event.key == pygame.K_LCTRL and current_player.on_ground and shooting == False:
                    charging = True
                if event.key == pygame.K_LALT:
                    mouse_view_active = True if not mouse_view_active else False
                if event.key == pygame.K_1 and current_player.teleport:
                    teleport = True
                    current_player.teleport = False

            if event.type == pygame.KEYUP:
                move_sfx.stop()
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_LCTRL and current_player.on_ground:
                    shoot_sfx.play()
                    if not shooting:
                        charging = False
                        shooting = True
                        if teleport:
                            bullet = TeleportBullet(current_player)
                            teleport = False
                        else:
                            bullet = NormalBullet(current_player)

        if not shooting and delay_time is None and not mouse_view_active:
            camera.update(current_player)
        elif mouse_view_active:
            update_mouse_camera()

        game_map.draw(camera)
        if time_left <= 0 and not shooting and not charging:
            start_ticks = pygame.time.get_ticks()
            switch_turn()
        elif charging or delay_time is not None:
            move_down = move_up = move_left = move_right = current_player.jumping = False
        elif shooting:
            charging = move_down = move_up = move_left = move_right = current_player.jumping = False
            current_player.shoot(bullet, game_map)
            if not mouse_view_active:
                camera.update(bullet)
            bullet.draw(camera)
            bullet.time += BULLET_SPEED
            if bullet.rect.right < 0 or bullet.rect.left > GAME_MAP_WIDTH or bullet.rect.top > GAME_MAP_HEIGHT or bullet.mask.overlap(game_map.mask, (game_map.rect.x - bullet.rect.x, game_map.rect.y - bullet.rect.y)):
                if pygame.sprite.collide_mask(bullet, game_map):
                    explosion_sfx.play()
                    if isinstance(bullet, NormalBullet):
                        spawm_particle(bullet.rect.center)
                        game_map.update_from_explosion(bullet.rect.center)
                        for character in characters:
                            if character.check_collision_with_explode_point(bullet,bullet.rect.center):
                                bullet.hit_target = True
                                character.HP -= BULLET_DAMAGE
                                if character.HP <= 0:
                                    winner = "Player 1" if character == player2 else "Player 2"
                                    game_over = True
                        bullet.kill()
                    elif isinstance(bullet, TeleportBullet):
                        current_player.rect.center = bullet.rect.center
                        if current_player.mask.overlap(game_map.mask, (game_map.rect.x - current_player.rect.x, game_map.rect.y - current_player.rect.y)):
                            current_player.rect.center = (current_player.rect.center[0], current_player.rect.center[1] - 50)
                        bullet.kill()
                delay_time = pygame.time.get_ticks()
                start_ticks = pygame.time.get_ticks()
                bullet.kill()
                shooting = False
                current_player.power = 0
                switch_turn()

        if delay_time is not None:
            if pygame.time.get_ticks() - delay_time >= 2000:
                delay_time = None

        particle_groups.update()
        for particle in particle_groups:
            particle.draw(screen, camera)
        characters.update(game_map)
        handle_movement(current_player)

        for character in characters:
            if character.rect.top > GAME_MAP_HEIGHT:
                character.HP = 0
                winner = "Player 1" if character == player2 else "Player 2"
                game_over = True
            character_angle = character.angle(game_map)
            character.draw(screen, camera, character_angle, current_player, (move_left or move_right), shooting, character_angle_line_image, charging, delay_time)
            character.draw_health_bar(camera)
            character.draw_turn_marker("P1" if character == player1 else "P2",character == current_player, camera)
            if character == current_player:
                character.draw_power_bar()

        if (not shooting and not charging):
            time_left_text.draw()
        pygame.display.update()
        clock.tick(60)