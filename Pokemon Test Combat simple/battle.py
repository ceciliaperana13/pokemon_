import pygame
import random
from settings import *
from button import Button
import os
from battle_engine import BattleEngine
from savemanager import SaveManager


class Battle:
    def __init__(self, screen, player_id, enemy_id):
        self.screen = screen
        self.engine = BattleEngine()  # On initialise la logique
        # On enregistre l'ennemi dans le pokedex dès le début de la rencontre
        self.engine.register_encounter(enemy_id)
        self.player_type = self.engine.get_pokemon_type(player_id)
        self.enemy_type = self.engine.get_pokemon_type(enemy_id)
        print(f"Combat : {self.player_type} VS {self.enemy_type}")
        self.player_name = player_id  # Ex: "16 - Dracolosse"
        self.enemy_name = enemy_id
        self.player_hp = 100
        self.enemy_hp = 100
        self.player_turn = True
        self.player_shake = 0
        self.enemy_shake = 0
        self.battle_log = "Que doit faire votre Pokémon ?"
        # On utilise directement le nom récupéré de la liste
        # player_id contient déjà "1 - Bulbizarre"
        p_path = f"asset/sprites/{player_id}.png"
        # Pour l'ennemi aléatoire, c'est plus complexe car il faut trouver
        # le nom du fichier qui commence par l'ID aléatoire
        # On vérifie si e_path contient déjà .png pour éviter "14 - Minidraco.png.png
        all_sprites = os.listdir("asset/sprites/")
        enemy_filename = next(
            (f for f in all_sprites if f.startswith(str(enemy_id) + " -")), None
        )
        if enemy_filename:
            e_path = f"asset/sprites/{enemy_filename}"
        else:
            e_path = p_path  # Secours

        try:
            self.player_img = pygame.image.load(p_path).convert_alpha()
            self.enemy_img = pygame.image.load(e_path).convert_alpha()
            self.player_img = pygame.transform.scale(self.player_img, (250, 250))
            self.enemy_img = pygame.transform.scale(self.enemy_img, (250, 250))
        except Exception as e:
            print(f"Erreur image : {e}")
            # Carré de secours si l'image n'est pas trouvée
            self.player_img = pygame.Surface((250, 250))
            self.player_img.fill((0, 0, 255))  # Bleu pour le joueur
            self.enemy_img = pygame.Surface((250, 250))
            self.enemy_img.fill((255, 0, 0))  # Rouge pour l'ennemi

        self.buttons = {
            "attack": Button("ATTAQUER", 500, 480, 250, 50, (200, 0, 0)),
            "flee": Button("FUIR", 500, 540, 250, 50, (100, 100, 100)),
        }

        # Nouveaux boutons de fin de match (cachés au début)
        self.end_buttons = {
            "save": Button(
                "Sauvegarder",
                WIDTH // 2 - 100,
                HEIGHT // 2 - 40,
                200,
                45,
                (46, 204, 113),
            ),
            "menu": Button(
                "Menu Principal",
                WIDTH // 2 - 100,
                HEIGHT // 2 + 30,
                200,
                45,
                (149, 165, 166),
            ),
            "replay": Button(
                "Rejouer", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 45, (52, 152, 219)
            ),
        }
        self.show_end_menu = False

    def handle_input(self, events, game_instance):
        for event in events:
            if self.show_end_menu:
                # --- LOGIQUE MENU DE FIN ---
                if self.end_buttons["save"].is_clicked(event):
                    # On prépare les données de progression
                    clean_id = str(self.player_name).split(" - ")[0].strip()

                    new_game_data = {
                        "current_pokemon": clean_id,
                        "x": 400,  # Ou game_instance.player.x si tu as un perso qui bouge
                        "y": 300,
                    }
                    # On utilise la méthode spécifique pour sauvegarde.json
                    SaveManager.save_game_data(new_game_data)

                    self.end_buttons["save"].text = "Sauvegardé !"
                    self.battle_log = "Progression enregistrée dans sauvegarde.json"

                elif self.end_buttons["menu"].is_clicked(event):
                    game_instance.state = "MENU"

                elif self.end_buttons["replay"].is_clicked(event):
                    game_instance.state = "LIST_ALL_VIEW"

            else:
                # --- LOGIQUE COMBAT ---
                if self.player_turn and self.player_hp > 0:
                    if self.buttons["attack"].is_clicked(event):
                        dmg, mult = self.engine.compute_damage(
                            self.player_type, self.enemy_type
                        )
                        self.enemy_hp -= dmg
                        self.shake_sprite("enemy")  # L'ennemi tremble !
                        eff_msg = (
                            " C'est super efficace !"
                            if mult > 1
                            else " Ce n'est pas très efficace..." if mult < 1 else ""
                        )
                        self.battle_log = (
                            f"Attaque {self.player_type} !{eff_msg} -{dmg} PV"
                        )

                        self.draw()
                        pygame.display.flip()
                        pygame.time.delay(1000)
                        self.player_turn = False

                    elif self.buttons["flee"].is_clicked(event):
                        game_instance.state = "MENU"

    def update(self, game_instance):
        # 1. Vérification du vainqueur
        winner, loser = self.engine.get_result(
            self.player_hp, self.enemy_hp, self.player_name, self.enemy_name
        )

        if winner:
            self.show_end_menu = True
            self.battle_log = f"Fini ! {winner} a gagné."
            # On récupère l'ID de l'ENNEMI pour le Pokédex
            # Juste après que le combat soit fini (quand show_end_menu devient True)
            # On force le nom en texte (str) avant de faire le split
            enemy_str = str(self.enemy_name)
            if " - " in enemy_str:
                enemy_id_only = enemy_str.split(" - ")[0].strip()
            else:
                enemy_id_only = enemy_str.strip()
            # On convertit en int puis en str pour enlever les zéros inutiles (ex: "04" -> "4")
            try:
                clean_id = str(int(enemy_id_only))
                self.engine.register_encounter(clean_id)
            except ValueError:
                print(f"Erreur : l'ID {enemy_id_only} n'est pas un nombre valide.")
            return  # On sort de la fonction, le combat est terminé !

        # 2. Tour de l'ennemi (seulement si le combat n'est pas fini)
        elif not self.player_turn:
            # On affiche d'abord le message "réfléchit" pour que l'écran ne soit pas figé
            self.battle_log = f"{self.enemy_name} prépare son attaque..."
            self.draw()
            pygame.display.flip()
            pygame.time.delay(1000)
            # Calcul des dégâts (tu peux utiliser ton engine ici aussi pour les types !)
            damage, mult = self.engine.compute_damage(self.enemy_type, self.player_type)
            self.player_hp -= damage
            self.shake_sprite("player")  # Le joueur tremble !
            eff_msg = " C'est super efficace !" if mult > 1 else ""
            self.battle_log = f"{self.enemy_name} réplique ! -{damage} PV.{eff_msg}"
            # Le tour revient au joueur, les boutons réapparaissent via le draw()
            self.player_turn = True

    def draw(self):
        self.screen.fill((240, 240, 240))  # Fond clair
        # Dessin des Pokémon avec l'effet de shake
        # random.randint crée l'oscillation si le shake est > 0
        p_offset = (
            random.randint(-self.player_shake, self.player_shake)
            if self.player_shake > 0
            else 0
        )
        e_offset = (
            random.randint(-self.enemy_shake, self.enemy_shake)
            if self.enemy_shake > 0
            else 0
        )
        self.screen.blit(self.player_img, (100 + p_offset, 200 + p_offset))
        self.screen.blit(self.enemy_img, (490 + e_offset, 50 + e_offset))
        # On diminue le shake à chaque frame pour qu'il s'arrête vite
        if self.player_shake > 0:
            self.player_shake -= 2
        if self.enemy_shake > 0:
            self.enemy_shake -= 2
        # Barres de vie
        self.draw_health_bar(150, 180, self.player_hp, "Joueur")
        self.draw_health_bar(520, 30, self.enemy_hp, "Ennemi")

        # Zone de texte (Rectangle noir en bas)
        pygame.draw.rect(self.screen, (20, 20, 20), (0, 450, WIDTH, 150))

        # AFFICHAGE DU MESSAGE (LOG)
        font = pygame.font.SysFont("Arial", 28)
        text_surf = font.render(self.battle_log, True, (255, 255, 255))
        self.screen.blit(text_surf, (50, 500))

        # --- GESTION DE L'AFFICHAGE PRIORITAIRE ---
        if self.show_end_menu:
            # 1. Menu de fin (Filtre noir + boutons spécifiques)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            for btn in self.end_buttons.values():
                btn.draw(self.screen)

        elif self.player_turn:
            # 2. Boutons de combat : UNIQUEMENT si c'est le tour du joueur
            # On utilise une boucle pour dessiner "attack" et "flee" d'un coup
            for btn in self.buttons.values():
                btn.draw(self.screen)

    def draw_health_bar(self, x, y, hp, label):
        # Fond vide
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, 200, 15))
        # PV restants (vert)
        current_hp_width = max(0, hp * 2)
        color = (0, 255, 0) if hp > 40 else (255, 165, 0) if hp > 15 else (255, 0, 0)
        pygame.draw.rect(self.screen, color, (x, y, current_hp_width, 15))
        # Contour
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 200, 15), 2)

    def shake_sprite(self, target):
        """Définit l'intensité du tremblement (pixel)."""
        if target == "player":
            self.player_shake = 15
        else:
            self.enemy_shake = 15
