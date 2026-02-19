import pygame

"""
Utility class to handle sprite manipulations.
"""
class Tool:
    @staticmethod  # Static method: no need to pass 'self' as an argument
    def split_image(spritsheet: pygame.Surface, x: int, y: int, width: int, height: int):
        """
        Extracts a specific portion of a spritesheet (a subsurface).
        """
        return spritsheet.subsurface(pygame.Rect(x, y, width, height))