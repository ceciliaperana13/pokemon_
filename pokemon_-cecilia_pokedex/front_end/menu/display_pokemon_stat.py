import pygame
from __settings__ import REGULAR_FONT, POKE_FONT
from .util_tool import UtilTool
from back_end.controller import create_player, does_player_exist

class PokemonStat():
    def __init__(self, player_name, pokemon_list, pokemon, pokemon_enemy, screen, background, identification):
        """
        Initializes the Pokémon Statistics screen.
        Displays detailed attributes of a selected Pokémon.
        """
        self.player_name = player_name
        self.pokemon_list = pokemon_list
        self.pokemon = pokemon
        self.pokemon_enemy = pokemon_enemy
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.util = UtilTool()
        self.background = background
        self.identification = identification
        
        self.selected_index = 0
        self.running = True

    def display(self):
        """
        Main loop for the statistics display screen.
        Renders the Pokémon sprite and its numerical attributes.
        """
        while self.running:
            self.screen.update()
            # Set the background image/video
            self.screen.set_background_display(self.background)
            # Apply a semi-transparent filter for better text readability
            self.util.draw_color_filter(self.screen)

            y_position = self.screen.height // 2

            # Load and scale the Pokémon sprite
            image = pygame.transform.scale(
                pygame.image.load(self.pokemon.get_image()), 
                (self.screen.height // 3, self.screen.height // 3)
            )
            image_rect = image.get_rect(center=(self.screen.width // 4, self.screen.height // 2))
            self.screen.display.blit(image, image_rect)
            
            font_size = self.screen.width // 30

            # Render Pokémon species name in uppercase (e.g., PIKACHU)
            self.util.draw_text(self.pokemon.name.upper(), POKE_FONT, font_size, self.screen, (self.screen.width // 2, y_position - 175), "white")

            # Extract the primary pet name
            pet_name_list = self.pokemon.pet_name.split()
            pet_name = pet_name_list[0]

            # Render detailed stats list
            self.util.draw_text(f"{pet_name}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position - 125), "white")
            self.util.draw_text(f"Level : {self.pokemon.get_level()}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position - 75), "white")
            self.util.draw_text(f"Type : {', '.join(self.pokemon.type)}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position - 25), "white")
            self.util.draw_text(f"HP : {self.pokemon.get_hp()}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position + 25), "white")
            
            self.util.draw_text(f"Strength : {self.pokemon.get_strength()}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position + 75), "white")
            self.util.draw_text(f"Defense : {self.pokemon.get_defense()}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position + 125), "white")
            self.util.draw_text(f"Speed : {self.pokemon.get_speed()}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position + 175), "white")
            self.util.draw_text(f"XP : {self.pokemon.get_xp()}", REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, y_position + 225), "white")
            
            pygame.display.flip()

            # Input Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    # Confirm selection and create player if they don't exist yet
                    if event.key == pygame.K_RETURN:
                        if not does_player_exist(self.player_name):
                            create_player(self.player_name, self.pokemon)
                        return
                    
                    # Return to previous screen
                    elif event.key == pygame.K_ESCAPE:
                        return