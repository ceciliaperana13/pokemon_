import pygame
import random
import os
from settings import *
from button import Button
from savemanager import SaveManager
from battle import Battle
from settings import VideoBackground 

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font("asset/font/Pocket-Monk.otf", 62)
        
        # Background et Audio
        self.video = VideoBackground("asset/wallpaper/wallpaper.mp4", WIDTH, HEIGHT)
        self.setup_music()
        # Vérifier si une sauvegarde existe
        data = SaveManager.get_game_data()
        last_id = data.get("current_pokemon")
        # Si le pokedex est vide et qu'aucun pokemon n'est choisi, on grise
        self.can_continue = len(data.get("pokedex", [])) > 0 or data.get("current_pokemon") is not None
        color_continue = WHITE if self.can_continue else (100, 100, 100)

        # Création des boutons
        self.buttons = {
            "load": Button("Continuer", 45, 180, 300, 50, WHITE),
            "new": Button("Nouvelle Partie", 45, 245, 300, 50, WHITE),
            "list": Button("Liste de Pokémon", 45, 310, 300, 50, WHITE),
            "options": Button("Options", 45, 375, 300, 50, WHITE),
            "pokedex": Button("Pokédex", 45, 440, 300, 50, WHITE)
        }
        # 2. ICI : On vérifie la sauvegarde pour griser le bouton "load"
        if not SaveManager.load_exists():
            self.buttons["load"].enabled = False

    def setup_music(self):
        try:
            pygame.mixer.music.load("asset/audio/mainsong.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            print("Erreur : Fichier audio introuvable.")

    def update_cursor(self):
        # Change le curseur en main si on survole un bouton
        mouse_pos = pygame.mouse.get_pos()
        on_button = any(btn.rect.collidepoint(mouse_pos) for btn in self.buttons.values())
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if on_button else pygame.SYSTEM_CURSOR_ARROW)

    def draw(self):
        # 1. Dessin de la vidéo
        frame = self.video.get_next_frame()
        if frame:
            self.screen.blit(frame, (0, 0))
        else:
            self.screen.fill(BLACK) # Plan B si la vidéo plante

        # 2. Dessin du titre (Ombre + Texte)
        title_text = "POKÉMON CLONE"
        shadow = self.title_font.render(title_text, True, (20, 20, 20))
        text = self.title_font.render(title_text, True, POKE_BLUE)
        self.screen.blit(shadow, (WIDTH // 2 - 346, 84))
        self.screen.blit(text, (WIDTH // 2 - 350, 80))

        # 3. Dessin des boutons
        for btn in self.buttons.values():
            btn.draw(self.screen)

    def handle_events(self, event, game_instance):
        # Clic sur CONTINUER
        if self.buttons["load"].is_clicked(event):
            if SaveManager.load_exists():
                # 1. On récupère les vraies données de sauvegarde
                data = SaveManager.get_game_data()
                saved_id = str(data.get("current_pokemon", "1"))

                # 2. On scanne le dossier pour trouver le nom complet du joueur (ex: "1 - Bulbizarre")
                all_sprites = os.listdir("asset/sprites/")
                player_full = next((f.replace(".png", "") for f in all_sprites if f.startswith(f"{saved_id} -")), "1 - Bulbizarre")
                
                # 3. On génère un ennemi aléatoire complet (ex: "4 - Salameche")
                enemy_id_rand = random.randint(1, 151)
                enemy_full = next((f.replace(".png", "") for f in all_sprites if f.startswith(f"{enemy_id_rand} -")), "4 - Salameche")

                # 4. On lance le combat avec les noms de fichiers corrects
                game_instance.battle_instance = Battle(game_instance.screen, player_full, enemy_full)
                game_instance.state = "BATTLE"
            else:
                # Optionnel : petit feedback si pas de save
                self.buttons["load"].text = "Vide !"

        # Clic sur NOUVELLE PARTIE
        elif self.buttons["new"].is_clicked(event):
            SaveManager.reset_game()
            SaveManager.reset_pokedex()
            print("Choisissez votre Pokémon...")
            game_instance.state = "LIST_ALL_VIEW"

        # Clic sur LISTE POKÉMON
        elif self.buttons["list"].is_clicked(event):
            game_instance.state = "LIST_ALL_VIEW"

        # Clic sur OPTIONS
        elif self.buttons["options"].is_clicked(event):
            print("Ouverture des options (Musique, Volume...)")