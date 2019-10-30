import pygame.freetype

pygame.freetype.init()
FONT = pygame.freetype.Font('fonts/Roboto-Regular.ttf')

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 800


def rotate_center(surface, angle, pos):
    to_draw = pygame.transform.rotate(surface, angle)
    new_rect = to_draw.get_rect(center=surface.get_rect(topleft=(pos[0], pos[1])).center)
    return to_draw, new_rect
