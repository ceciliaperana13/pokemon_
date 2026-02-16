import pygame, sys
from __settings__ import MAIN_MENU_BACKGROUND1, LIGHT_GREEN, REGULAR_FONT, POKE_FONT
from .util_tool import UtilTool
from .name_input import NameInput
from .select_player import SelectPlayer
from front_end.sounds import Sounds
from front_end.gameplay.game import Game
from front_end.gameplay.pokedex_manager import Pokedex
from back_end.controller import get_first_pokemon

sounds = Sounds()

class Menu:
    def __init__(self, screen):
        """
        Initialize the menu with the screen, font, options, and selected index.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 50)  # Set the font for menu text
        self.options = ["Start Game", "Resume Game", "Exit"]  # Menu options
        self.selected_index = 0  # Index of the currently selected option
        self.running = True  # Controls the menu loop
        self.util = UtilTool()
        
        # 🆕 Initialiser le Pokédex avec le bon chemin
        self.pokedex = Pokedex("back_end/data/pokedex.json")

    def display(self):
        """
        Main menu loop that displays options and handles user input.
        """
        # Charger la vidéo background une seule fois au début
        self.screen.set_background_display("assets/wallpaper/wallpaper.mp4")  # Sans le / au début
        
        while self.running:
            # Mettre à jour la vidéo background (nouvelle frame)
            self.screen.update_video_background()
            
            font_size = self.screen.height // 10
            self.util.draw_text("Main Menu", POKE_FONT, font_size, self.screen,\
                                (self.screen.width//2, self.screen.height // 10*2), LIGHT_GREEN)

            # Draw menu options
            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else (255, 255, 255)  # Highlight selected option
                self.util.draw_text(option, REGULAR_FONT, font_size - 10, self.screen,\
                                (self.screen.width//2, self.screen.height // 10*4 + i*150), color)
        
            pygame.display.flip()  # Refresh the screen

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If user closes the window
                    self.screen.cleanup()  # Libérer les ressources vidéo
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:  # Navigate down
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:  # Navigate up
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:  # Select an option
                        match self.selected_index:
                            case 0:  # Start a new game
                                player_name, pokemon = NameInput(self.screen).get_name()
                                # Passer le Pokédex au jeu
                                game = Game(self.screen, player_name, pokemon, self.pokedex)
                                
                                # Stop the opening music and start the map music
                                sounds.stop_background_music()
                                sounds.play_background_music()

                                game.run()
                            case 1:  # Resume game
                                select_player = SelectPlayer(self.screen).display()
                                pokemon = get_first_pokemon(select_player)
                                # Passer le Pokédex au jeu
                                game = Game(self.screen, select_player, pokemon, self.pokedex)

                                # Stop the opening music and start the map music
                                sounds.stop_background_music()
                                sounds.play_map_music()
                                
                                game.run()
                            case 2:  # Exit
                                self.screen.cleanup()  # Libérer les ressources vidéo
                                pygame.quit()
                                sys.exit()