import pygame
from multifile import FONT


class Button:
    def __init__(self, pos, text, size=40, outline_width=2):
        self.x, self.y, self.width, self.height = pos
        self.text = text
        self.size = size

        self.clicked = False

        self.temp_x, self.temp_y = 0, 0

        self.outline_width = outline_width

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move_frame(self, delta):
        self.temp_x, self.temp_y = delta

    def check_clicked(self):
        mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        rect = self.get_rect()
        rect = (rect[0] + self.temp_x, rect[1] + self.temp_y, rect[2], rect[3])
        if mouse_rect.colliderect(rect):
            return True
        return False

    def draw(self, surface):
        x, y = self.x, self.y
        x += self.temp_x
        y += self.temp_y
        pygame.draw.rect(surface, (0, 0, 0), (x, y, self.width, self.height))
        pygame.draw.rect(surface, (255, 255, 255), (x, y, self.width, self.height), self.outline_width)
        font_surface, font_pos = FONT.render(self.text, (255, 255, 255), size=self.size)
        surface.blit(font_surface, (x + self.width/2 - font_pos.width/2, y + self.height/2 - font_pos.height/2))
        self.temp_x, self.temp_y = 0, 0
