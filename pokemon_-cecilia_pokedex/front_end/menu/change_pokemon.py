import pygame, sys
from __settings__ import LIGHT_GREEN, BATTLE_BACKGROUND, REGULAR_FONT, POKE_FONT
from front_end.menu.util_tool import UtilTool
from .display_pokemon_stat import PokemonStat
from back_end.controller import get_all_pokemons_from_pokedex

class ChangePokemon():
    def __init__(self, player_name, screen, pokemon_list=[]):
        """
        Initializes the Pokemon swap menu.
        Allows the player to browse through their caught Pokemon and view their stats.
        """
        self.player_name = player_name
        self.screen = screen
        self.background = BATTLE_BACKGROUND
        self.font = pygame.font.Font(None, 50)
        self.util = UtilTool()
        
        # Load the player's collection if no specific list is provided
        if not pokemon_list:
            self.pokemons = get_all_pokemons_from_pokedex(self.player_name)
        else:
            self.pokemons = pokemon_list

        # Create a list of names to display as menu options
        self.options = []
        for pokemon in self.pokemons:
            option = pokemon.name
            self.options.append(option)

        self.selected_index = 0
        self.running = True

    def display(self):
        """
        Main loop for the Pokemon selection menu.
        Returns the selected Pokemon object to the caller.
        """
        while self.running:
            # Refresh screen and set the battle background
            self.screen.update()
            self.screen.set_background_display(self.background)
            
            font_size = self.screen.height // 20
            
            # Draw the header title
            self.util.draw_text("Choose your pokemon", POKE_FONT, font_size, self.screen,
                                (self.screen.width//2, self.screen.height // 10*2), LIGHT_GREEN)

            # Render the list of Pokemon names
            for i, option in enumerate(self.options):
                # Highlight the currently hovered/selected name
                color = LIGHT_GREEN if i == self.selected_index else (255, 255, 255)
                self.util.draw_text(option, REGULAR_FONT, font_size,
                                    self.screen, (self.screen.width //2, self.screen.height // 10*3 + i*60), color)
                
            pygame.display.flip()

            # Process user input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    # Navigation: Move selection up or down
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)

                    # Confirmation: Open stats screen or confirm selection
                    elif event.key == pygame.K_RETURN:
                        for index in range(len(self.options)):
                            if self.selected_index == index:
                                # Show the stats for the selected Pokemon before returning
                                pokemon_enemy = None
                                PokemonStat(self.player_name, self.pokemons, self.pokemons[index], 
                                            pokemon_enemy, self.screen, self.background, 
                                            "in_pause_menu").display()
                                
                                # Return the selected Pokemon object to the game loop
                                return self.pokemons[self.selected_index]