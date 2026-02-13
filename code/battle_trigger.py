import pygame
from typing import Callable, Optional


class BattleTrigger:
    """Gère les zones de déclenchement de combat sur la carte."""
    
    def __init__(self, tile_x: int, tile_y: int, tile_size: int = 16):
        """
        Initialise un déclencheur de combat.
        
        Args:
            tile_x: Coordonnée X de la tuile (en tuiles)
            tile_y: Coordonnée Y de la tuile (en tuiles)
            tile_size: Taille d'une tuile en pixels (défaut: 16)
        """
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_size = tile_size
        
        # Zone de collision (en pixels)
        self.rect = pygame.Rect(
            tile_x * tile_size,
            tile_y * tile_size,
            tile_size,
            tile_size
        )
        
        self.triggered = False
        self.callback: Optional[Callable] = None
    
    def check_collision(self, player_hitbox: pygame.Rect) -> bool:
        """
        Vérifie si le joueur entre en collision avec la zone de combat.
        
        Args:
            player_hitbox: Hitbox du joueur
            
        Returns:
            True si collision détectée, False sinon
        """
        return self.rect.colliderect(player_hitbox)
    
    def set_callback(self, callback: Callable) -> None:
        """
        Définit la fonction à appeler lors du déclenchement.
        
        Args:
            callback: Fonction à exécuter lors du combat
        """
        self.callback = callback
    
    def trigger(self) -> None:
        """Déclenche le combat si un callback est défini."""
        if self.callback and not self.triggered:
            self.triggered = True
            self.callback()
    
    def reset(self) -> None:
        """Réinitialise le déclencheur (permet de re-déclencher le combat)."""
        self.triggered = False