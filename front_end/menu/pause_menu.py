import pygame, sys
from __settings__ import MAIN_MENU_BACKGROUND1, LIGHT_GREEN, REGULAR_FONT, POKE_FONT
from .util_tool import UtilTool
from .select_player import SelectPlayer
from .change_pokemon import ChangePokemon
from front_end.sounds import Sounds
from back_end.controller import get_all_pokemons_from_pokedex, get_first_pokemon, save_player_data, load_player_data

sounds = Sounds()

class PauseMenu:
    def __init__(self, player, pokemon, screen, pokedex, pokemon_list=[]):
        """
        Initialize the menu with the screen, font, options, and selected index.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 50)  # Set the font for menu text
        self.options = ["Continue", "Save Game", "Load Game", "Change Pokemon", "Exit"]  # Menu options
        self.selected_index = 0  # Index of the currently selected option
        self.running = True  # Controls the menu loop
        self.player = player
        self.pokemon = pokemon
        self.pokedex = pokedex  # 🆕 Pokédex
        self.util = UtilTool()
        if not pokemon_list:
            self.pokemons = get_all_pokemons_from_pokedex(self.player)
        else:
            self.pokemons = pokemon_list

    def save_game(self):
        """🆕 Sauvegarde la partie avec le Pokédex"""
        print("💾 Sauvegarde de la partie en cours...")
        
        try:
            # Préparer les données à sauvegarder
            save_data = {
                "player_name": self.player,
                "pokemon": self.pokemon,
                # 🔥 IMPORTANT : Sauvegarder les données du Pokédex
                "player_pokedex": self.pokedex.obtenir_donnees_sauvegarde()
            }
            
            # Appeler la fonction de sauvegarde
            save_player_data(self.player, save_data)
            
            print(f"✅ Partie sauvegardée avec succès pour {self.player}")
            print(f"   - Pokémon trouvés : {self.pokedex.nombre_pokemon_trouves()}")
            
            # Message visuel
            font_size = self.screen.height // 15
            self.util.draw_text("✓ Game Saved!", REGULAR_FONT, font_size, self.screen,
                              (self.screen.width//2, self.screen.height // 10*8), (0, 255, 0))
            pygame.display.flip()
            pygame.time.wait(1000)
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")

    def load_game(self):
        """🆕 Charge une autre sauvegarde"""
        print("📂 Chargement d'une autre sauvegarde...")
        
        # Sélectionner un joueur
        new_player = SelectPlayer(self.screen).display()
        
        if new_player:
            # Charger les données sauvegardées
            save_data = load_player_data(new_player)
            
            if save_data:
                # Charger le Pokémon
                self.pokemon = get_first_pokemon(new_player)
                self.player = new_player
                self.pokemons = get_all_pokemons_from_pokedex(new_player)
                
                # 🔥 IMPORTANT : Charger le Pokédex sauvegardé
                if "player_pokedex" in save_data:
                    self.pokedex.charger_donnees_sauvegarde(save_data["player_pokedex"])
                    print(f"✓ Pokédex chargé : {self.pokedex.nombre_pokemon_trouves()} Pokémon trouvés")
                
                # Quitter le menu pause et retourner au jeu avec les nouvelles données
                self.running = False
                return "loaded"
            else:
                print(f"⚠ Aucune sauvegarde trouvée pour {new_player}")
        
        return None

    def display(self):
        """
        Main menu loop that displays options and handles user input.
        """
        while self.running:
            self.screen.update()
            self.screen.get_display().fill((0, 0, 0))

            self.screen.set_background_display(MAIN_MENU_BACKGROUND1)
            
            font_size = self.screen.height // 10
            self.util.draw_text("Pause Menu", POKE_FONT, font_size, self.screen,\
                                (self.screen.width//2, self.screen.height // 10*2), LIGHT_GREEN)

            # Draw menu options
            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else (255, 255, 255)
                self.util.draw_text(option, REGULAR_FONT, font_size - 14, self.screen,\
                                (self.screen.width//2, self.screen.height // 10*3.5 + i*100), color)

            pygame.display.flip()

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        match self.selected_index:
                            case 0:  # Continue
                                sounds.stop_background_music()
                                sounds.play_map_music()
                                return self.player, self.pokemon
                            
                            case 1:  # Save Game
                                self.save_game()
                            
                            case 2:  # Load Game
                                result = self.load_game()
                                if result == "loaded":
                                    # Retourner avec le nouveau joueur et Pokémon
                                    sounds.stop_background_music()
                                    sounds.play_map_music()
                                    return self.player, self.pokemon
                            
                            case 3:  # Change Pokemon
                                self.pokemon = ChangePokemon(self.player, self.screen).display()
                                import front_end.gameplay.game as gameplay
                                game = gameplay.Game(self.screen, self.player, self.pokemon, self.pokedex)
                                
                                sounds.stop_background_music()
                                sounds.play_map_music()
                                game.run()
                            
                            case 4:  # Exit
                                pygame.quit()
                                sys.exit()
                    
                    elif event.key == pygame.K_ESCAPE:
                        # Échap ferme le menu pause et reprend le jeu
                        sounds.stop_background_music()
                        sounds.play_map_music()
                        return self.player, self.pokemon
        
        return self.player, self.pokemon