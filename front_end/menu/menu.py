import pygame, sys
from __settings__ import MAIN_MENU_BACKGROUND1, LIGHT_GREEN, REGULAR_FONT, POKE_FONT
from .util_tool import UtilTool
from .name_input import NameInput
from .select_player import SelectPlayer
from front_end.sounds import Sounds
from front_end.gameplay.game import Game
from front_end.gameplay.pokedex_manager import Pokedex
from back_end.controller import get_first_pokemon, get_all_pokemons_from_pokedex

# Initialize the global sound controller
sounds = Sounds()

class Menu:
    def __init__(self, screen):
        """Initializes the main menu state."""
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.options = ["Start Game", "Resume Game", "Exit"]
        self.selected_index = 0
        self.running = True
        self.util = UtilTool()
        # Note: self.pokedex is not stored here to ensure a fresh instance is created for each session

    def _new_pokedex(self):
        """Creates a fresh instance of the Pokédex for every new session."""
        return Pokedex("back_end/data/pokedex.json")

    def display(self):
        """Displays the main menu with a video background and handles navigation."""
        # Set the dynamic video background
        self.screen.set_background_display("assets/wallpaper/wallpaper.mp4")
        
        while self.running:
            # Update the video frames for the background
            self.screen.update_video_background()
            
            font_size = self.screen.height // 10
            
            # Draw Main Title
            self.util.draw_text("Main Menu", POKE_FONT, font_size, self.screen,
                                (self.screen.width//2, self.screen.height // 10*2), LIGHT_GREEN)

            # Draw Menu Options with highlighting for the selection
            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else (255, 255, 255)
                self.util.draw_text(option, REGULAR_FONT, font_size - 10, self.screen,
                                (self.screen.width//2, self.screen.height // 10*4 + i*150), color)
        
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen.cleanup()
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Keyboard navigation
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    
                    # Confirm Selection
                    elif event.key == pygame.K_RETURN:
                        match self.selected_index:
                            case 0:  # New Game logic
                                player_name, pokemon = NameInput(self.screen).get_name()
                                pokedex = self._new_pokedex()  # Create a fresh Pokédex instance
                                game = Game(self.screen, player_name, pokemon, pokedex)
                                
                                sounds.stop_background_music()
                                sounds.play_background_music()
                                game.run()

                            case 1:  # Resume existing save
                                select_player = SelectPlayer(self.screen).display()
                                pokemon = get_all_pokemons_from_pokedex(select_player)
                                pokedex = self._new_pokedex()  # Create a fresh Pokédex instance
                                game = Game(self.screen, select_player, pokemon, pokedex)
                                
                                sounds.stop_background_music()
                                sounds.play_map_music()
                                game.run()

                            case 2:  # Quit Application
                                self.screen.cleanup()
                                pygame.quit()
                                sys.exit()