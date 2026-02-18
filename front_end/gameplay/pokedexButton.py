import pygame
import os
from .pokedexUIbase import PokedexUIBase


class PokedexButton(PokedexUIBase):
    """
    Bouton pour ouvrir/fermer le Pokédex.
    Hérite de PokedexUIBase pour les couleurs et la Pokéball de fallback.
    """

    def __init__(self, x: int, y: int,
                 image_path: str = "assets/logo/pokedex.png",
                 taille: int = 100):
        super().__init__()

        self.x, self.y   = x, y
        self.taille       = taille
        self.survol       = False
        self.est_clique   = False
        self.temps_animation = 0
        self.pulse_amplitude = 5

        # ── Chargement de l'image ─────────────────────────────────────────
        self.image_originale = self._charger_image(image_path)

        self.image_normale = None
        self.image_survol  = None
        self.image_clique  = None

        if self.image_originale:
            self._preparer_variantes()

        # Rectangle de collision
        self.rect = pygame.Rect(x, y, taille, taille)

        # Son optionnel
        self.son_clic = None
        try:
            chemin_son = "assets/sounds/pokedex_open.wav"
            if os.path.exists(chemin_son):
                self.son_clic = pygame.mixer.Sound(chemin_son)
        except Exception:
            pass

    # ── Initialisation ────────────────────────────────────────────────────────

    @staticmethod
    def _charger_image(image_path: str):
        """Essaie plusieurs chemins et retourne la Surface ou None."""
        candidats = [
            image_path,
            "assets/logo/pokedex.png",
            "assets/logo/pokedex.jpg",
            "assets/logo/Pokedex.png",
            "assets/logo/POKEDEX.png",
        ]
        for chemin in candidats:
            if os.path.exists(chemin):
                try:
                    img = pygame.image.load(chemin).convert_alpha()
                    print(f"✓ Bouton Pokédex chargé : {chemin}")
                    return img
                except pygame.error as e:
                    print(f"⚠ Erreur {chemin}: {e}")
        print("⚠ Image du bouton non trouvée, utilisation du bouton par défaut")
        return None

    def _preparer_variantes(self):
        """Crée les versions normale, survol et cliquée de l'image."""
        t = self.taille
        self.image_normale = pygame.transform.smoothscale(self.image_originale, (t, t))

        # Survol : +10 %, légèrement plus lumineuse
        ts = int(t * 1.1)
        survol = pygame.transform.smoothscale(self.image_originale, (ts, ts)).copy()
        overlay = pygame.Surface((ts, ts))
        overlay.fill((50, 50, 50))
        survol.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.image_survol = survol

        # Cliqué : -5 %
        tc = int(t * 0.95)
        self.image_clique = pygame.transform.smoothscale(self.image_originale, (tc, tc))

    # ── Mise à jour ───────────────────────────────────────────────────────────

    def update(self, dt: int = 1):
        self.temps_animation += dt

    # ── Événements souris ─────────────────────────────────────────────────────

    def verifier_survol(self, pos) -> bool:
        self.survol = self.rect.collidepoint(pos)
        return self.survol

    def verifier_clic(self, pos) -> bool:
        if self.rect.collidepoint(pos):
            self.est_clique = True
            if self.son_clic:
                self.son_clic.play()
            return True
        return False

    # ── Dessin ────────────────────────────────────────────────────────────────

    def dessiner(self, screen):
        if self.image_normale:
            self._dessiner_avec_image(screen)
        else:
            self._dessiner_fallback(screen)
        self.est_clique = False

    def _dessiner_avec_image(self, screen):
        if self.est_clique and self.image_clique:
            image   = self.image_clique
            ox = (self.taille - image.get_width())  // 2
            oy = (self.taille - image.get_height()) // 2 + 2
        elif self.survol and self.image_survol:
            image   = self.image_survol
            ox = (self.taille - image.get_width())  // 2
            oy = (self.taille - image.get_height()) // 2
            # Pulsation verticale
            pulse = abs((self.temps_animation % 60) - 30) / 30.0
            oy   -= int(pulse * self.pulse_amplitude)
        else:
            image, ox, oy = self.image_normale, 0, 0

        # Ombre
        if not self.est_clique:
            ombre = pygame.Surface((self.taille + 10, self.taille + 10))
            ombre.set_alpha(100)
            ombre.fill((0, 0, 0))
            screen.blit(ombre, (self.x - 5, self.y + 5))

        screen.blit(image, (self.x + ox, self.y + oy))

        # Halo de survol
        if self.survol:
            halo = pygame.Surface((self.taille, self.taille), pygame.SRCALPHA)
            pygame.draw.circle(halo, (255, 255, 255, 30),
                               (self.taille // 2, self.taille // 2), self.taille // 2)
            screen.blit(halo, (self.x, self.y))

    def _dessiner_fallback(self, screen):
        """Pokéball vectorielle si aucune image n'est disponible."""
        if self.est_clique:
            rayon, couleur = self.taille // 2 - 2, (180, 20, 20)
        elif self.survol:
            rayon, couleur = self.taille // 2 + 3, (255, 50, 50)
        else:
            rayon, couleur = self.taille // 2, (220, 30, 30)

        cx = self.x + self.taille // 2
        cy = self.y + self.taille // 2

        # Ombre
        pygame.draw.circle(screen, (0, 0, 0), (cx + 3, cy + 3), rayon)
        # Corps principal — réutilise la méthode héritée
        self.dessiner_pokeball_non_possede(screen, cx, cy, rayon)

        # Lettre "P" centrale
        font = pygame.font.Font(None, int(self.taille * 0.5))
        txt  = font.render("P", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(cx, cy)))