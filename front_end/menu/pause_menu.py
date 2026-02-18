import pygame, sys
from __settings__ import MAIN_MENU_BACKGROUND1, LIGHT_GREEN, REGULAR_FONT, POKE_FONT
from .util_tool import UtilTool
from .select_player import SelectPlayer
from .change_pokemon import ChangePokemon
from front_end.sounds import Sounds
from back_end.controller import get_all_pokemons_from_pokedex, get_first_pokemon
from front_end.gameplay.pokedex_manager import Pokedex

sounds = Sounds()

class PauseMenu:
    def __init__(self, player, pokemon, screen, pokedex, pokemon_list=[]):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.options = ["Continue", "Change Player", "Change Pokemon", "Exit"]
        self.selected_index = 0
        self.running = True
        self.player = player
        self.pokemon = pokemon
        self.pokedex = pokedex
        self.util = UtilTool()
        if not pokemon_list:
            self.pokemons = get_all_pokemons_from_pokedex(self.player)
        else:
            self.pokemons = pokemon_list

    def _nouveau_pokedex(self):
        """Crée une instance fraîche du Pokédex."""
        return Pokedex("back_end/data/pokedex.json")

    def load_game(self):
        """Charge une autre sauvegarde."""
        print("📂 Chargement d'une autre sauvegarde...")

        new_player = SelectPlayer(self.screen).display()

        if new_player:
            self.player   = new_player
            self.pokemon  = get_all_pokemons_from_pokedex(new_player)
            self.pokemons = self.pokemon
            # ✅ Pokédex vierge — Game s'occupera de l'enregistrer
            self.pokedex  = self._nouveau_pokedex()
            self.running  = False
            return "loaded"
        
        return None

    def display(self):
        while self.running:
            self.screen.update()
            self.screen.get_display().fill((0, 0, 0))
            self.screen.set_background_display(MAIN_MENU_BACKGROUND1)

            font_size = self.screen.height // 10
            self.util.draw_text("Pause Menu", POKE_FONT, font_size, self.screen,
                                (self.screen.width//2, self.screen.height // 10*2), LIGHT_GREEN)

            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else (255, 255, 255)
                self.util.draw_text(option, REGULAR_FONT, font_size - 14, self.screen,
                                (self.screen.width//2, self.screen.height // 10*3.5 + i*100), color)

            pygame.display.flip()

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

                            case 1:  # Charger une autre save
                                result = self.load_game()
                                if result == "loaded":
                                    sounds.stop_background_music()
                                    sounds.play_map_music()
                                    return self.player, self.pokemon

                            case 2:  # Changer de Pokémon
                                self.pokemon = ChangePokemon(self.player, self.screen).display()
                                import front_end.gameplay.game as gameplay
                                # ✅ Pokédex vierge pour la nouvelle session
                                game = gameplay.Game(
                                    self.screen, self.player,
                                    self.pokemon, self._nouveau_pokedex()
                                )
                                sounds.stop_background_music()
                                sounds.play_map_music()
                                game.run()

                            case 3:  # Quitter
                                pygame.quit()
                                sys.exit()

                    elif event.key == pygame.K_ESCAPE:
                        sounds.stop_background_music()
                        sounds.play_map_music()
                        return self.player, self.pokemon

        return self.player, self.pokemon