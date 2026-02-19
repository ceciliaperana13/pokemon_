import pygame, sys, math
from __settings__ import BATTLE_FLOOR, REGULAR_FONT, LIGHT_GREEN, DARK_GREEN
from .util_tool import UtilTool

class BagMenu:
    def __init__(self, screen, pokemon, pokemon_enemy, bag):
        """
        Initializes the Bag menu with the game screen, player Pokemon, enemy Pokemon, and bag inventory.
        """
        self.screen = screen
        self.bag = bag
        self.font = pygame.font.Font(None, 50)  # Standard font for menu interactions
        
        # Dynamic options list showing current quantities of items
        self.options = [
            f"Potion [{self.bag.get_potion()}]", 
            f"Pokeball [{self.bag.get_pokeball()}]", 
            "Back"
        ]
        
        self.selected_index = 0  # Tracks which item the user is currently highlighting
        self.running = True      # Controls the menu display loop
        self.util = UtilTool()
        self.pokemon = pokemon
        self.pokemon_enemy = pokemon_enemy

    def display(self):
        """
        Main loop to render the bag interface and handle item selection logic.
        """
        # Prepare visual assets for the battle background overlay
        battle_floor = self.util.load_image(BATTLE_FLOOR)
        battle_floor2 = pygame.transform.flip(battle_floor, True, False)
        
        # Flip player Pokemon sprite to face the enemy
        pokemon_sprite = pygame.transform.flip(
            self.util.load_image(self.pokemon.get_image()), True, False
        )
        pokemon_enemy_sprite = self.util.load_image(self.pokemon_enemy.get_image())
        
        # Animation variables for the idle floating effect
        time_count = 0
        var_x = 5
        var_y = 5
        speed = 1.5
        win = False
        
        while self.running:
            self.screen.update()
            
            # Sine wave calculations for smooth sprite movement
            if not win:
                time_count += speed
                x_movement = int(var_y * math.sin(time_count * 0.1))
                y_movement = int(var_x * math.sin(time_count * 0.08))
            
            # Draw the combat environment behind the menu
            self.util.display_assets_and_background(
                self.screen, x_movement, y_movement, 
                battle_floor, battle_floor2, 
                pokemon_enemy_sprite, pokemon_sprite
            )

            # Draw the semi-transparent box for the menu options
            self.util.draw_option_screen(self.screen)
            
            # Render each menu option horizontally
            for i, option in enumerate(self.options):
                # Highlight the selected index with a lighter green
                color = LIGHT_GREEN if i == self.selected_index else DARK_GREEN
                self.util.draw_text(
                    option, REGULAR_FONT, self.screen.width // 30, self.screen,
                    (self.screen.width // 2 + i * 200, self.screen.height // 8 * 7), 
                    color
                )

            pygame.display.flip()  # Update the display surface

            # Input Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Navigate through items (Supports Arrow keys and WASD/Left-Right)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    
                    # Confirm selection and return the item type to the combat controller
                    elif event.key == pygame.K_RETURN:
                        match self.selected_index:
                            case 0:
                                return "Potions"
                            case 1:
                                return "Pokeball"
                            case 2:
                                return "Back"