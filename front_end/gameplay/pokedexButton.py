import pygame
import os


class PokedexButton:
    """Bouton pour ouvrir/fermer le Pokédex avec image personnalisée"""
    
    def __init__(self, x, y, image_path="assets/logo/pokedex.png", taille=100):
        """
        Initialise le bouton Pokédex
        
        Args:
            x (int): Position X du bouton
            y (int): Position Y du bouton
            image_path (str): Chemin vers l'image du bouton
            taille (int): Taille du bouton (largeur et hauteur)
        """
        self.x = x
        self.y = y
        self.taille = taille
        self.image_originale = None
        self.image_normale = None
        self.image_survol = None
        self.image_clique = None
        self.survol = False
        self.est_clique = False
        
        # Essayer différentes extensions si le fichier n'existe pas
        chemins_possibles = [
            image_path,
            "assets/logo/pokedex.png",
            "assets/logo/pokedex.jpg",
            "assets/logo/Pokedex.png",
            "assets/logo/POKEDEX.png",
        ]
        
        image_chargee = False
        for chemin in chemins_possibles:
            if os.path.exists(chemin):
                try:
                    self.image_originale = pygame.image.load(chemin).convert_alpha()
                    print(f"✓ Bouton Pokédex chargé : {chemin}")
                    image_chargee = True
                    break
                except pygame.error as e:
                    print(f"⚠ Erreur lors du chargement de {chemin}: {e}")
        
        if not image_chargee:
            print(f"⚠ Image du bouton non trouvée, utilisation du bouton par défaut")
            self.image_originale = None
        
        # Préparer les différentes versions de l'image
        if self.image_originale:
            # Redimensionner l'image
            self.image_normale = pygame.transform.smoothscale(
                self.image_originale, 
                (taille, taille)
            )
            
            # Version survol (légèrement plus grande et plus lumineuse)
            taille_survol = int(taille * 1.1)
            self.image_survol = pygame.transform.smoothscale(
                self.image_originale, 
                (taille_survol, taille_survol)
            )
            # Ajouter un effet de luminosité
            self.image_survol = self.image_survol.copy()
            overlay = pygame.Surface((taille_survol, taille_survol))
            overlay.fill((50, 50, 50))
            self.image_survol.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            
            # Version cliquée (légèrement plus petite)
            taille_clique = int(taille * 0.95)
            self.image_clique = pygame.transform.smoothscale(
                self.image_originale, 
                (taille_clique, taille_clique)
            )
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, taille, taille)
        
        # Animation de pulsation
        self.temps_animation = 0
        self.pulse_amplitude = 5
        
        # Son (optionnel)
        self.son_clic = None
        try:
            # Essayer de charger un son si disponible
            if os.path.exists("assets/sounds/pokedex_open.wav"):
                self.son_clic = pygame.mixer.Sound("assets/sounds/pokedex_open.wav")
        except:
            pass
    
    def update(self, dt=1):
        """
        Met à jour l'animation du bouton
        
        Args:
            dt: Delta time pour l'animation
        """
        self.temps_animation += dt
    
    def verifier_survol(self, pos):
        """
        Vérifie si la souris survole le bouton
        
        Args:
            pos (tuple): Position (x, y) de la souris
        
        Returns:
            bool: True si la souris survole le bouton
        """
        self.survol = self.rect.collidepoint(pos)
        return self.survol
    
    def verifier_clic(self, pos):
        """
        Vérifie si le bouton a été cliqué
        
        Args:
            pos (tuple): Position (x, y) du clic
        
        Returns:
            bool: True si le bouton a été cliqué
        """
        if self.rect.collidepoint(pos):
            self.est_clique = True
            
            # Jouer le son
            if self.son_clic:
                self.son_clic.play()
            
            return True
        return False
    
    def dessiner(self, screen):
        """
        Dessine le bouton sur l'écran
        
        Args:
            screen: Surface pygame où dessiner
        """
        if self.image_normale:
            self._dessiner_avec_image(screen)
        else:
            self._dessiner_fallback(screen)
        
        # Reset du clic
        self.est_clique = False
    
    def _dessiner_avec_image(self, screen):
        """Dessine le bouton avec l'image chargée"""
        # Choisir l'image selon l'état
        if self.est_clique and self.image_clique:
            image = self.image_clique
            offset_x = (self.taille - self.image_clique.get_width()) // 2
            offset_y = (self.taille - self.image_clique.get_height()) // 2 + 2
        elif self.survol and self.image_survol:
            image = self.image_survol
            offset_x = (self.taille - self.image_survol.get_width()) // 2
            offset_y = (self.taille - self.image_survol.get_height()) // 2
            
            # Effet de pulsation
            pulse = abs((self.temps_animation % 60) - 30) / 30.0
            offset_y -= int(pulse * self.pulse_amplitude)
        else:
            image = self.image_normale
            offset_x = 0
            offset_y = 0
        
        # Dessiner une ombre
        if not self.est_clique:
            ombre_surface = pygame.Surface((self.taille + 10, self.taille + 10))
            ombre_surface.set_alpha(100)
            ombre_surface.fill((0, 0, 0))
            screen.blit(ombre_surface, (self.x - 5, self.y + 5))
        
        # Dessiner l'image
        screen.blit(image, (self.x + offset_x, self.y + offset_y))
        
        # Effet de brillance si survol
        if self.survol:
            overlay = pygame.Surface((self.taille, self.taille), pygame.SRCALPHA)
            pygame.draw.circle(
                overlay, 
                (255, 255, 255, 30), 
                (self.taille // 2, self.taille // 2), 
                self.taille // 2
            )
            screen.blit(overlay, (self.x, self.y))
    
    def _dessiner_fallback(self, screen):
        """Dessine un bouton par défaut si l'image n'est pas disponible"""
        # Couleurs
        if self.est_clique:
            couleur = (180, 20, 20)
            rayon = self.taille // 2 - 2
        elif self.survol:
            couleur = (255, 50, 50)
            rayon = self.taille // 2 + 3
        else:
            couleur = (220, 30, 30)
            rayon = self.taille // 2
        
        centre_x = self.x + self.taille // 2
        centre_y = self.y + self.taille // 2
        
        # Ombre
        pygame.draw.circle(screen, (0, 0, 0), (centre_x + 3, centre_y + 3), rayon)
        
        # Cercle principal (style Pokéball)
        pygame.draw.circle(screen, couleur, (centre_x, centre_y), rayon)
        
        # Partie blanche
        pygame.draw.circle(screen, (255, 255, 255), (centre_x, centre_y), rayon - 10)
        
        # Cercle central
        pygame.draw.circle(screen, (40, 40, 40), (centre_x, centre_y), rayon // 3)
        pygame.draw.circle(screen, (255, 255, 255), (centre_x, centre_y), rayon // 3, 3)
        
        # Texte "P"
        font = pygame.font.Font(None, int(self.taille * 0.5))
        text = font.render("P", True, (255, 255, 255))
        text_rect = text.get_rect(center=(centre_x, centre_y))
        screen.blit(text, text_rect)