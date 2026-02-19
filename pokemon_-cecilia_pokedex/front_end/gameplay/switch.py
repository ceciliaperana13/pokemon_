import pygame

class Switch:
    def __init__(self, type: str, name: str, hitbox: pygame.Rect, port: int):
        """
        Initializes a world switch (trigger zone).
        
        Args:
            type (str): The category of the switch (e.g., 'teleport', 'event').
            name (str): The unique identifier for this trigger.
            hitbox (pygame.Rect): The rectangular area that triggers the switch.
            port (int): The destination or ID associated with this switch.
        """
        self.type = type
        self.name = name
        self.hitbox = hitbox
        self.port = port

    def check_collision(self, temp_hitbox):
        """
        Detects if the player's hitbox overlaps with the switch area.
        
        Args:
            temp_hitbox (pygame.Rect): The hitbox to check against (usually the player).
            
        Returns:
            bool: True if a collision is detected, False otherwise.
        """
        return self.hitbox.colliderect(temp_hitbox)