import pygame
from __settings__ import MAIN_MENU_BACKGROUND4, LIGHT_GREEN, REGULAR_FONT, POKE_FONT
from .util_tool import UtilTool
from .selectpokemon import SelectPokemon
from .intro import IntroChoice
from back_end.controller import does_player_exist, get_first_pokemon

class NameInput:
    def __init__(self, screen):
        """Initializes the name input screen."""
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.player_name = ""
        self.util = UtilTool()

    def get_name(self):
        """Main loop to capture the player's name and handle character creation or loading."""
        while True:
            # Refresh screen and draw background
            self.screen.update()
            self.screen.get_display().fill((0, 0, 0))
            self.screen.set_background_display(MAIN_MENU_BACKGROUND4)
            
            font_size = self.screen.height // 15
            
            # Draw UI instructions and current name string
            self.util.draw_text("Enter your name", POKE_FONT, font_size, self.screen,
                                (self.screen.width // 2, self.screen.height // 3), "white")

            self.util.draw_text(self.player_name, REGULAR_FONT, font_size, self.screen,
                                (self.screen.width // 2, self.screen.height // 2), LIGHT_GREEN)
 
            self.util.draw_text("(Press enter key to continue)", REGULAR_FONT, font_size, self.screen,
                                (self.screen.width // 2, self.screen.height // 3*2), "white")

            pygame.display.flip()

            # Event handling for text input and navigation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pass
                    
                    # Confirm name entry
                    if event.key == pygame.K_RETURN and self.player_name:
                        # Case 1: Player already exists in database
                        if does_player_exist(self.player_name):
                            pygame.time.wait(1000)
                            # Fetch the first Pokemon associated with this save
                            pokemon = get_first_pokemon(self.player_name)
                            return self.player_name, pokemon
                        
                        # Case 2: New player creation
                        else:
                            # Play the introduction sequences
                            IntroChoice(self.player_name, self.screen).display()
                            # Open the starter Pokemon selection screen
                            my_pokemon = SelectPokemon(self.player_name, self.screen).display()

                            return self.player_name, my_pokemon
                    
                    # Handle character deletion
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    
                    # Capture alphanumeric characters for the name
                    elif event.unicode.isalnum():
                        self.player_name += event.unicode