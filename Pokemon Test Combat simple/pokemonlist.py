import pygame
import os
from settings import *
from button import Button
from utilitaire import Utilitaire 

class PokemonList:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 26, bold=True)
        self.btn_back = Button("Retour", WIDTH // 2 - 100, HEIGHT - 70, 200, 45, (100, 100, 100))
        self.sprite_path = "asset/sprites/"
        # --- OPTIMISATION : On charge la liste UNE SEULE FOIS ici ---
        all_files = [f.replace('.png', '') for f in os.listdir(self.sprite_path) if f.endswith('.png')]
        self.available = sorted(all_files, key=Utilitaire.natural_sort_key)
        # Variables de scroll
        self.scroll_y = 0
        self.scroll_speed = 30
        self.content_height = 0
        
        # Cache pour les images (évite de recharger à chaque seconde)
        self.images_cache = {}

    def handle_input(self, events):
        for event in events:
            # Détection de la molette de la souris
            if event.type == pygame.MOUSEWHEEL:
                # event.y vaut 1 (haut) ou -1 (bas)
                self.scroll_y += event.y * self.scroll_speed
        
        # --- LIMITES DU SCROLL (Clamping) ---
        # On ne peut pas scroller plus haut que le premier Pokémon
        self.scroll_y = min(0, self.scroll_y)

        # On ne peut pas scroller plus bas que le dernier Pokémon
        # On calcule la limite basse : (Hauteur totale du contenu - Hauteur de l'écran)
        max_scroll = -(len(self.available) * 65 - HEIGHT + 150)
        if self.scroll_y < max_scroll:
            self.scroll_y = max_scroll

    def display(self):
        self.screen.fill((30, 30, 60))
        
        # 1. RÉCUPÉRATION ET TRI NATUREL (C'est ici que l'ordre change)
        # On liste les fichiers et on applique Utilitaire.natural_sort_key
        all_files = [f.replace('.png', '') for f in os.listdir(self.sprite_path) if f.endswith('.png')]
        available = sorted(all_files, key=Utilitaire.natural_sort_key)
        
        # 2. CALCUL DU CONTENU
        self.content_height = len(available) * 65 + 100

        # 3. AFFICHAGE
        for i, name in enumerate(self.available):
            rect_y = 80 + (i * 65) + self.scroll_y
            
            # On ne dessine que si c'est visible à l'écran (Performance)
            if -70 < rect_y < HEIGHT:
                rect = pygame.Rect(50, rect_y, WIDTH - 100, 55)
                pygame.draw.rect(self.screen, (60, 60, 90), rect, border_radius=10)
                
                # Chargement du Sprite (optionnel, si tu veux les afficher)
                if name not in self.images_cache:
                    try:
                        img = pygame.image.load(f"{self.sprite_path}{name}.png").convert_alpha()
                        self.images_cache[name] = pygame.transform.scale(img, (45, 45))
                    except:
                        self.images_cache[name] = None

                # Affichage de l'image si elle existe
                if self.images_cache[name]:
                    self.screen.blit(self.images_cache[name], (65, rect_y + 5))

                # Affichage du texte (décalé si image présente)
                display_name = name.replace('_', ' ').replace('-', ' ').title()
                txt = self.font.render(display_name, True, WHITE)
                self.screen.blit(txt, (125, rect_y + 12))

        # Bouton de retour fixe
        self.btn_back.draw(self.screen)
    # Dans pokemonlist.py, à l'intérieur de la classe PokemonList

    def get_id_at_mouse(self, mouse_pos):
            # Sécurité : Si on clique sur le bouton retour, on ne sélectionne pas de Pokémon
            if self.btn_back.rect.collidepoint(mouse_pos):
                return None

            # On utilise directement self.available qui a été créé dans le __init__
            for i, name in enumerate(self.available):
                rect_y = 80 + (i * 65) + self.scroll_y
                
                # On ne permet le clic QUE si le Pokémon est réellement visible à l'écran
                # (entre le haut de l'écran et le bouton retour en bas)
                if 0 < rect_y < HEIGHT - 100:
                    poke_rect = pygame.Rect(50, rect_y, WIDTH - 100, 55)
                    
                    if poke_rect.collidepoint(mouse_pos):
                        print(f"Pokémon choisi : {name}") # Pour vérifier dans ta console
                        return name 
                        
            return None