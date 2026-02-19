import pygame, sys, math
from __settings__ import BATTLE_FLOOR, REGULAR_FONT, LIGHT_GREEN, DARK_GREEN
from .util_tool import UtilTool

class AttackMenu:
    def __init__(self, screen, pokemon, pokemon_enemy):
        """
        Initializes the Attack menu with the current battle participants.
        """
        self.screen = screen
        self.pokemon = pokemon
        self.font = pygame.font.Font(None, 50)  # Font for menu items
        
        # Attack options are based on the Pokémon's types, with a 'Back' option added
        self.options = self.pokemon.type + ["Back"] 
        self.selected_index = 0  # Tracks which move is highlighted
        self.running = True      # Loop control flag
        self.util = UtilTool()
        self.pokemon_enemy = pokemon_enemy

    def display(self):
        """
        Main loop to display the moves and handle user selection during battle.
        """
        # Load environment textures
        battle_floor = self.util.load_image(BATTLE_FLOOR)
        battle_floor2 = pygame.transform.flip(battle_floor, True, False)
        
        # Load sprites: player sees their Pokémon from the back, enemy from the front
        pokemon_back = self.util.load_image(self.pokemon.get_back_image())
        pokemon_enemy = self.util.load_image(self.pokemon_enemy.get_image())
        
        # Floating animation variables
        time_count = 0
        var_x = 5
        var_y = 5
        speed = 1.5
        win = False
        
        while self.running:
            self.screen.update()
            
            # Apply floating movement using sine wave math for a dynamic feel
            if not win:
                time_count += speed
                x_movement = int(var_y * math.sin(time_count * 0.1))
                y_movement = int(var_x * math.sin(time_count * 0.08))
            
            # Draw the battle scene with animation offsets
            self.util.display_assets_and_background_in_fight(
                self.screen, x_movement, y_movement, 
                battle_floor, battle_floor2, 
                pokemon_enemy, pokemon_back
            )

            # Draw the menu UI overlay
            self.util.draw_option_screen(self.screen)

            # Render moves/options across the bottom menu
            for i, option in enumerate(self.options):
                # Apply highlight color to the currently selected move
                color = LIGHT_GREEN if i == self.selected_index else DARK_GREEN
                self.util.draw_text(
                    option, REGULAR_FONT, self.screen.width // 30, self.screen,
                    (self.screen.width // 2 + i * 200, self.screen.height // 8 * 7), 
                    color
                )

            pygame.display.flip()  # Update the screen

            # Input Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Navigate through moves horizontally
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    
                    # Return the name of the selected move or "Back"
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected_index]