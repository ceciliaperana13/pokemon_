import pygame
import os
from .pokedexUIbase import PokedexUIBase


class PokedexButton(PokedexUIBase):
    """
    Button used to open/close the Pokédex.
    Inherits from PokedexUIBase for shared colors and fallback Pokéball drawing.
    """

    def __init__(self, x: int, y: int,
                 image_path: str = "assets/logo/pokedex.png",
                 size: int = 100):
        super().__init__()

        self.x, self.y = x, y
        self.size = size
        self.hovered = False
        self.is_clicked = False
        self.animation_time = 0
        self.pulse_amplitude = 5

        # ── Image Loading ─────────────────────────────────────────────────────
        self.original_image = self._load_image(image_path)

        self.normal_image = None
        self.hover_image  = None
        self.clicked_image = None

        if self.original_image:
            self._prepare_variants()

        # Collision Rectangle
        self.rect = pygame.Rect(x, y, size, size)

        # Optional Sound
        self.click_sound = None
        try:
            sound_path = "assets/sounds/pokedex_open.wav"
            if os.path.exists(sound_path):
                self.click_sound = pygame.mixer.Sound(sound_path)
        except Exception:
            pass

    # ── Initialization ────────────────────────────────────────────────────────

    @staticmethod
    def _load_image(image_path: str):
        """Tries several paths and returns the Surface or None."""
        candidates = [
            image_path,
            "assets/logo/pokedex.png",
            "assets/logo/pokedex.jpg",
            "assets/logo/Pokedex.png",
            "assets/logo/POKEDEX.png",
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    print(f"✓ Pokédex Button loaded: {path}")
                    return img
                except pygame.error as e:
                    print(f"⚠ Error {path}: {e}")
        print("⚠ Button image not found, using default fallback")
        return None

    def _prepare_variants(self):
        """Creates normal, hover, and clicked versions of the button image."""
        s = self.size
        self.normal_image = pygame.transform.smoothscale(self.original_image, (s, s))

        # Hover state: +10% size and slightly brighter
        hover_size = int(s * 1.1)
        hover_img = pygame.transform.smoothscale(self.original_image, (hover_size, hover_size)).copy()
        overlay = pygame.Surface((hover_size, hover_size))
        overlay.fill((50, 50, 50))
        hover_img.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.hover_image = hover_img

        # Clicked state: -5% size
        clicked_size = int(s * 0.95)
        self.clicked_image = pygame.transform.smoothscale(self.original_image, (clicked_size, clicked_size))

    # ── Logic Updates ─────────────────────────────────────────────────────────

    def update(self, dt: int = 1):
        """Updates animation timers."""
        self.animation_time += dt

    # ── Input Handling ────────────────────────────────────────────────────────

    def check_hover(self, pos) -> bool:
        """Checks if the mouse is hovering over the button."""
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def check_click(self, pos) -> bool:
        """Checks if the button was clicked and plays feedback sound."""
        if self.rect.collidepoint(pos):
            self.is_clicked = True
            if self.click_sound:
                self.click_sound.play()
            return True
        return False

    # ── Rendering ─────────────────────────────────────────────────────────────

    def draw(self, screen):
        """Main draw call; chooses between image or fallback vector drawing."""
        if self.normal_image:
            self._draw_with_image(screen)
        else:
            self._draw_fallback(screen)
        # Reset click state after drawing one frame
        self.is_clicked = False

    def _draw_with_image(self, screen):
        """Renders the button using the prepared sprites with animation effects."""
        if self.is_clicked and self.clicked_image:
            image = self.clicked_image
            offset_x = (self.size - image.get_width()) // 2
            offset_y = (self.size - image.get_height()) // 2 + 2
        elif self.hovered and self.hover_image:
            image = self.hover_image
            offset_x = (self.size - image.get_width()) // 2
            offset_y = (self.size - image.get_height()) // 2
            # Floating/Pulsing effect while hovering
            pulse = abs((self.animation_time % 60) - 30) / 30.0
            offset_y -= int(pulse * self.pulse_amplitude)
        else:
            image, offset_x, offset_y = self.normal_image, 0, 0

        # Draw Shadow (not when clicked for a 'pressed' effect)
        if not self.is_clicked:
            shadow = pygame.Surface((self.size + 10, self.size + 10))
            shadow.set_alpha(100)
            shadow.fill((0, 0, 0))
            screen.blit(shadow, (self.x - 5, self.y + 5))

        screen.blit(image, (self.x + offset_x, self.y + offset_y))

        # Hover Glow Effect
        if self.hovered:
            halo = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(halo, (255, 255, 255, 30),
                               (self.size // 2, self.size // 2), self.size // 2)
            screen.blit(halo, (self.x, self.y))

    def _draw_fallback(self, screen):
        """Renders a vector-based Pokéball if the button image file is missing."""
        if self.is_clicked:
            radius, color = self.size // 2 - 2, (180, 20, 20)
        elif self.hovered:
            radius, color = self.size // 2 + 3, (255, 50, 50)
        else:
            radius, color = self.size // 2, (220, 30, 30)

        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        # Draw background shadow circle
        pygame.draw.circle(screen, (0, 0, 0), (center_x + 3, center_y + 3), radius)
        
        # Use the inherited drawing method for the Pokéball base
        self.draw_not_owned_pokeball(screen, center_x, center_y, radius)

        # Draw a central "P" for Pokedex
        font = pygame.font.Font(None, int(self.size * 0.5))
        text = font.render("P", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(center_x, center_y)))