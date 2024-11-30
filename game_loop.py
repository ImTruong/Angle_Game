import random
from menu import *
import pygame.mouse

from bullet import *
from random import uniform
import pygame.mixer
from sound import *
from character import Character
from particle import Particle
from text import Text
from camera import *

particle_groups = pygame.sprite.Group()

def main_game_loop(game_map,number_of_player):

    camera = Camera(game_map.game_map_width, game_map.game_map_height)

    GAME_MAP_WIDTH = game_map.game_map_width
    GAME_MAP_HEIGHT = game_map.game_map_height
    CHARACTER_WIDTH = game_map.character_width
    CHARACTER_HEIGHT = game_map.character_height

    character_display_image = pygame.transform.scale(pygame.image.load("image/character_display_image.png").convert_alpha(), (CHARACTER_WIDTH, CHARACTER_HEIGHT))
    character_real_image = pygame.transform.scale(pygame.image.load("image/character_block.png").convert_alpha(), (CHARACTER_WIDTH, CHARACTER_HEIGHT))
    character_angle_line_image = pygame.image.load("image/Dotted_Line_Angle.png").convert_alpha()
    character_angle_line_image = pygame.transform.scale(character_angle_line_image, (89, 10))
    character_limit_angle_line_image = pygame.image.load("image/limit_angle_line.png").convert_alpha()
    character_limit_angle_line_image = pygame.transform.scale(character_limit_angle_line_image, (89, 10))
    freeze_image = pygame.transform.scale(pygame.image.load("image/freeze.png").convert_alpha(), (CHARACTER_WIDTH*2, CHARACTER_HEIGHT*2))

    characters = pygame.sprite.Group()
    list_of_character = []

    for i in range(number_of_player):
        player = Character(character_display_image, character_real_image, 0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        player.rect.x, player.rect.y = game_map.spawn_rand_point(player)
        characters.add(player)
        list_of_character.append(player)

    current_player = random.choice(list(characters))

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
    frozen_bullet = False
    heal_bullet = False
    continous_bullet = 0
    start_ticks = pygame.time.get_ticks()
    time_left_text = Text(f"Time Left: {time_limit}", 100, 50, size=30, color=BLACK)
    selected_skill = None
    skill_active = False

    def switch_turn():
        nonlocal current_player
        current_index = list_of_character.index(current_player)
        next_index = (current_index + 1) % len(list_of_character)
        current_player = list_of_character[next_index]
        if current_player.HP == 0:
            switch_turn()
        current_player.speed = DEFAULT_CHARACTER_SPEED
        if current_player.freeze > 0:
            current_player.freeze -= 1
            if not current_player.freeze == 0:
                switch_turn()



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

    def check_team_status():
        odd_team_dead = all(player.HP == 0 for i, player in enumerate(list_of_character) if i % 2 == 0)
        even_team_dead = all(player.HP == 0 for i, player in enumerate(list_of_character) if i % 2 != 0)
        if odd_team_dead:
            return "Even team wins!"
        if even_team_dead:
            return "Odd team wins!"
        return None

    while not game_over:
        if check_team_status() is not None and delay_time is None:
            game_over = True
            end_menu(check_team_status())
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = time_limit - seconds
        time_left_text.text = time_left_text.font.render(f"Time Left: {int(time_left)}", True, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_menu()
                if event.key == pygame.K_SPACE:
                    if not (charging or shooting):
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
                    if not (move_up or move_down or charging or shooting):
                        move_sfx.play(-1)
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    if not (move_up or move_down or charging or shooting):
                        move_sfx.play(-1)
                    move_right = True
                if event.key == pygame.K_LCTRL and current_player.on_ground and not shooting:
                    move_sfx.stop()
                    jump_sfx.stop()
                    charging = True
                if event.key == pygame.K_LALT:
                    mouse_view_active = not mouse_view_active

                if event.key == pygame.K_1 and not skill_active and current_player.teleport == True:
                    selected_skill = "Teleport" if selected_skill != "Teleport" else None
                    teleport = True if teleport is False else False
                    frozen_bullet = False
                    heal_bullet = False
                    skill_active = False

                if event.key == pygame.K_2 and not skill_active and current_player.frozen_bullet == True:
                    selected_skill = "Frozen Bullet" if selected_skill != "Frozen Bullet" else None
                    teleport = False
                    frozen_bullet = True if frozen_bullet is False else False
                    heal_bullet = False
                    skill_active = False

                if event.key == pygame.K_3 and not skill_active and current_player.heal_bullet == True:
                    selected_skill = "Heal Bullet" if selected_skill != "Heal Bullet" else None
                    teleport = False
                    frozen_bullet = False
                    heal_bullet = True if heal_bullet is False else False
                    skill_active = False

                if event.key == pygame.K_4 and not skill_active and current_player.continuous_bullet == True and current_player.on_ground:
                    selected_skill = "Continuous Bullet"
                    teleport = False
                    frozen_bullet = False
                    heal_bullet = False
                    continous_bullet = 1
                    current_player.continuous_bullet = False
                    bullet = ContinuousBullet(current_player)
                    shoot_sfx.play()
                    shooting = True
                    skill_active = True

            if event.type == pygame.KEYUP:
                move_sfx.stop()
                jump_sfx.stop()
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
                        elif frozen_bullet:
                            bullet = IceBullet(current_player)
                            frozen_bullet = False
                        elif heal_bullet:
                            bullet = HealBullet(current_player)
                            heal_bullet = False
                        elif continous_bullet != 0:
                            bullet = ContinuousBullet(current_player)
                        else :
                            bullet = NormalBullet(current_player)
                        skill_active = False

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
            if bullet.rect.right < 0 or bullet.rect.left > GAME_MAP_WIDTH or bullet.rect.top > GAME_MAP_HEIGHT or bullet.mask.overlap(game_map.mask, (game_map.rect.x - bullet.rect.x, game_map.rect.y - bullet.rect.y)) or (isinstance(bullet, ContinuousBullet) and bullet.rect.bottom < 0):
                if pygame.sprite.collide_mask(bullet, game_map):
                    explosion_sfx.play()
                    if isinstance(bullet, NormalBullet) or isinstance(bullet, ContinuousBullet):
                        spawm_particle(bullet.rect.center)
                        game_map.update_from_explosion(bullet.rect.center)
                        for character in characters:
                            if character.check_collision_with_explode_point(bullet, bullet.rect.center):
                                bullet.hit_target = True
                                if (character.freeze > 0):
                                    character.freeze = 0
                                else:
                                    character.HP -= NORMAL_BULLET_DAMAGE if isinstance(bullet, NormalBullet) else CONTINUOUS_BULLET_DAMAGE
                                    if character.HP <= 0:
                                        character.kill()

                    elif isinstance(bullet, TeleportBullet):
                        current_player.teleport = False
                        current_player.rect.center = bullet.rect.center
                        if current_player.mask.overlap(game_map.mask, (
                        game_map.rect.x - current_player.rect.x, game_map.rect.y - current_player.rect.y)):
                            found_safe_position = False
                            for distance in range(1, 30):
                                for dx in range(-distance, distance + 1):
                                    for dy in range(-distance, distance + 1):
                                        if not current_player.mask.overlap(game_map.mask,
                                                                           (
                                                                           game_map.rect.x - current_player.rect.x - dx,
                                                                           game_map.rect.y - current_player.rect.y - dy)):
                                            current_player.rect.x += dx
                                            current_player.rect.y += dy
                                            found_safe_position = True
                                            break

                                    if found_safe_position:
                                        break

                                if found_safe_position:
                                    break
                    elif isinstance(bullet, IceBullet):
                        current_player.frozen_bullet = False
                        for character in characters:
                            if character.check_collision_with_explode_point(bullet, bullet.rect.center):
                                character.freeze = 3
                    elif isinstance(bullet, HealBullet):
                        current_player.heal_bullet = False
                        for character in characters:
                            if character.check_collision_with_explode_point(bullet, bullet.rect.center):
                                character.HP += 25
                                if character.HP > 100:
                                    character.HP = 100
                delay_time = pygame.time.get_ticks()
                start_ticks = pygame.time.get_ticks()
                bullet.kill()
                shooting = False
                current_player.power = 0
                if  continous_bullet > 0 and continous_bullet <= 2:
                    continous_bullet += 1
                    shooting = True
                    bullet = ContinuousBullet(current_player)
                    if continous_bullet > 2:
                        continous_bullet = 0
                else:
                    skill_active = False
                    selected_skill = None
                    switch_turn()
        if delay_time is not None:
            if pygame.time.get_ticks() - delay_time >= DELAY_BETWEEN:
                delay_time = None

        particle_groups.update()
        for particle in particle_groups:
            particle.draw(screen, camera)
        characters.update(game_map)
        handle_movement(current_player)

        for character in characters:
            if character.rect.top > GAME_MAP_HEIGHT:
                character.HP = 0
                character.kill()
            character_angle = character.angle(game_map)
            character.draw(screen, camera, character_angle, current_player, (move_left or move_right), shooting, character_angle_line_image, character_limit_angle_line_image, charging, delay_time, freeze_image)
            character.draw_health_bar(camera)
            character.draw_turn_marker(f"P{list_of_character.index(character) + 1}", character == current_player,camera)
            if character == current_player:
                character.draw_power_bar()
                character.draw_skills(screen,selected_skill)

        if (not shooting and not charging):
            time_left_text.draw()
        pygame.display.update()
        clock.tick(60)