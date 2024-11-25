from random import *
from character import *
from game_map import *
from bullet import *
from particle import *
from text import *
from constants import *
from camera import *

particle_groups = pygame.sprite.Group()

def main_game_loop():

    game_map = SeaMap(0, 0)
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
    bullet_image = pygame.transform.scale(pygame.image.load("image/CannonBullet.png").convert_alpha(), (BULLET_SIZE, BULLET_SIZE))
    player1 = Character(character_display_image, character_real_image, 1500, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    player2 = Character(character_display_image, character_real_image, 400, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)



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
    time_limit = 20
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

    delay_time = None

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
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_LCTRL and current_player.on_ground and shooting == False:
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
                if event.key == pygame.K_LCTRL and current_player.on_ground:
                    if not shooting:
                        charging = False
                        shooting = True
                        bullet = Bullet(bullet_image, current_player)

        if not shooting and delay_time is None:
            camera.update(current_player)

        game_map.draw(camera)
        if time_left <= 0 and not shooting and not charging:
            start_ticks = pygame.time.get_ticks()
            switch_turn()
        elif charging or delay_time is not None:
            move_down = move_up = move_left = move_right = current_player.jumping = False
        elif shooting:
            charging = move_down = move_up = move_left = move_right = current_player.jumping = False
            current_player.shoot(bullet, game_map)
            camera.update(bullet)
            bullet.draw(camera)
            bullet.time += BULLET_SPEED
            if bullet.rect.right < 0 or bullet.rect.left > GAME_MAP_WIDTH or bullet.rect.top > WINDOW_HEIGHT or bullet.mask.overlap(game_map.mask, (game_map.rect.x - bullet.rect.x, game_map.rect.y - bullet.rect.y)):
                if pygame.sprite.collide_mask(bullet, game_map):
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
            if character == current_player:
                character.draw_power_bar()

        if (not shooting and not charging):
            time_left_text.draw()
        pygame.display.update()
        clock.tick(60)