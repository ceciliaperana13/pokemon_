import pygame, sys, math
from .util_tool import UtilTool
from __settings__ import BATTLE_FLOOR, REGULAR_FONT, LIGHT_GREEN, DARK_GREEN

class InfoMenu:
    def __init__(self, screen, pokemon, pokemon_enemy):
        """
        Initialize the menu with the screen, font, options, and selected index.
        """
        self.screen = screen
        self.pokemon = pokemon
        self.pokemon_enemy = pokemon_enemy
        self.font = pygame.font.Font(None, 50)  # Set the font for menu text
        # Menu options dynamically named based on the current Pokémon
        self.options = [f"{self.pokemon.name}", f"{self.pokemon_enemy.name}", "Back"]
        self.selected_index = 0  # Index of the currently selected option
        self.running = True  # Controls the menu loop
        self.util = UtilTool()

    def display(self):
        """
        Main menu loop that displays options and handles user input.
        """
        # Load and prepare battle visual assets
        battle_floor = self.util.load_image(BATTLE_FLOOR)
        battle_floor2 = pygame.transform.flip(battle_floor, True, False)
        # Flip player Pokémon to face the enemy
        pokemon = pygame.transform.flip(self.util.load_image(self.pokemon.get_image()), True, False)
        pokemon_enemy = self.util.load_image(self.pokemon_enemy.get_image())
        
        # Variables for the hovering animation (floating effect)
        time_count = 0
        var_x = 5
        var_y = 5
        speed = 1.5
        win = False
        what_to_display = 3  # Control variable to decide which info overlay to show

        while self.running:
            self.screen.update()
            
            # Calculate floating animation using sine waves
            if not win:
                time_count += speed
                x_movement = int(var_y * math.sin(time_count * 0.1))
                y_movement = int(var_x * math.sin(time_count * 0.08))
            
            # Render background and Pokémon sprites
            self.util.display_assets_and_background(self.screen, x_movement, y_movement, battle_floor, battle_floor2, pokemon_enemy, pokemon)

            # Draw the UI container for the options
            self.util.draw_option_screen(self.screen)

            # Conditional rendering based on user selection
            if what_to_display == 0:
                self.draw_info_screen(self.pokemon)
            elif what_to_display == 1:
                self.draw_info_screen(self.pokemon_enemy)
 
            # Draw menu interaction buttons (Player Name, Enemy Name, Back)
            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else DARK_GREEN  # Highlight selection
                self.util.draw_text(option, REGULAR_FONT, self.screen.width //30, self.screen,\
                                    (self.screen.width//2 + i * 200, self.screen.height//8*7), color)

            pygame.display.flip()  # Update the full display Surface to the screen

            # Handle user input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit game
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Horizontal navigation through the menu
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    
                    # Action selection logic
                    elif event.key == pygame.K_RETURN:
                        match self.selected_index:
                            case 0:  # Display Player Pokémon Stats
                                what_to_display = 0
                            case 1:  # Display Enemy Pokémon Stats
                                what_to_display = 1
                            case 2:  # Close Info Menu
                                return

    def draw_info_screen(self, actual_pokemon):
        """
        Renders a centered window overlay showing specific Pokémon statistics.
        """
        # Draw the popup window frame
        self.util.draw_window_with_background(self.screen, self.screen.width //2.5, self.screen.height //2.5)
        
        font_size = self.screen.height // 20
        x = self.screen.width // 2
        y = self.screen.height // 2
        
        # Render various statistics line by line
        self.util.draw_text(f"{actual_pokemon.name}",\
                              REGULAR_FONT, font_size , self.screen, (x, y - font_size*2))
        self.util.draw_text(f"Level : {str(actual_pokemon.get_level())}",\
                                REGULAR_FONT, font_size , self.screen, (x, y - font_size))
        self.util.draw_text(f"Strength : {str(actual_pokemon.get_strength())}",\
                              REGULAR_FONT, font_size , self.screen, (x, y ))
        self.util.draw_text(f"Defense : {str(actual_pokemon.get_defense())}",\
                              REGULAR_FONT, font_size , self.screen, (x, y + font_size))
        # Joins types with a comma if the Pokémon has multiple types
        self.util.draw_text(f"Type : {str(', '.join(actual_pokemon.type))}",\
                              REGULAR_FONT, font_size , self.screen, (x, y + font_size*2))