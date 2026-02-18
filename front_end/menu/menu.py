import pygame, sys
from __settings__ import MAIN_MENU_BACKGROUND1, LIGHT_GREEN, REGULAR_FONT, POKE_FONT
from .util_tool import UtilTool
from .name_input import NameInput
from .select_player import SelectPlayer
from front_end.sounds import Sounds
from front_end.gameplay.game import Game
from front_end.gameplay.pokedex_manager import Pokedex
from back_end.controller import get_first_pokemon, get_all_pokemons_from_pokedex

sounds = Sounds()

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.options = ["Start Game", "Resume Game", "Exit"]
        self.selected_index = 0
        self.running = True
        self.util = UtilTool()
        self.pokedex = Pokedex("back_end/data/pokedex.json")

    def display(self):
        self.screen.set_background_display("assets/wallpaper/wallpaper.mp4")
        
        while self.running:
            self.screen.update_video_background()
            
            font_size = self.screen.height // 10
            self.util.draw_text("Main Menu", POKE_FONT, font_size, self.screen,\
                                (self.screen.width//2, self.screen.height // 10*2), LIGHT_GREEN)

            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else (255, 255, 255)
                self.util.draw_text(option, REGULAR_FONT, font_size - 10, self.screen,\
                                (self.screen.width//2, self.screen.height // 10*4 + i*150), color)
        
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen.cleanup()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        match self.selected_index:
                            case 0:  # Nouvelle partie
                                player_name, pokemon = NameInput(self.screen).get_name()
                                game = Game(self.screen, player_name, pokemon, self.pokedex)
                                sounds.stop_background_music()
                                sounds.play_background_music()
                                game.run()

                            case 1:  # Reprendre une partie
                                select_player = SelectPlayer(self.screen).display()
                                # ✅ Tous les Pokémon au lieu du premier seulement
                                pokemon = get_all_pokemons_from_pokedex(select_player)
                                game = Game(self.screen, select_player, pokemon, self.pokedex)
                                sounds.stop_background_music()
                                sounds.play_map_music()
                                game.run()

                            case 2:  # Quitter
                                self.screen.cleanup()
                                pygame.quit()
                                sys.exit()