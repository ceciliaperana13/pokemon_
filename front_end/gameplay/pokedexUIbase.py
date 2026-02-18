import pygame
import os


# ══════════════════════════════════════════════════════════════════════════════
#  Constantes de couleurs et de types — partagées par toutes les classes UI
# ══════════════════════════════════════════════════════════════════════════════

COULEURS = {
    'fond':              (220, 220, 230),
    'rouge_pokemon':     (220,  30,  30),
    'rouge_fonce':       (180,  20,  20),
    'blanc':             (255, 255, 255),
    'blanc_casse':       (245, 245, 250),
    'noir':              ( 40,  40,  50),
    'gris':              (150, 150, 160),
    'gris_clair':        (200, 200, 210),
    'carte':             (255, 255, 255),
    'carte_survol':      (255, 245, 245),
    'carte_selectionnee':(255, 230, 230),
    'ombre':             (180, 180, 190),
}

COULEURS_TYPES = {
    'Feu':      (255,  68,  34),
    'Eau':      ( 52, 152, 219),
    'Plante':   ( 46, 204, 113),
    'Electrik': (241, 196,  15),
    'Psy':      (155,  89, 182),
    'Combat':   (192,  57,  43),
    'Normal':   (149, 165, 166),
    'Vol':      (133, 193, 233),
    'Poison':   (142,  68, 173),
    'Sol':      (211,  84,   0),
    'Roche':    (120,  81,  45),
    'Insecte':  (166, 187,   0),
    'Spectre':  ( 52,  73,  94),
    'Acier':    (120, 144, 156),
    'Glace':    (174, 214, 241),
    'Dragon':   (116, 125, 140),
    'Ténèbres': ( 44,  62,  80),
    'Fée':      (253, 121, 168),
}


# ══════════════════════════════════════════════════════════════════════════════
#  Classe de base — outillage commun à tous les composants visuels
# ══════════════════════════════════════════════════════════════════════════════

class PokedexUIBase:
    """
    Classe de base qui regroupe :
      - les dictionnaires de couleurs
      - le chargement / dessin de sprites
      - le dessin d'une Pokéball (placeholder ou icône « non possédé »)
      - les polices partagées
    """

    def __init__(self):
        self.couleurs       = COULEURS
        self.couleurs_types = COULEURS_TYPES
        self.sprites_cache: dict = {}

        # Polices partagées (pygame doit déjà être initialisé)
        self.font_titre = pygame.font.Font(None, 48)
        self.font_nom   = pygame.font.Font(None, 32)
        self.font_info  = pygame.font.Font(None, 24)
        self.font_petit = pygame.font.Font(None, 20)

    # ── Sprites ──────────────────────────────────────────────────────────────

    def charger_sprite(self, pokemon: dict):
        """
        Charge et met en cache le sprite d'un Pokémon.
        Retourne une Surface pygame ou None si introuvable.
        """
        pokemon_id = pokemon.get('id')
        if pokemon_id in self.sprites_cache:
            return self.sprites_cache[pokemon_id]

        chemin = pokemon.get('spritePokedex') or f"assets/imagePokedex/Spr_1b_{pokemon_id:03d}.png"
        chemins = [
            chemin,
            f"assets/imagePokedex/Spr_1b_{pokemon_id:03d}.png",
            f"assets/imagePokedex/{pokemon_id:03d}.png",
            f"assets/imagePokedex/{pokemon_id}.png",
        ]

        sprite = None
        for c in chemins:
            if os.path.exists(c):
                try:
                    sprite = pygame.image.load(c).convert_alpha()
                    break
                except pygame.error as e:
                    print(f"⚠ Erreur sprite {c}: {e}")

        self.sprites_cache[pokemon_id] = sprite
        return sprite

    def dessiner_sprite(self, screen, pokemon: dict, x: int, y: int, taille_max: int):
        """Dessine le sprite centré en (x, y) dans un carré taille_max×taille_max."""
        sprite = self.charger_sprite(pokemon)
        if sprite:
            w, h = sprite.get_size()
            ratio = min(taille_max / w, taille_max / h)
            sprite_scaled = pygame.transform.scale(sprite, (int(w * ratio), int(h * ratio)))
            screen.blit(sprite_scaled, sprite_scaled.get_rect(center=(x, y)))
        else:
            self._dessiner_pokeball_placeholder(screen, x, y)

    # ── Pokéball placeholder / icône non-possédé ──────────────────────────────

    def _dessiner_pokeball_placeholder(self, screen, x: int, y: int, rayon: int = 25):
        """Petite Pokéball grisée (utilisée quand le sprite est absent)."""
        self._dessiner_pokeball(screen, x, y, rayon,
                                couleur_haut=self.couleurs['gris_clair'],
                                couleur_bas=self.couleurs['blanc'])

    def dessiner_pokeball_non_possede(self, screen, x: int, y: int, rayon: int = 32):
        """
        Grande Pokéball silhouette pour les Pokémon non encore obtenus.
        Affichée à la place du sprite + nom.
        """
        self._dessiner_pokeball(screen, x, y, rayon,
                                couleur_haut=(180, 30, 30),
                                couleur_bas=(230, 230, 230),
                                alpha=160)

    def _dessiner_pokeball(self, screen, x: int, y: int, rayon: int,
                           couleur_haut, couleur_bas, alpha: int = 255):
        """Dessin générique d'une Pokéball à (x, y)."""
        surf = pygame.Surface((rayon * 2 + 4, rayon * 2 + 4), pygame.SRCALPHA)
        cx = cy = rayon + 2

        # Demi-sphère supérieure
        pygame.draw.circle(surf, (*couleur_haut, alpha), (cx, cy), rayon)
        # Demi-sphère inférieure (rectangle blanc qui couvre la moitié basse)
        pygame.draw.rect(surf, (*couleur_bas, alpha),
                         (0, cy, rayon * 2 + 4, rayon + 4))
        # Rebord blanc pour rendre la coupure nette
        pygame.draw.rect(surf, (255, 255, 255, alpha),
                         (0, cy - 3, rayon * 2 + 4, 6))
        # Contour
        pygame.draw.circle(surf, (60, 60, 60, alpha), (cx, cy), rayon, 2)
        # Ligne horizontale centrale
        pygame.draw.line(surf, (60, 60, 60, alpha),
                         (0, cy), (rayon * 2 + 4, cy), 2)
        # Cercle central
        pygame.draw.circle(surf, (255, 255, 255, alpha), (cx, cy), rayon // 4 + 2)
        pygame.draw.circle(surf, (60, 60, 60, alpha), (cx, cy), rayon // 4 + 2, 2)

        screen.blit(surf, surf.get_rect(center=(x, y)))

    # ── Utilitaires de dessin ─────────────────────────────────────────────────

    def couleur_type(self, type_pokemon: str):
        """Retourne la couleur associée à un type (avec fallback)."""
        return self.couleurs_types.get(type_pokemon.capitalize(), (100, 100, 100))

    def couleur_stat(self, pourcentage: float):
        """Retourne rouge/orange/vert selon la valeur de la stat (0-1)."""
        if pourcentage < 0.33:
            return (255, 150, 150)
        if pourcentage < 0.66:
            return (255, 200, 100)
        return (100, 220, 100)