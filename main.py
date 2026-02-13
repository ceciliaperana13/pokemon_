import pygame
from settings import *
from menu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        # Initialisation de la fenêtre via ton fichier settings
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pokémon Clone - Menu")
        
        # On ne garde que le menu principal
        self.main_menu = MainMenu(self.screen)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"

    def run(self):
        while self.running:
            events = pygame.event.get()
            
            # 1. Événements globaux
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # 2. Logique et Dessin du Menu
            if self.state == "MENU":
                self.main_menu.update_cursor()
                self.main_menu.draw()
                
                for event in events:
                    # Gestion des clics et survols dans le menu
                    self.main_menu.handle_events(event, self)

                    # Exemple d'action sur un bouton spécifique
                    if self.main_menu.buttons["load"].is_clicked(event):
                        print("Bouton Charger cliqué !")

            # 3. Rafraîchissement
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    Game().run()