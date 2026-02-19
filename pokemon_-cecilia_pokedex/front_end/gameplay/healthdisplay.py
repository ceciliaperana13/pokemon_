import pygame
from __settings__ import DARK_GREEN, LIGHT_GREEN, REGULAR_FONT, LIGHT_RED
from front_end.menu.util_tool import UtilTool

class HealthDisplay():
    def __init__(self):
        """
        Initializes the HealthDisplay utility using common UI tools.
        """
        self.util = UtilTool()

    def draw_health_bar(self, x, y, pokemon, hp_max, screen, my_center, who_is_displayed="player"):
        """
        Draws a stylized health bar container including name, level, and HP status.
        
        :param hp_max: Used to calculate the current ratio if scaling is needed.
        :param my_center: Coordinates for the center of the health display box.
        :param who_is_displayed: "player" or "enemy" (affects bar alignment).
        """
        # Define the dimensions of the health UI box
        width = screen.width // 4
        height = screen.height // 10
        healthbar_width = width - 20
        
        # Calculate HP ratio for the visual bar length
        if hp_max == pokemon.get_hp_max():
            hp_ratio = healthbar_width * (pokemon.get_hp() / pokemon.get_hp_max())
        else:
            # Adjustment logic if the provided hp_max differs from the object's max HP
            actual_hp = pokemon.get_hp() + (pokemon.get_hp_max() - hp_max)
            hp_ratio = healthbar_width * (actual_hp / pokemon.get_hp_max())
            
        # Ensure the bar doesn't go negative
        if pokemon.get_hp() <= 0:
            hp_ratio = 0

        # Draw the background window/container
        self.util.draw_small_window_with_background(screen, width, height, my_center)

        font_size = screen.height // 35
        # Clean the pet name (removing timestamp or UUID suffix if present)
        pet_name = pokemon.pet_name.split()[0]

        # Render Pokemon Species and Nickname
        self.util.draw_text_from_top_left(f"{pokemon.name} : {pet_name}", REGULAR_FONT,
                            font_size, screen,
                            ((my_center[0] - screen.width // 8.5), (my_center[1] - screen.height // 25)))
        
        # Render Level
        self.util.draw_text_from_top_left(f"lvl : {pokemon.get_level()}", REGULAR_FONT,
                            font_size, screen,
                            ((my_center[0] - screen.width // 8.5), (my_center[1] + screen.height // 50)))
        
        # Create a surface for the health bar with alpha transparency support
        window_surface = pygame.Surface((screen.width, screen.height), pygame.SRCALPHA)
        window_rect = window_surface.get_rect(center = (screen.width //2, screen.height // 2))

        # --- DRAWING THE BAR ---
        
        # 1. Background (The 'Empty' part of the bar - Light Red)
        health_bar_background = pygame.rect.Rect(0, 0, healthbar_width, 18)
        health_bar_background.midleft = (my_center[0] - healthbar_width // 2, my_center[1] + 3)
        pygame.draw.rect(window_surface, LIGHT_RED, health_bar_background, border_radius=10)       
        
        # 2. Actual Health (The 'Filled' part - Light Green)
        health_bar_actual = pygame.rect.Rect(0, 0, hp_ratio, 18)
        
        # Enemies usually have their bars fill from right to left or mirrored
        if who_is_displayed == "enemy":
            health_bar_actual.midright = (my_center[0] + healthbar_width // 2, my_center[1] + 3)
        else:
            health_bar_actual.midleft = (my_center[0] - healthbar_width // 2, my_center[1] + 3)

        pygame.draw.rect(window_surface, LIGHT_GREEN, health_bar_actual, border_radius=10)
        
        # 3. Border (Dark Green outline)
        pygame.draw.rect(window_surface, DARK_GREEN, health_bar_background, 3, border_radius=10)

        # Apply the health bar surface to the main display
        screen.display.blit(window_surface, window_rect)

        # Render numeric HP values (e.g., "50 / 100") at the bottom right of the box
        if hp_max == pokemon.get_hp_max():
            display_hp = pokemon.get_hp()
        else:
            display_hp = actual_hp
            
        self.util.draw_text_from_bottom_right(f"{display_hp} / {pokemon.get_hp_max()}", REGULAR_FONT,
                                font_size, screen,
                                ((my_center[0] + screen.width // 8.75), (my_center[1] + screen.height // 21)))