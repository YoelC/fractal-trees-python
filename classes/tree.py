import pygame
from classes.line import Line
from classes.blossom import Blossom
from multifile import WINDOW_WIDTH, WINDOW_HEIGHT


class Tree:
    def __init__(self, pos, angle, ticks, vel, number, division_ratio=2, division_angle=45, divide_angles=True, divide_distance=True, color1=(200, 200, 200), color2=(150, 150, 150), fruits=False):
        self.parent_line = Line(pos, angle, ticks, vel, number, division_angle)
        self.lines = []
        self.grown_lines = []
        self.blossoms = []
        self.max_number = number

        self.divide_angles = divide_angles
        self.divide_distance = divide_distance

        self.division_ratio = division_ratio

        self.grown = False

        self.window_width, self.window_height = WINDOW_WIDTH, WINDOW_HEIGHT

        self.color1, self.color2 = color1, color2

        self.fruits = fruits

    def move(self):
        for line in self.lines:
            line.move()

        self.parent_line.move()

        for line in self.grown_lines:
            line.move()

        if 2 ** self.max_number == len(self.lines):
            self.grown = True

        for blossom in self.blossoms:
            blossom.move()

    def create_new(self):
        def append_line(type__, parent):
            self.lines.append(Line(parent=parent,
                                   type_=type__,
                                   division_ratio=self.division_ratio,
                                   divide_angles=self.divide_angles,
                                   divide_distance=self.divide_distance
                                   ))

        lines_copy = self.lines.copy()
        if self.parent_line.grown and self.parent_line not in self.grown_lines and self.parent_line.number > 0:
            append_line(0, self.parent_line)
            append_line(1, self.parent_line)
            self.grown_lines.append(self.parent_line)

        for i, line in enumerate(lines_copy):
            if line.number > 0 and line.grown:
                append_line(0, line)
                append_line(1, line)

                self.grown_lines.append(line)
                self.lines.remove(line)

            if line.number == 1 and line.grown and self.fruits:
                self.blossoms.append(Blossom(parent=line))

    def move_center(self, dx, dy):
        for line in self.lines:
            line.x += dx
            line.origin_x += dx

            line.y += dy
            line.origin_y += dy

        for line in self.grown_lines:
            line.x += dx
            line.origin_x += dx

            line.y += dy
            line.origin_y += dy

        for blossom in self.blossoms:
            blossom.x += dx
            blossom.y += dy

    def draw(self, surface):
        def inside_screen_line(line, lim1, lim2, window_width, window_height):
            if line.x > window_width or line.x < lim1:
                if line.origin_x > window_width or line.origin_x < lim1:
                    return False

            if line.y > window_height or line.y < lim2:
                if line.origin_y > window_height or line.origin_y < lim2:
                    return False

            return True

        def inside_screen_blossom(blossom, lim1, lim2, window_width, window_height):
            if blossom.x + blossom.width > window_width or blossom.x < lim1:
                if blossom.y + blossom.width > window_height or blossom.y < lim2:
                    return False

            return True

        for line in self.grown_lines:
            if inside_screen_line(line, 0, 0, self.window_width, self.window_height):
                line.draw(surface, color=self.color1)

        for line in self.lines:
            if inside_screen_line(line, 0, 0, self.window_width, self.window_height):
                line.draw(surface, color=self.color2)

        self.parent_line.draw(surface)

        for blossom in self.blossoms:
            if inside_screen_blossom(blossom, 0, 0, self.window_width, self.window_height):
                blossom.draw(surface)
