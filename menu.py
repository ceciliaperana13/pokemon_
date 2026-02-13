import pygame
from settings import *
from button import Button
from settings import VideoBackground 

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font("asset/font/Pocket-Monk.otf", 62)
        
        # Background et Audio
        self.video = VideoBackground("asset/wallpaper/wallpaper.mp4", WIDTH, HEIGHT)
        self.setup_music()

        # Création des boutons (Tous actifs par défaut maintenant)
        self.buttons = {
            "load": Button("Continuer", 45, 180, 300, 50, WHITE),
            "new": Button("Nouvelle Partie", 45, 245, 300, 50, WHITE),
            "list": Button("Liste de Pokémon", 45, 310, 300, 50, WHITE),
            "options": Button("Options", 45, 375, 300, 50, WHITE)
        }

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
            self.screen.fill(BLACK)

        # 2. Dessin du titre
        title_text = "POKÉMON CLONE"
        shadow = self.title_font.render(title_text, True, (20, 20, 20))
        text = self.title_font.render(title_text, True, POKE_BLUE)
        self.screen.blit(shadow, (WIDTH // 2 - 346, 84))
        self.screen.blit(text, (WIDTH // 2 - 350, 80))

        # 3. Dessin des boutons
        for btn in self.buttons.values():
            btn.draw(self.screen)

    def handle_events(self, event, game_instance):
        # Ici on ne garde que les prints pour tester si les clics fonctionnent
        if self.buttons["load"].is_clicked(event):
            print("Action : Continuer")

        elif self.buttons["new"].is_clicked(event):
            print("Action : Nouvelle Partie")

        elif self.buttons["list"].is_clicked(event):
            print("Action : Liste Pokémon")

        elif self.buttons["options"].is_clicked(event):
            print("Action : Options")