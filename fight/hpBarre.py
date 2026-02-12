import pygame
from UIElement import UIElement

class HPBar(UIElement):
    def __init__(self, x, y, width, height, max_hp):
        super().__init__(x, y, width, height)
        self.max_hp = max_hp
        self.hp = max_hp
        self.display_hp = max_hp

    def update(self):
        if self.display_hp > self.hp: self.display_hp -= 0.5
        elif self.display_hp < self.hp: self.display_hp += 0.5

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.rect.inflate(4, 4), border_radius=3)
        ratio = max(0, self.display_hp / self.max_hp)
        color = (50, 255, 50) if ratio > 0.5 else (255, 255, 0) if ratio > 0.2 else (255, 50, 50)
        pygame.draw.rect(surface, color, (self.rect.x, self.rect.y, self.rect.width * ratio, self.rect.height), border_radius=3)