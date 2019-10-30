import pygame
from multifile import FONT


class CheckBox:
    width, height = 40, 40

    def __init__(self, pos, text):
        self.x, self.y = pos
        self.text = text

        self.checked = False

        _, self.font_pos = FONT.render(f'{self.text}', (255, 255, 255), size=40)

        self.temp_x, self.temp_y = 0, 0

    def move_frame(self, delta):
        self.temp_x, self.temp_y = delta

    def get_rect(self):
        return pygame.Rect(self.x + self.temp_x, self.y + self.temp_y, self.width + self.width * 2 + self.font_pos.width, self.height)

    def is_checked(self):
        return self.checked

    def check_clicked(self):
        mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if mouse_rect.colliderect(self.get_rect()):
            return True
        return False

    def draw(self, surface):
        x, y = self.x, self.y
        x += self.temp_x
        y += self.temp_y
        if self.checked:
            gap = 16
            pygame.draw.rect(surface, (255, 255, 255), (x + gap/2, y + gap/2, self.width - gap, self.height - gap))

        pygame.draw.rect(surface, (255, 255, 255), (x, y, self.width, self.height),
                         4)
        font_surface, self.font_pos = FONT.render(f'{self.text}', (255, 255, 255), size=40)
        surface.blit(font_surface, (x + self.width*2, y))

        self.temp_x, self.temp_y = 0, 0
