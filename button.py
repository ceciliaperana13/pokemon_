import pygame
from settings import DARK_GRAY, BLACK

class Button:
    def __init__(self, text, x, y, w, h, base_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = base_color
        self.font = pygame.font.Font("asset/font/Pocket-Monk.otf", 30)
        # On garde une variable enabled par sécurité, mais toujours True
        self.enabled = True 

    def draw(self, screen):
        # 1. Gestion des couleurs et de l'effet de survol
        bg_color = (10, 15, 30)
        text_color = (255, 255, 255)
        
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            border_color = (0, 200, 255) # Bleu néon au survol
            draw_rect = self.rect.inflate(4, 4) # Effet zoom
        else:
            border_color = (255, 255, 255) # Blanc par défaut
            draw_rect = self.rect

        # 2. Dessin du fond (Arrondi)
        pygame.draw.rect(screen, bg_color, draw_rect, border_radius=15)

        # 3. Dessin de la bordure
        pygame.draw.rect(screen, border_color, draw_rect, width=3, border_radius=15)

        # 4. Affichage du texte
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # Vérifie si l'utilisateur clique sur le bouton
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False