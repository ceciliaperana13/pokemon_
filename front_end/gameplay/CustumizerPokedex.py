import pygame
from .pokedexUIbase import PokedexUIBase

class CustomizerPokedex(PokedexUIBase):
    """
    Main Graphical Interface for the Pokedex.
    Inherits from PokedexUIBase for colors, sprites, and common utilities.
    """

    def __init__(self, pokedex, width: int, height: int):
        super().__init__()

        self.pokedex = pokedex
        self.width   = width
        self.height  = height

        # Interface State
        self.hover_index   = None
        self.scroll_offset = 0

        # Grid Layout Settings
        self.pokemon_per_row = 4
        self.card_size       = 180
        self.margin          = 25

    
    #  Main Entry Point
    

    def draw(self, screen):
        """Draws the complete Pokedex interface."""
        screen.fill(self.colors['background'])
        self._draw_header(screen)
        self._draw_grid(screen)
        
        # Display the side panel if a Pokemon is currently selected
        if self.pokedex.get_selected_pokemon():
            self._draw_details(screen)

    
    #  Header Section
    

    def _draw_header(self, screen):
        """Draws the top navigation bar with title and discovery counter."""
        red   = self.colors['pokemon_red']
        dark  = self.colors['dark_red']
        white = self.colors['white']

        # Header background and shadow line
        pygame.draw.rect(screen, red, (0, 0, self.width, 100))
        pygame.draw.rect(screen, dark, (0, 95, self.width, 5))

        # Left decorative Pokeball
        self.draw_not_owned_pokeball(screen, 80, 50, radius=35)

        # Status LED lights (Classic Pokedex aesthetic)
        for i, c in enumerate([dark, (255, 150, 150), (255, 100, 100)]):
            pygame.draw.circle(screen, c, (150 + i * 25, 50), 8)

        # Title and counter rendering
        screen.blit(self.font_title.render("POKÉDEX", True, white), (250, 35))
        found = self.pokedex.found_count()
        total = self.pokedex.total_count()
        counter = self.font_small.render(
            f"{found} / {total} Pokémon discovered", True, (255, 200, 200)
        )
        screen.blit(counter, (250, 70))

    
    #  Card Grid
    

    def _draw_grid(self, screen):
        """Calculates and renders the scrollable grid of Pokemon cards."""
        zone_y      = 120
        zone_h      = self.height - 140
        start_y     = zone_y + self.margin - self.scroll_offset

        for i, pokemon in enumerate(self.pokedex.get_all_pokemon()):
            col = i % self.pokemon_per_row
            row = i // self.pokemon_per_row
            
            x = self.margin + col * (self.card_size + self.margin)
            y = start_y + row * (self.card_size + self.margin)

            # Optimization: Skip drawing if the card is outside the visible area
            if y + self.card_size < zone_y or y > zone_y + zone_h:
                continue

            self._draw_pokemon_card(screen, pokemon, x, y, i)

    
    #  Individual Card Rendering
    

    def _draw_pokemon_card(self, screen, pokemon: dict, x: int, y: int, index: int):
        """Draws a single Pokemon card with its sprite or a placeholder."""
        selected_poke = self.pokedex.get_selected_pokemon()
        is_selected = selected_poke and selected_poke.get('id') == pokemon.get('id')
        is_owned = pokemon.get('stats', {}).get('found', False)

        # Determine card style based on state (selected, hovered, or normal)
        if is_selected:
            bg, border, thickness = self.colors['card_selected'], self.colors['pokemon_red'], 4
        elif self.hover_index == index:
            bg, border, thickness = self.colors['card_hover'], self.colors['pokemon_red'], 3
        else:
            bg, border, thickness = self.colors['card'], self.colors['light_gray'], 2

        # Draw drop shadow
        pygame.draw.rect(screen, self.colors['shadow'],
                         pygame.Rect(x + 5, y + 5, self.card_size, self.card_size),
                         border_radius=15)

        # Main Card Body
        rect = pygame.Rect(x, y, self.card_size, self.card_size)
        pygame.draw.rect(screen, bg, rect, border_radius=15)
        pygame.draw.rect(screen, border, rect, thickness, border_radius=15)

        # Top Red Header Strip
        strip = pygame.Rect(x + 10, y + 10, self.card_size - 20, 40)
        pygame.draw.rect(screen, self.colors['pokemon_red'], strip, border_radius=8)

        # Pokedex ID Number
        num_text = self.font_info.render(f"No. {pokemon.get('id', '?'):03d}", True, self.colors['white'])
        screen.blit(num_text, (x + 20, y + 20))

        # Image Frame
        img_rect = pygame.Rect(x + 15, y + 60, self.card_size - 30, 80)
        pygame.draw.rect(screen, self.colors['off_white'], img_rect, border_radius=10)
        pygame.draw.rect(screen, self.colors['light_gray'], img_rect, 2, border_radius=10)

        cx = x + self.card_size // 2
        cy = y + 100

        if is_owned:
            # Render Owned Pokemon: sprite, name, and type badges
            self.draw_sprite(screen, pokemon, cx, cy, 70)

            name_text = self.font_name.render(pokemon.get('name', 'Unknown'), True, self.colors['black'])
            screen.blit(name_text, name_text.get_rect(center=(cx, y + 155)))

            self._draw_type_badges(screen, pokemon.get('type', []),
                                   x + 20, y + 175, self.card_size - 40)
        else:
            # Render Unowned Pokemon: Placeholder icon and question marks
            self.draw_not_owned_pokeball(screen, cx, cy, radius=28)

            q_mark = self.font_name.render("???", True, self.colors['gray'])
            screen.blit(q_mark, q_mark.get_rect(center=(cx, y + 155)))

    
    #  Detail Panel (Right Side)
    

    def _draw_details(self, screen):
        """Renders the detailed info panel for the selected Pokemon."""
        pokemon = self.pokedex.get_selected_pokemon()
        if not pokemon: return

        is_owned = pokemon.get('stats', {}).get('found', False)
        panel_x, panel_y = self.width - 380, 120
        panel_w, panel_h = 360, self.height - 140

        # Panel Background, Shadow, and Border
        pygame.draw.rect(screen, self.colors['shadow'], (panel_x + 5, panel_y + 5, panel_w, panel_h), border_radius=20)
        pygame.draw.rect(screen, self.colors['white'], (panel_x, panel_y, panel_w, panel_h), border_radius=20)
        pygame.draw.rect(screen, self.colors['pokemon_red'], (panel_x, panel_y, panel_w, panel_h), 5, border_radius=20)

        # Header Decorative Strip
        pygame.draw.rect(screen, self.colors['pokemon_red'], (panel_x, panel_y, panel_w, 60), border_radius=20)
        pygame.draw.rect(screen, self.colors['white'], (panel_x, panel_y + 55, panel_w, 10))
        screen.blit(self.font_info.render("DETAILS", True, self.colors['white']), (panel_x + 20, panel_y + 15))

        y = panel_y + 80

        if is_owned:
            # Information for Discovered Pokemon
            screen.blit(self.font_title.render(pokemon.get('name', '?'), True, self.colors['pokemon_red']), (panel_x + 20, y))
            y += 50
            screen.blit(self.font_info.render(f"No. {pokemon.get('id', '?'):03d}", True, self.colors['gray']), (panel_x + 20, y))
            y += 35

            # Large Sprite Frame
            sprite_rect = pygame.Rect(panel_x + 20, y, panel_w - 40, 120)
            pygame.draw.rect(screen, self.colors['off_white'], sprite_rect, border_radius=15)
            pygame.draw.rect(screen, self.colors['light_gray'], sprite_rect, 2, border_radius=15)
            self.draw_sprite(screen, pokemon, panel_x + panel_w // 2, y + 60, 100)
            y += 135

            # Types Section
            screen.blit(self.font_info.render("TYPES", True, self.colors['black']), (panel_x + 20, y))
            y += 25
            y = self._draw_type_badges(screen, pokemon.get('type', []), panel_x + 20, y, 140, badge_h=30, return_y=True)
            y += 10

            # Stats Section
            screen.blit(self.font_info.render("BASE STATISTICS", True, self.colors['black']), (panel_x + 20, y))
            y += 30
            self._draw_stats(screen, pokemon.get('stats', {}), panel_x, y)
        else:
            # View for Undiscovered Pokemon
            self.draw_not_owned_pokeball(screen, panel_x + panel_w // 2, panel_y + panel_h // 2 - 60, radius=55)
            msg1 = self.font_name.render("??? Unknown ???", True, self.colors['gray'])
            msg2 = self.font_small.render("Discover this Pokemon to", True, self.colors['gray'])
            msg3 = self.font_small.render("reveal its information!", True, self.colors['gray'])
            mx, my = panel_x + panel_w // 2, panel_y + panel_h // 2 + 20
            screen.blit(msg1, msg1.get_rect(center=(mx, my))); my += 35
            screen.blit(msg2, msg2.get_rect(center=(mx, my))); my += 22
            screen.blit(msg3, msg3.get_rect(center=(mx, my)))

        self._draw_close_button(screen, panel_x, panel_y, panel_w, panel_h)

    
    #  Drawing Helpers
    

    def _draw_type_badges(self, screen, types, x: int, y: int, badge_w: int, badge_h: int = 28, return_y: bool = False):
        """Draws stylized type badges and optionally returns the final Y position."""
        if isinstance(types, str): types = [types]
        for t in types:
            t_norm = t.capitalize()
            rect = pygame.Rect(x, y, badge_w, badge_h)
            pygame.draw.rect(screen, self.get_type_color(t_norm), rect, border_radius=badge_h // 2)
            txt = self.font_info.render(t_norm.upper(), True, self.colors['white'])
            screen.blit(txt, txt.get_rect(center=rect.center))
            y += badge_h + 5
        return y if return_y else None

    def _draw_stats(self, screen, stats: dict, panel_x: int, y: int):
        """Renders the horizontal base stat bars (HP, ATK, DEF, SPD)."""
        mapping = {'hp': 'HP', 'attack': 'ATK', 'defense': 'DEF', 'speed': 'SPD'}
        bar_x, bar_w, bar_h = panel_x + 65, 200, 16

        for key in ('hp', 'attack', 'defense', 'speed'):
            if key not in stats or key == 'found': continue
            val = stats[key]
            screen.blit(self.font_small.render(mapping[key], True, self.colors['black']), (panel_x + 20, y))

            # Bar Background
            pygame.draw.rect(screen, self.colors['light_gray'], (bar_x, y, bar_w, bar_h), border_radius=8)
            # Fill Bar (Color varies based on value)
            pct = min(val / 200, 1.0)
            fill_w = int(bar_w * pct)
            if fill_w > 0:
                pygame.draw.rect(screen, self.get_stat_color(pct), (bar_x, y, fill_w, bar_h), border_radius=8)
            # Border
            pygame.draw.rect(screen, self.colors['gray'], (bar_x, y, bar_w, bar_h), 2, border_radius=8)
            # Numeric Label
            screen.blit(self.font_small.render(str(val), True, self.colors['pokemon_red']), (bar_x + bar_w + 8, y))
            y += 28

    def _draw_close_button(self, screen, panel_x, panel_y, panel_w, panel_h):
        """Draws a button to deselect the current Pokemon and close the panel."""
        btn_y = panel_y + panel_h - 60
        btn_rect = pygame.Rect(panel_x + 20, btn_y, panel_w - 40, 40)
        pygame.draw.rect(screen, self.colors['pokemon_red'], btn_rect, border_radius=20)
        txt = self.font_info.render("CLOSE", True, self.colors['white'])
        screen.blit(txt, txt.get_rect(center=btn_rect.center))

    
    #  Mouse Event Handling
    

    def check_click(self, pos):
        """Handles mouse clicks for card selection and the close button."""
        x, y = pos

        # Check Close Button
        if self.pokedex.get_selected_pokemon():
            panel_x, panel_y = self.width - 380, 120
            panel_w, panel_h = 360, self.height - 140
            btn_rect = pygame.Rect(panel_x + 20, panel_y + panel_h - 60, panel_w - 40, 40)
            if btn_rect.collidepoint(x, y):
                self.pokedex.deselect_pokemon()
                return

        # Check Grid Cards
        start_y = 120 + self.margin - self.scroll_offset
        for i, pokemon in enumerate(self.pokedex.get_all_pokemon()):
            cx = self.margin + (i % self.pokemon_per_row) * (self.card_size + self.margin)
            cy = start_y + (i // self.pokemon_per_row) * (self.card_size + self.margin)
            if pygame.Rect(cx, cy, self.card_size, self.card_size).collidepoint(x, y):
                self.pokedex.select_pokemon(pokemon)
                return

    def check_hover(self, pos):
        """Updates the card index currently under the mouse cursor."""
        x, y = pos
        start_y = 120 + self.margin - self.scroll_offset
        self.hover_index = None
        for i, _ in enumerate(self.pokedex.get_all_pokemon()):
            cx = self.margin + (i % self.pokemon_per_row) * (self.card_size + self.margin)
            cy = start_y + (i // self.pokemon_per_row) * (self.card_size + self.margin)
            if pygame.Rect(cx, cy, self.card_size, self.card_size).collidepoint(x, y):
                self.hover_index = i
                return

    def scroll(self, direction: int):
        """Adjusts the vertical scroll offset."""
        self.scroll_offset = max(0, self.scroll_offset + direction * 40)