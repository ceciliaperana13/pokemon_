import pygame, sys
from __settings__ import MAIN_MENU_BACKGROUND2, LIGHT_GREEN, REGULAR_FONT, DARK_GREEN, POKE_FONT
from .util_tool import UtilTool
from back_end.controller import get_player_names

class SelectPlayer:
    def __init__(self, screen):
        """Initializes the player selection screen."""
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        # Fetch the list of existing players from the controller
        self.options = get_player_names()
        self.selected_index = 0
        self.running = True
        self.util = UtilTool()

    def display(self):
        """Main loop for the player selection menu."""
        while self.running:
            # Update screen state and clear background
            self.screen.update()
            self.screen.get_display().fill((0, 0, 0))

            # Set background and draw main title
            self.screen.set_background_display(MAIN_MENU_BACKGROUND2)
            font_size = self.screen.height // 10
            self.util.draw_text("Select your player", POKE_FONT, font_size, self.screen,
                                (self.screen.width // 2, self.screen.height // 10 * 2), LIGHT_GREEN)

            # Draw the list of player names in a grid layout (3 columns of 5)
            for i, option in enumerate(self.options):
                # Highlight the currently selected player name
                if i == self.selected_index:
                    color = LIGHT_GREEN
                else:
                    color = "white"

                # Calculate vertical position based on a modulo of 5 (5 names per column)
                y = i % 5
                
                # Column 1 (Players 0-4)
                if i in range(0, 5):
                    self.util.draw_text(option, REGULAR_FONT, self.screen.height // 22, self.screen,
                                        (self.screen.width // 8 * 2, self.screen.height // 8 * y + self.screen.height // 8 * 3), color)
                
                # Column 2 (Players 5-9)
                elif i in range(5, 10):
                    self.util.draw_text(option, REGULAR_FONT, self.screen.height // 22, self.screen,
                                        (self.screen.width // 8 * 4, self.screen.height // 8 * y + self.screen.height // 8 * 3), color)

                # Column 3 (Players 10-14)
                elif i in range(10, 15):
                    self.util.draw_text(option, REGULAR_FONT, self.screen.height // 22, self.screen,
                                        (self.screen.width // 8 * 6, self.screen.height // 8 * y + self.screen.height // 8 * 3), color)
            
            pygame.display.flip()

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Navigate forward through the list
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    
                    # Navigate backward through the list
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)

                    # Confirm player selection
                    elif event.key == pygame.K_RETURN:
                        for index in range(len(self.options)):
                            if self.selected_index == index:
                                # Returns the chosen player name to the main game loop
                                return self.options[index]