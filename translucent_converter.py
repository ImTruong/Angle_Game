import pygame

pygame.init()

image = pygame.image.load('input.png').convert_alpha()

width, height = image.get_size()
for x in range(width):
    for y in range(height):
        r, g, b, a = image.get_at((x, y))

        if (r, g, b) == (0, 0, 0):
            image.set_at((x, y), (r, g, b, 0))

pygame.image.save(image, 'output.png')