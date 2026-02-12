import pygame
from UIElement import UIElement

class BattleButton(UIElement):
    def __init__(self, text, x, y, width, height, base_color, hover_color, font):
        super().__init__(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.font = font
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.base_color
        pygame.draw.rect(surface, (50, 50, 50), self.rect.inflate(4, 4), border_radius=5)
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        txt = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(txt, txt.get_rect(center=self.rect.center))