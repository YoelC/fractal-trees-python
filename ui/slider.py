import pygame
from multifile import FONT


class Slider:
    def __init__(self, pos, text, attached_value):
        self.x, self.y, self.width, self.height = pos
        self.text = text
        self.slider_percentage = 100
        self.holding_click = False
        self.x_offset = self.width * (self.slider_percentage/100)
        self.attached_value = attached_value
        self.percentage_multiplier = 1

        self.round_value = 2

        self.temp_x, self.temp_y = 0, 0
        self.moved_frame = False

    def set_round(self, round_value):
        self.round_value = round_value

    def move_frame(self, delta):
        self.temp_x, self.temp_y = delta

    def set_percentage(self, percentage):
        self.slider_percentage = percentage

    def move(self, mouse_x_pos):
        if self.holding_click:
            self.slider_percentage = ((mouse_x_pos - self.x) / self.width) * 100
            if self.slider_percentage < 0:
                self.slider_percentage = 0
            if self.slider_percentage > 100:
                self.slider_percentage = 100

    def get_value(self):
        if self.round_value == 0:
            return int(round(self.attached_value * (self.slider_percentage / 100), self.round_value))
        return round(self.attached_value * (self.slider_percentage / 100), self.round_value)

    def get_rect(self):
        return pygame.Rect(self.x + self.x_offset - 20 - 2, self.y + self.height/2 - 20 - 2, 40 + 4, 40 + 4)

    def check_clicked(self, clicked, holding_click):
        if clicked:
            mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
            if self.get_rect().colliderect(mouse_rect):
                self.holding_click = True

        if (holding_click or clicked) and self.holding_click:
            self.holding_click = True
        else:
            self.holding_click = False

    def draw(self, surface):
        x, y = self.x, self.y
        x += self.temp_x
        y += self.temp_y
        self.x_offset = self.width * (self.slider_percentage/100)
        pygame.draw.line(surface, (255, 255, 255),
                         (x, y + self.height/2),
                         (x + self.width, y + self.height/2), 4)

        pygame.draw.rect(surface, (0, 0, 0), (x + self.x_offset - 20, y + self.height/2 - 20, 40, 40))
        pygame.draw.rect(surface, (255, 255, 255), (x + self.x_offset - 20, y + self.height/2 - 20, 40, 40), 4)
        font_surface, font_pos = FONT.render(f'{self.text}: {self.get_value()}', (255, 255, 255), size=40)
        surface.blit(font_surface, (x, y - 25))
        self.temp_x, self.temp_y = 0, 0
