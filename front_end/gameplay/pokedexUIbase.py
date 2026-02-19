import pygame
import os

# ══════════════════════════════════════════════════════════════════════════════
#  Color Constants and Types — Shared across all UI classes
# ══════════════════════════════════════════════════════════════════════════════

COLORS = {
    'background':        (220, 220, 230),
    'pokemon_red':       (220,  30,  30),
    'dark_red':          (180,  20,  20),
    'white':             (255, 255, 255),
    'off_white':         (245, 245, 250),
    'black':             ( 40,  40,  50),
    'gray':              (150, 150, 160),
    'light_gray':        (200, 200, 210),
    'card':              (255, 255, 255),
    'card_hover':        (255, 245, 245),
    'card_selected':     (255, 230, 230),
    'shadow':            (180, 180, 190),
}

TYPE_COLORS = {
    'Fire':     (255,  68,  34),
    'Water':    ( 52, 152, 219),
    'Grass':    ( 46, 204, 113),
    'Electric': (241, 196,  15),
    'Psychic':  (155,  89, 182),
    'Fighting': (192,  57,  43),
    'Normal':   (149, 165, 166),
    'Flying':   (133, 193, 233),
    'Poison':   (142,  68, 173),
    'Ground':   (211,  84,   0),
    'Rock':     (120,  81,  45),
    'Bug':      (166, 187,   0),
    'Ghost':    ( 52,  73,  94),
    'Steel':    (120, 144, 156),
    'Ice':      (174, 214, 241),
    'Dragon':   (116, 125, 140),
    'Dark':     ( 44,  62,  80),
    'Fairy':    (253, 121, 168),
}


# ══════════════════════════════════════════════════════════════════════════════
#  Base Class — Common tools for all visual components
# ══════════════════════════════════════════════════════════════════════════════

class PokedexUIBase:
    """
    Base class providing:
      - Color dictionaries
      - Sprite loading and caching
      - Pokéball drawing (placeholder or 'not owned' icon)
      - Shared fonts
    """

    def __init__(self):
        self.colors       = COLORS
        self.type_colors  = TYPE_COLORS
        self.sprites_cache: dict = {}

        # Shared fonts (pygame must be initialized before this)
        self.font_title  = pygame.font.Font(None, 48)
        self.font_name   = pygame.font.Font(None, 32)
        self.font_info   = pygame.font.Font(None, 24)
        self.font_small  = pygame.font.Font(None, 20)

    # ── Sprites ──────────────────────────────────────────────────────────────

    def load_sprite(self, pokemon: dict):
        """
        Loads and caches a Pokémon's sprite.
        Returns a pygame Surface or None if not found.
        """
        pokemon_id = pokemon.get('id')
        if pokemon_id in self.sprites_cache:
            return self.sprites_cache[pokemon_id]

        # Try multiple path formats for compatibility
        base_path = pokemon.get('spritePokedex') or f"assets/imagePokedex/Spr_1b_{pokemon_id:03d}.png"
        paths = [
            base_path,
            f"assets/imagePokedex/Spr_1b_{pokemon_id:03d}.png",
            f"assets/imagePokedex/{pokemon_id:03d}.png",
            f"assets/imagePokedex/{pokemon_id}.png",
        ]

        sprite = None
        for p in paths:
            if os.path.exists(p):
                try:
                    sprite = pygame.image.load(p).convert_alpha()
                    break
                except pygame.error as e:
                    print(f"⚠ Sprite error at {p}: {e}")

        self.sprites_cache[pokemon_id] = sprite
        return sprite

    def draw_sprite(self, screen, pokemon: dict, x: int, y: int, max_size: int):
        """Draws the sprite centered at (x, y) within a max_size square."""
        sprite = self.load_sprite(pokemon)
        if sprite:
            w, h = sprite.get_size()
            ratio = min(max_size / w, max_size / h)
            scaled_sprite = pygame.transform.scale(sprite, (int(w * ratio), int(h * ratio)))
            screen.blit(scaled_sprite, scaled_sprite.get_rect(center=(x, y)))
        else:
            self._draw_pokeball_placeholder(screen, x, y)

    # ── Pokéball placeholder / 'not owned' icon ──────────────────────────────

    def _draw_pokeball_placeholder(self, screen, x: int, y: int, radius: int = 25):
        """Small grayed-out Pokéball (used when sprite is missing)."""
        self._draw_pokeball(screen, x, y, radius,
                           top_color=self.colors['light_gray'],
                           bottom_color=self.colors['white'])

    def draw_not_owned_pokeball(self, screen, x: int, y: int, radius: int = 32):
        """
        Large silhouette Pokéball for Pokémon not yet obtained.
        Displayed instead of the sprite and name.
        """
        self._draw_pokeball(screen, x, y, radius,
                           top_color=(180, 30, 30),
                           bottom_color=(230, 230, 230),
                           alpha=160)

    def _draw_pokeball(self, screen, x: int, y: int, radius: int,
                        top_color, bottom_color, alpha: int = 255):
        """Generic Pokéball drawing logic at (x, y)."""
        # Create a surface with transparency support
        surf = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
        cx = cy = radius + 2

        # Top half (Red/Gray circle)
        pygame.draw.circle(surf, (*top_color, alpha), (cx, cy), radius)
        # Bottom half (White rectangle covering the lower half of the circle)
        pygame.draw.rect(surf, (*bottom_color, alpha),
                         (0, cy, radius * 2 + 4, radius + 4))
        # White middle stripe to clean up the cut
        pygame.draw.rect(surf, (255, 255, 255, alpha),
                         (0, cy - 3, radius * 2 + 4, 6))
        # Outer border
        pygame.draw.circle(surf, (60, 60, 60, alpha), (cx, cy), radius, 2)
        # Horizontal middle line
        pygame.draw.line(surf, (60, 60, 60, alpha),
                         (0, cy), (radius * 2 + 4, cy), 2)
        # Central button
        pygame.draw.circle(surf, (255, 255, 255, alpha), (cx, cy), radius // 4 + 2)
        pygame.draw.circle(surf, (60, 60, 60, alpha), (cx, cy), radius // 4 + 2, 2)

        screen.blit(surf, surf.get_rect(center=(x, y)))

    # ── Drawing Utilities ─────────────────────────────────────────────────────

    def get_type_color(self, pokemon_type: str):
        """Returns the color associated with a Pokémon type (with fallback)."""
        return self.type_colors.get(pokemon_type.capitalize(), (100, 100, 100))

    def get_stat_color(self, percentage: float):
        """Returns Red/Orange/Green based on the stat value (0.0 to 1.0)."""
        if percentage < 0.33:
            return (255, 150, 150) # Weak
        if percentage < 0.66:
            return (255, 200, 100) # Average
        return (100, 220, 100)     # Strong