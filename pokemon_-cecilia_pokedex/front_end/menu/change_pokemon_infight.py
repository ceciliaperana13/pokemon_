import pygame, sys, math
from __settings__ import BATTLE_BACKGROUND, BATTLE_FLOOR, REGULAR_FONT, LIGHT_GREEN, DARK_GREEN
from .util_tool import UtilTool
from .display_pokemon_stat import PokemonStat
from back_end.controller import get_all_pokemons_from_pokedex, save_pokemon_to_pokedex

class ChangePokemonInFight():
    def __init__(self, player_name, pokemon, pokemon_enemy, screen, pokemon_list=[]):
        """
        Initializes the in-battle Pokemon switching menu.
        Synchronizes the current active Pokemon's state with the team list.
        """
        self.player_name = player_name
        self.screen = screen
        self.background = BATTLE_BACKGROUND
        self.font = pygame.font.Font(None, 50)
        self.util = UtilTool()
        self.pokemon_enemy = pokemon_enemy
        self.pokemon = pokemon

        # Load player's Pokemon and ensure the current active Pokemon is updated in the list
        if not pokemon_list:
            self.pokemons = get_all_pokemons_from_pokedex(self.player_name)
            index_to_pop = 0
            for p in self.pokemons:
                if p.pet_name == self.pokemon.pet_name:
                    index_to_pop = self.pokemons.index(p)
                    self.pokemons.pop(index_to_pop)
                    break
            # Re-insert the current active instance to preserve health/status changes
            self.pokemons.insert(index_to_pop, self.pokemon)
        else:
            self.pokemons = pokemon_list

        # Prepare menu options (Pokemon names)
        self.options = [p.name for p in self.pokemons]
        self.selected_index = 0
        self.running = True

    def display(self):
        """
        Main loop for displaying the switch menu overlaying the battle scene.
        """
        # Load battle environment assets
        battle_floor = self.util.load_image(BATTLE_FLOOR)
        battle_floor2 = pygame.transform.flip(battle_floor, True, False)
        pokemon_enemy_img = self.util.load_image(self.pokemon_enemy.get_image())
        
        # Animation variables for the "floating" sprite effect
        time_count = 0
        var_x = 5
        var_y = 5
        speed = 1.5
        win = False
        
        self.screen.set_background_display(self.background)

        while self.running:
            # Prepare current active Pokemon sprite
            my_pokemon_img = pygame.transform.flip(self.util.load_image(self.pokemon.get_image()), True, False)

            self.screen.update()
            
            # Calculate floating movement using sine waves
            if not win:
                time_count += speed
                x_movement = int(var_y * math.sin(time_count * 0.1))
                y_movement = int(var_x * math.sin(time_count * 0.08))
            
            # Draw battle background and sprites
            self.util.display_assets_and_background(self.screen, x_movement, y_movement, 
                                                     battle_floor, battle_floor2, 
                                                     pokemon_enemy_img, my_pokemon_img)

            # Draw the selection window overlay
            self.util.draw_window_with_background(self.screen, self.screen.width//2, self.screen.height //2)

            # Render Pokemon selection in a 3x3 grid layout
            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else DARK_GREEN
                
                # Calculate grid position (y is row, columns are handled by width multipliers)
                y_grid = i % 3
                
                # Column 1 (Index 0-2)
                if i in range(0, 3):
                    self.util.draw_text(option, REGULAR_FONT, self.screen.height//22, self.screen,
                                        (self.screen.width // 8*3, self.screen.height // 8 * y_grid + self.screen.height // 8*3), color)
                # Column 2 (Index 3-5)
                elif i in range(3, 6):
                    self.util.draw_text(option, REGULAR_FONT, self.screen.height//22, self.screen,
                                        (self.screen.width // 8*4, self.screen.height // 8 * y_grid + self.screen.height // 8*3), color)
                # Column 3 (Index 6-8)
                elif i in range(6, 9):
                    self.util.draw_text(option, REGULAR_FONT, self.screen.height//22, self.screen,
                                        (self.screen.width // 8*5, self.screen.height // 8 * y_grid + self.screen.height // 8*3), color)

            pygame.display.flip()

            # Input Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Navigate through Pokemon options
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)

                    # Confirm selection
                    elif event.key == pygame.K_RETURN:
                        # Save current state before switching
                        save_pokemon_to_pokedex(self.player_name, self.pokemon)
                        
                        # Show stats for the selected Pokemon
                        PokemonStat(self.player_name, self.pokemons, self.pokemons[self.selected_index], 
                                    self.pokemon_enemy, self.screen, self.background, "in_fight").display()
                        
                        # Check if we stayed with the same Pokemon or switched
                        if self.pokemons[self.selected_index].pet_name == self.pokemon.pet_name:
                            return self.pokemon
                        else:
                            return self.pokemons[self.selected_index]
                    
                    # Cancel and return current active Pokemon
                    elif event.key == pygame.K_ESCAPE:
                        return self.pokemon