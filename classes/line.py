import pygame
from math import cos, sin, radians


class Line:
    def __init__(self, pos=None, angle=None, ticks=None, vel=None, number=None, division_angle=None, parent=None, type_=None, division_ratio=1.2, divide_angles=True, divide_distance=True):

        self.division_angle = division_angle

        self.angle = angle
        self.distance = 0

        self.angle_vel = 0

        self.ticks = ticks
        self.max_ticks = ticks
        self.vel = vel
        self.number = number
        self.type_ = type_

        if parent is not None and type_ is not None:
            self.division_angle = parent.division_angle/division_ratio if divide_angles else parent.division_angle
            self.angle = parent.angle + self.division_angle if type_ == 0 else parent.angle - self.division_angle
            self.ticks = parent.max_ticks/division_ratio if divide_distance else parent.max_ticks
            self.max_ticks = parent.max_ticks/division_ratio if divide_distance else parent.max_ticks
            self.vel = parent.vel
            self.number = parent.number - 1

            self.origin_x = parent.x
            self.origin_y = parent.y
        else:
            self.origin_x, self.origin_y = pos
            self.x, self.y = pos

        self.parent = parent
        self.grown = False

    def move(self):
        if self.type_ is None:
            self.angle += self.angle_vel
        else:
            self.division_angle += self.angle_vel
        if self.parent is not None:
            self.origin_x = self.parent.x
            self.origin_y = self.parent.y
            self.angle = self.parent.angle + self.division_angle if self.type_ == 0 else self.parent.angle - self.division_angle

        if self.ticks > 0:
            self.distance += self.vel

            self.x = self.origin_x + self.distance * cos(radians(self.angle))
            self.y = self.origin_y - self.distance * sin(radians(self.angle))

            self.ticks -= 1
        else:
            self.x = self.origin_x + self.distance * cos(radians(self.angle))
            self.y = self.origin_y - self.distance * sin(radians(self.angle))

            self.grown = True

    def draw(self, surface, color=(200, 200, 200)):
        pygame.draw.line(surface, color, (self.origin_x, self.origin_y), (self.x, self.y), 2*self.number)
