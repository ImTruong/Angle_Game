import pygame.mixer
import pygame.mixer_music

pygame.mixer.init()


move_sfx = pygame.mixer.Sound("sound/move.wav")
move_sfx.set_volume(1)

jump_sfx = pygame.mixer.Sound("sound/jump.wav")
jump_sfx.set_volume(1)

explosion_sfx = pygame.mixer.Sound("sound/Explosion.wav")
explosion_sfx.set_volume(1)

game_over_sfx = pygame.mixer.Sound("sound/GameOver.wav")
game_over_sfx.set_volume(1)

shoot_sfx = pygame.mixer.Sound("sound/Shot.wav")
shoot_sfx.set_volume(1)

pygame.mixer_music.load("sound/BackGound.mp3")

