import pygame
from .pokedexUIbase import PokedexUIBase


class CustomizerPokedex(PokedexUIBase):
    """
    Interface graphique principale du Pokédex.
    Hérite de PokedexUIBase pour les couleurs, sprites et utilitaires communs.
    """

    def __init__(self, pokedex, largeur: int, hauteur: int):
        super().__init__()

        self.pokedex  = pokedex
        self.largeur  = largeur
        self.hauteur  = hauteur

        # État de l'interface
        self.index_survol  = None
        self.scroll_offset = 0

        # Disposition de la grille
        self.pokemon_par_ligne = 4
        self.taille_carte      = 180
        self.marge             = 25

    
    #  Point d'entrée principal
    

    def dessiner(self, screen):
        """Dessine l'interface complète du Pokédex."""
        screen.fill(self.couleurs['fond'])
        self._dessiner_header(screen)
        self._dessiner_grille(screen)
        if self.pokedex.obtenir_pokemon_selectionne():
            self._dessiner_details(screen)

    
    #  En-tête
    

    def _dessiner_header(self, screen):
        rouge  = self.couleurs['rouge_pokemon']
        fonce  = self.couleurs['rouge_fonce']
        blanc  = self.couleurs['blanc']
        noir   = self.couleurs['noir']

        pygame.draw.rect(screen, rouge, (0, 0, self.largeur, 100))
        pygame.draw.rect(screen, fonce, (0, 95, self.largeur, 5))

        # Pokéball décorative gauche
        self.dessiner_pokeball_non_possede(screen, 80, 50, rayon=35)

        # Petits voyants
        for i, c in enumerate([fonce, (255, 150, 150), (255, 100, 100)]):
            pygame.draw.circle(screen, c, (150 + i * 25, 50), 8)

        # Titre + compteur
        screen.blit(self.font_titre.render("POKÉDEX", True, blanc), (250, 35))
        trouves  = self.pokedex.nombre_pokemon_trouves()
        total    = self.pokedex.nombre_pokemon()
        compteur = self.font_petit.render(
            f"{trouves} / {total} Pokémon découverts", True, (255, 200, 200)
        )
        screen.blit(compteur, (250, 70))

    
    #  Grille de cartes
    

    def _dessiner_grille(self, screen):
        zone_y      = 120
        zone_h      = self.hauteur - 140
        y_depart    = zone_y + self.marge - self.scroll_offset

        for i, pokemon in enumerate(self.pokedex.obtenir_tous_les_pokemon()):
            col = i % self.pokemon_par_ligne
            lig = i // self.pokemon_par_ligne
            x = self.marge + col * (self.taille_carte + self.marge)
            y = y_depart + lig * (self.taille_carte + self.marge)

            if y + self.taille_carte < zone_y or y > zone_y + zone_h:
                continue  # hors de la zone visible

            self._dessiner_carte_pokemon(screen, pokemon, x, y, i)

    
    #  Carte individuelle
    

    def _dessiner_carte_pokemon(self, screen, pokemon: dict, x: int, y: int, index: int):
        pokemon_sel = self.pokedex.obtenir_pokemon_selectionne()
        est_selectionne = pokemon_sel and pokemon_sel.get('id') == pokemon.get('id')
        est_possede = pokemon.get('stats', {}).get('found', False)

        # Couleurs de la carte
        if est_selectionne:
            fond, bordure, ep = self.couleurs['carte_selectionnee'], self.couleurs['rouge_pokemon'], 4
        elif self.index_survol == index:
            fond, bordure, ep = self.couleurs['carte_survol'], self.couleurs['rouge_pokemon'], 3
        else:
            fond, bordure, ep = self.couleurs['carte'], self.couleurs['gris_clair'], 2

        # Ombre
        pygame.draw.rect(screen, self.couleurs['ombre'],
                         pygame.Rect(x + 5, y + 5, self.taille_carte, self.taille_carte),
                         border_radius=15)

        # Corps de la carte
        rect = pygame.Rect(x, y, self.taille_carte, self.taille_carte)
        pygame.draw.rect(screen, fond,   rect, border_radius=15)
        pygame.draw.rect(screen, bordure, rect, ep, border_radius=15)

        # Bande rouge supérieure
        bande = pygame.Rect(x + 10, y + 10, self.taille_carte - 20, 40)
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'], bande, border_radius=8)

        # Numéro Pokédex
        num_texte = self.font_info.render(f"N° {pokemon.get('id', '?'):03d}", True, self.couleurs['blanc'])
        screen.blit(num_texte, (x + 20, y + 20))

        # Zone image
        img_rect = pygame.Rect(x + 15, y + 60, self.taille_carte - 30, 80)
        pygame.draw.rect(screen, self.couleurs['blanc_casse'], img_rect, border_radius=10)
        pygame.draw.rect(screen, self.couleurs['gris_clair'],  img_rect, 2, border_radius=10)

        cx = x + self.taille_carte // 2
        cy = y + 100

        if est_possede:
            # ── Pokémon possédé 
            self.dessiner_sprite(screen, pokemon, cx, cy, 70)

            nom_texte = self.font_nom.render(pokemon.get('name', 'Inconnu'), True, self.couleurs['noir'])
            screen.blit(nom_texte, nom_texte.get_rect(center=(cx, y + 155)))

            self._dessiner_badges_types(screen, pokemon.get('type', []),
                                        x + 20, y + 175, self.taille_carte - 40)
        else:
            # ── Pokémon non possédé 
            self.dessiner_pokeball_non_possede(screen, cx, cy, rayon=28)

            point_interro = self.font_nom.render("???", True, self.couleurs['gris'])
            screen.blit(point_interro, point_interro.get_rect(center=(cx, y + 155)))

    
    #  Panneau de détails 
    

    def _dessiner_details(self, screen):
        pokemon = self.pokedex.obtenir_pokemon_selectionne()
        if not pokemon:
            return

        est_possede = pokemon.get('stats', {}).get('found', False)

        panel_x, panel_y   = self.largeur - 380, 120
        panel_l, panel_h   = 360, self.hauteur - 140

        # Ombre + fond + bordure
        pygame.draw.rect(screen, self.couleurs['ombre'],
                         (panel_x + 5, panel_y + 5, panel_l, panel_h), border_radius=20)
        pygame.draw.rect(screen, self.couleurs['blanc'],
                         (panel_x, panel_y, panel_l, panel_h), border_radius=20)
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'],
                         (panel_x, panel_y, panel_l, panel_h), 5, border_radius=20)

        # Bande décorative rouge
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'],
                         (panel_x, panel_y, panel_l, 60), border_radius=20)
        pygame.draw.rect(screen, self.couleurs['blanc'],
                         (panel_x, panel_y + 55, panel_l, 10))
        screen.blit(self.font_info.render("DÉTAILS", True, self.couleurs['blanc']),
                    (panel_x + 20, panel_y + 15))

        y = panel_y + 80

        if est_possede:
            # Nom
            screen.blit(self.font_titre.render(pokemon.get('name', '?'), True, self.couleurs['rouge_pokemon']),
                        (panel_x + 20, y)); y += 50
            # Numéro
            screen.blit(self.font_info.render(f"N° {pokemon.get('id', '?'):03d}", True, self.couleurs['gris']),
                        (panel_x + 20, y)); y += 35

            # Zone sprite
            sprite_rect = pygame.Rect(panel_x + 20, y, panel_l - 40, 120)
            pygame.draw.rect(screen, self.couleurs['blanc_casse'], sprite_rect, border_radius=15)
            pygame.draw.rect(screen, self.couleurs['gris_clair'],  sprite_rect, 2, border_radius=15)
            self.dessiner_sprite(screen, pokemon,
                                 panel_x + panel_l // 2, y + 60, 100)
            y += 135

            # Types
            screen.blit(self.font_info.render("TYPES", True, self.couleurs['noir']), (panel_x + 20, y))
            y += 25
            y = self._dessiner_badges_types(screen, pokemon.get('type', []),
                                            panel_x + 20, y, 140, hauteur_badge=30,
                                            retourner_y=True)
            y += 10

            # Stats
            screen.blit(self.font_info.render("STATISTIQUES", True, self.couleurs['noir']),
                        (panel_x + 20, y)); y += 30
            self._dessiner_stats(screen, pokemon.get('stats', {}), panel_x, y)

        else:
            # ── Pokémon non possédé 
            self.dessiner_pokeball_non_possede(screen,
                                               panel_x + panel_l // 2,
                                               panel_y + panel_h // 2 - 60,
                                               rayon=55)
            msg1 = self.font_nom.render("??? Inconnu ???", True, self.couleurs['gris'])
            msg2 = self.font_petit.render("Trouvez ce Pokémon pour", True, self.couleurs['gris'])
            msg3 = self.font_petit.render("révéler ses informations !", True, self.couleurs['gris'])
            mx = panel_x + panel_l // 2
            my = panel_y + panel_h // 2 + 20
            screen.blit(msg1, msg1.get_rect(center=(mx, my)));      my += 35
            screen.blit(msg2, msg2.get_rect(center=(mx, my)));      my += 22
            screen.blit(msg3, msg3.get_rect(center=(mx, my)))

        # Bouton fermer
        self._dessiner_bouton_fermer(screen, panel_x, panel_y, panel_l, panel_h)

    
    #  Helpers de dessin
    

    def _dessiner_badges_types(self, screen, types, x: int, y: int,
                               largeur_badge: int, hauteur_badge: int = 28,
                               retourner_y: bool = False):
        """Dessine les badges de types et retourne le y final si demandé."""
        if isinstance(types, str):
            types = [types]
        for t in types:
            t_norm = t.capitalize()
            rect = pygame.Rect(x, y, largeur_badge, hauteur_badge)
            pygame.draw.rect(screen, self.couleur_type(t_norm), rect,
                             border_radius=hauteur_badge // 2)
            txt = self.font_info.render(t_norm.upper(), True, self.couleurs['blanc'])
            screen.blit(txt, txt.get_rect(center=rect.center))
            y += hauteur_badge + 5
        return y if retourner_y else None

    def _dessiner_stats(self, screen, stats: dict, panel_x: int, y: int):
        mapping = {'hp': 'PV', 'attack': 'ATT', 'defense': 'DEF', 'speed': 'VIT'}
        barre_x  = panel_x + 65
        barre_l  = 200
        barre_h  = 16

        for key in ('hp', 'attack', 'defense', 'speed'):
            if key not in stats or key == 'found':
                continue
            valeur = stats[key]
            screen.blit(self.font_petit.render(mapping[key], True, self.couleurs['noir']),
                        (panel_x + 20, y))

            # Fond de barre
            pygame.draw.rect(screen, self.couleurs['gris_clair'],
                             (barre_x, y, barre_l, barre_h), border_radius=8)
            # Remplissage
            pct = min(valeur / 200, 1.0)
            remplie = int(barre_l * pct)
            if remplie > 0:
                pygame.draw.rect(screen, self.couleur_stat(pct),
                                 (barre_x, y, remplie, barre_h), border_radius=8)
            # Contour
            pygame.draw.rect(screen, self.couleurs['gris'],
                             (barre_x, y, barre_l, barre_h), 2, border_radius=8)
            # Valeur numérique
            screen.blit(self.font_petit.render(str(valeur), True, self.couleurs['rouge_pokemon']),
                        (barre_x + barre_l + 8, y))
            y += 28

    def _dessiner_bouton_fermer(self, screen, panel_x, panel_y, panel_l, panel_h):
        bouton_y   = panel_y + panel_h - 60
        bouton_rect = pygame.Rect(panel_x + 20, bouton_y, panel_l - 40, 40)
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'], bouton_rect, border_radius=20)
        txt = self.font_info.render("FERMER", True, self.couleurs['blanc'])
        screen.blit(txt, txt.get_rect(center=bouton_rect.center))

    
    #  Événements souris
    

    def est_clique(self, pos):
        """Gère les clics (bouton fermer ou sélection d'une carte)."""
        x, y = pos

        # Bouton fermer
        if self.pokedex.obtenir_pokemon_selectionne():
            panel_x, panel_y = self.largeur - 380, 120
            panel_l, panel_h = 360, self.hauteur - 140
            bouton_rect = pygame.Rect(panel_x + 20, panel_y + panel_h - 60, panel_l - 40, 40)
            if bouton_rect.collidepoint(x, y):
                self.pokedex.deselectionner_pokemon()
                return

        # Cartes de la grille
        y_depart = 120 + self.marge - self.scroll_offset
        for i, pokemon in enumerate(self.pokedex.obtenir_tous_les_pokemon()):
            cx = self.marge + (i % self.pokemon_par_ligne) * (self.taille_carte + self.marge)
            cy = y_depart + (i // self.pokemon_par_ligne) * (self.taille_carte + self.marge)
            if pygame.Rect(cx, cy, self.taille_carte, self.taille_carte).collidepoint(x, y):
                self.pokedex.selectionner_pokemon(pokemon)
                return

    def verifier_survol(self, pos):
        """Met à jour l'index survolé."""
        x, y = pos
        y_depart = 120 + self.marge - self.scroll_offset
        self.index_survol = None
        for i, pokemon in enumerate(self.pokedex.obtenir_tous_les_pokemon()):
            cx = self.marge + (i % self.pokemon_par_ligne) * (self.taille_carte + self.marge)
            cy = y_depart + (i // self.pokemon_par_ligne) * (self.taille_carte + self.marge)
            if pygame.Rect(cx, cy, self.taille_carte, self.taille_carte).collidepoint(x, y):
                self.index_survol = i
                return

    def defiler(self, direction: int):
        """Défilement vertical (direction : +1 bas, -1 haut)."""
        self.scroll_offset = max(0, self.scroll_offset + direction * 40)