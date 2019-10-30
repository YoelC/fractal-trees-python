import pygame
from random import randint
from multifile import rotate_center


class Blossom:
    def __init__(self, parent):
        self.x = parent.x
        self.y = parent.y

        self.x_vel = 0
        self.y_vel = 0

        self.width, self.height = parent.distance/10, parent.distance/10
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0))

        self.angle = parent.angle

        self.parent = parent
        self.attached = True
        self.distance_unnatached = 0

        self.lifetime = 100 + randint(1, 300)

    def move(self):
        if self.lifetime < 0:
            self.attached = False
            self.y_vel = -4

        self.x += self.x_vel
        self.y -= self.y_vel

        if self.attached:
            self.x = self.parent.x
            self.y = self.parent.y

        self.lifetime -= 1 if self.attached else 0

    def draw(self, surface):
        to_draw, new_rect = rotate_center(self.surface, self.angle, (self.x - self.width/2, self.y - self.height/2))
        surface.blit(to_draw, new_rect)
