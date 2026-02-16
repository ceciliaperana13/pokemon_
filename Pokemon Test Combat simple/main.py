import pygame
import os
import random
from settings import *
from menu import MainMenu
from pokemonlist import PokemonList
from pokedex import PokedexView
from savemanager import SaveManager
from battle import Battle

class Game:
    def __init__(self):
        pygame.init()
        # On s'assure que les fichiers JSON existent avant de charger le menu
        SaveManager.init_files()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pokémon Clone")
        # Initialisation des moteurs et menus
        self.main_menu = MainMenu(self.screen)
        self.available_list_view = PokemonList(self.screen)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        self.pokedex_view = PokedexView(self.screen)

    def run(self):
        while self.running:
            events = pygame.event.get()
            # 1. Événements globaux (Quitter et Echap)
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.state = "PAUSE"
                    elif self.state == "PAUSE":
                        self.state = "PLAYING"
                    elif self.state == "LIST_ALL_VIEW":
                        self.state = "MENU"

            # 2. Logique et Dessin selon l'état
            if self.state == "MENU":
                self.main_menu.update_cursor()
                self.main_menu.draw()  # Affiche la vidéo et les boutons
                for event in events:
                    self.main_menu.handle_events(event, self)
                    # --- AJOUT DU CLIC POKÉDEX ---
                    if self.main_menu.buttons["pokedex"].is_clicked(event):
                        self.state = "POKEDEX"

                    if self.main_menu.buttons["load"].is_clicked(event):
                        if SaveManager.load_exists():
                            data = SaveManager.get_game_data()
                            # On récupère l'ID (ex: "1")
                            saved_id = str(data.get("current_pokemon", "1")).strip()
                            
                            # On scanne le dossier pour trouver le nom COMPLET (ex: "1 - Bulbizarre.png")
                            sprite_dir = "asset/sprites/"
                            all_files = os.listdir(sprite_dir)
                            
                            # On cherche le fichier qui commence par "ID -"
                            player_file = next((f for f in all_files if f.startswith(f"{saved_id} -")), None)
                            
                            if player_file:
                                # On enlève le ".png" pour l'envoyer à la classe Battle
                                player_poke_name = player_file.replace(".png", "")
                                
                                # Génération d'un ennemi aléatoire (ex: entre 1 et 18)
                                enemy_id_num = random.randint(1, 18)
                                enemy_file = next((f for f in all_files if f.startswith(f"{enemy_id_num} -")), None)
                                
                                if enemy_file:
                                    enemy_poke_name = enemy_file.replace(".png", "")
                                    # On lance enfin le combat avec les noms complets
                                    self.battle_instance = Battle(self.screen, player_poke_name, enemy_poke_name)
                                    self.state = "BATTLE"
                                else:
                                    print(f"Erreur : Aucun sprite trouvé pour l'ennemi {enemy_id_num}")
                            else:
                                print(f"Erreur : Aucun sprite trouvé pour l'ID joueur {saved_id}")
                        else:
                            self.main_menu.buttons["load"].text = "Pas de sauvegarde !"

            elif self.state == "LIST_ALL_VIEW":
                self.available_list_view.handle_input(events)
                self.available_list_view.display()

                for event in events:
                    # 1. Gestion du bouton retour
                    if self.available_list_view.btn_back.is_clicked(event):
                        self.state = "MENU"

                    # 2. SELECTION DU POKEMON
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # CONDITION CRUCIALE : On ne vérifie l'ID que si c'est un CLIC GAUCHE (bouton 1)
                        # Cela ignore la molette (boutons 4 et 5)
                        if event.button == 1:
                            player_poke_id = self.available_list_view.get_id_at_mouse(
                                event.pos
                            )

                            if player_poke_id:
                                # On choisit un ennemi au hasard entre 1 et 151
                                enemy_poke_id = random.randint(1, 151)

                                # Sauvegarde du choix
                                SaveManager.save_pokemon_choice(player_poke_id)

                                # Lancement du combat
                                self.battle_instance = Battle(
                                    self.screen, player_poke_id, enemy_poke_id
                                )
                                self.state = "BATTLE"

            # Dans main.py, sous l'état BATTLE
            elif self.state == "BATTLE":
                self.battle_instance.handle_input(
                    events, self
                )  # On passe 'self' (le jeu)
                self.battle_instance.update(self)
                self.battle_instance.draw()

            # Dans le run (gestion des états)
            elif self.state == "POKEDEX":
                self.pokedex_view.display()
                for event in events:
                    if self.pokedex_view.btn_back.is_clicked(event):
                        self.state = "MENU"

            # 3. Rafraîchissement
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    Game().run()
