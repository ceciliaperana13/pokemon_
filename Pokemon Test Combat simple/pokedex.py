import pygame
from settings import *
from button import Button
from savemanager import SaveManager
import os 

class PokedexView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 18, bold=True) # Taille réduite pour les noms
        self.btn_back = Button("RETOUR", WIDTH // 2 - 100, HEIGHT - 70, 200, 45, (100, 100, 100))
        self.scroll_y = 0  # Position de départ
        self.scroll_speed = 30 # Pixels déplacés par coup de molette
        # Cache pour les images et les noms
        self.images_cache = {}
        self.names_cache = {}
        
        if os.path.exists("asset/sprites/"):
            all_files = os.listdir("asset/sprites/")
            # Dans le __init__ de PokedexView
        for f in all_files:
            if " - " in f:
                # On récupère l'ID et on enlève les zéros au début (ex: "009" -> "9")
                raw_id = f.split(" - ")[0].strip()
                clean_id = str(int(raw_id)) 

                img = pygame.image.load(os.path.join("asset/sprites/", f)).convert_alpha()
                self.images_cache[clean_id] = pygame.transform.scale(img, (70, 70))
                self.names_cache[clean_id] = f.replace(".png", "").split(" - ")[1]

    # CETTE FONCTION DOIT ÊTRE ALIGNÉE AVEC LE def __init__
    def display(self):
        self.screen.fill((20, 30, 50))
        data = SaveManager.get_pokedex_data()
        # On transforme tout en "ID propre" (ex: "004" devient "4")
        pokedex_decouvert = data.get("discovered", [])
        for x in data.get("pokedex", []):
            try:
                pokedex_decouvert.append(str(int(str(x).strip())))
            except:
                continue

        # --- Affichage de la grille ---
        cols = 4  
        margin_x, margin_y = 180, 130 

        for i in range(1, 152):
            row = (i - 1) // cols
            col = (i - 1) % cols
            x = 80 + (col * margin_x)
            y = 80 + (row * margin_y) + self.scroll_y

            if -100 < y < HEIGHT:
                id_str = str(i) # "1", "2", "3"...
                
                if id_str in pokedex_decouvert:
                    # On cherche dans le cache
                    if id_str in self.images_cache:
                        self.screen.blit(self.images_cache[id_str], (x, y))
                        name = self.names_cache.get(id_str, "Inconnu")
                        name_surf = self.font.render(name, True, (0, 255, 100))
                        self.screen.blit(name_surf, (x, y + 75))
                    else:
                        # Si l'ID est connu mais l'image manque
                        error_surf = self.font.render(f"N°{id_str} (Image !)", True, (255, 100, 100))
                        self.screen.blit(error_surf, (x, y + 30))
                else:
                    mystery_surf = self.font.render(f"{i} ???", True, (80, 80, 80))
                    self.screen.blit(mystery_surf, (x, y + 30))

        # Interface fixe (Header & Button)
        pygame.draw.rect(self.screen, (20, 30, 50), (0, 0, WIDTH, 70))
        title_surf = self.font.render(f"POKEDEX : {len(pokedex_decouvert)} / 151", True, (255, 255, 255))
        self.screen.blit(title_surf, (WIDTH // 2 - 120, 20))
        self.btn_back.draw(self.screen)

    def handle_input(self, events, game_instance):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Gestion du Scroll avec la molette
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # Molette vers le haut
                    self.scroll_y = min(0, self.scroll_y + self.scroll_speed)
                if event.button == 5: # Molette vers le bas
                    # On limite le scroll pour ne pas aller dans le vide (ex: -1500)
                    self.scroll_y -= self.scroll_speed 

            if self.btn_back.is_clicked(event):
                game_instance.state = "MENU"