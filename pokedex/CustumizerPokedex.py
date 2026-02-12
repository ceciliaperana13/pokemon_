import pygame
import os

class CustomizerPokedex:
    """Classe pour l'interface graphique du Pokédex"""
    
    def __init__(self, pokedex, largeur, hauteur):
        """
        Initialise l'interface graphique du Pokédex
        
        Args:
            pokedex: Instance de la classe Pokedex
            largeur (int): Largeur de la fenêtre
            hauteur (int): Hauteur de la fenêtre
        """
        self.pokedex = pokedex
        self.largeur = largeur
        self.hauteur = hauteur
        
        # État de l'interface
        self.index_survol = None
        self.scroll_offset = 0
        
        # Cache pour les sprites
        self.sprites_cache = {}
        
        # Configuration visuelle
        self.pokemon_par_ligne = 4
        self.taille_carte = 180
        self.marge = 25
        
        # Couleurs Pokémon 
        self.couleurs = {
            'fond': (220, 220, 230),
            'rouge_pokemon': (220, 30, 30),
            'rouge_fonce': (180, 20, 20),
            'blanc': (255, 255, 255),
            'blanc_casse': (245, 245, 250),
            'noir': (40, 40, 50),
            'gris': (150, 150, 160),
            'gris_clair': (200, 200, 210),
            'carte': (255, 255, 255),
            'carte_survol': (255, 245, 245),
            'carte_selectionnee': (255, 230, 230),
            'ombre': (180, 180, 190)
        }
        
        # Couleurs des types Pokémon
        self.couleurs_types = {
            'Feu': (255, 68, 34),
            'Eau': (52, 152, 219),
            'Plante': (46, 204, 113),
            'Electrik': (241, 196, 15),
            'Psy': (155, 89, 182),
            'Combat': (192, 57, 43),
            'Normal': (149, 165, 166),
            'Vol': (133, 193, 233),
            'Poison': (142, 68, 173),
            'Sol': (211, 84, 0),
            'Roche': (120, 81, 45),
            'Insecte': (166, 187, 0),
            'Spectre': (52, 73, 94),
            'Acier': (120, 144, 156),
            'Glace': (174, 214, 241),
            'Dragon': (116, 125, 140),
            'Ténèbres': (44, 62, 80),
            'Fée': (253, 121, 168)
        }
        
        # Polices
        self.font_titre = pygame.font.Font(None, 48)
        self.font_nom = pygame.font.Font(None, 32)
        self.font_info = pygame.font.Font(None, 24)
        self.font_petit = pygame.font.Font(None, 20)
    
    def charger_sprite(self, pokemon):
        """
        Charge le sprite d'un Pokémon depuis le JSON ou génère le chemin
        
        Args:
            pokemon (dict): Données du Pokémon
            
        Returns:
            pygame.Surface: Image du Pokémon ou None si non trouvée
        """
        pokemon_id = pokemon.get('id')
        
        # Vérifier le cache
        if pokemon_id in self.sprites_cache:
            return self.sprites_cache[pokemon_id]
        
        sprite = None
        
        # Option 1: Chemin depuis le JSON
        chemin_sprite = pokemon.get('sprite')
        
        # Option 2: Générer le chemin automatiquement si non présent dans le JSON
        if not chemin_sprite:
            chemin_sprite = f"assets/imagePokedex/Spr_1b_{pokemon_id:03d}.png"
        
        # Essayer de charger le sprite
        if chemin_sprite and os.path.exists(chemin_sprite):
            try:
                sprite = pygame.image.load(chemin_sprite).convert_alpha()
            except pygame.error as e:
                print(f" Erreur lors du chargement du sprite {chemin_sprite}: {e}")
        else:
            # Si le fichier n'existe pas, essayer d'autres formats possibles
            chemins_alternatifs = [
                f"assets/imagePokedex/Spr_1b_{pokemon_id:03d}.png",
                f"assets/imagePokedex/{pokemon_id:03d}.png",
                f"assets/imagePokedex/{pokemon_id}.png"
            ]
            
            for chemin in chemins_alternatifs:
                if os.path.exists(chemin):
                    try:
                        sprite = pygame.image.load(chemin).convert_alpha()
                        break
                    except pygame.error:
                        continue
        
        # Mettre en cache (même si None)
        self.sprites_cache[pokemon_id] = sprite
        return sprite
    
    def dessiner_sprite(self, screen, pokemon, x, y, taille_max):
        """
        Dessine le sprite d'un Pokémon
        
        Args:
            screen: Surface Pygame
            pokemon (dict): Données du Pokémon
            x (int): Position X du centre
            y (int): Position Y du centre
            taille_max (int): Taille maximale du sprite
        """
        sprite = self.charger_sprite(pokemon)
        
        if sprite:
            # Redimensionner le sprite pour qu'il rentre dans la zone
            sprite_rect = sprite.get_rect()
            ratio = min(taille_max / sprite_rect.width, taille_max / sprite_rect.height)
            nouvelle_largeur = int(sprite_rect.width * ratio)
            nouvelle_hauteur = int(sprite_rect.height * ratio)
            
            sprite_redimensionne = pygame.transform.scale(sprite, (nouvelle_largeur, nouvelle_hauteur))
            sprite_rect = sprite_redimensionne.get_rect(center=(x, y))
            
            screen.blit(sprite_redimensionne, sprite_rect)
        else:
            # Fallback: Pokéball stylisée
            self._dessiner_pokeball_placeholder(screen, x, y)
    
    def _dessiner_pokeball_placeholder(self, screen, x, y):
        """Dessine une Pokéball comme placeholder si pas de sprite"""
        pygame.draw.circle(screen, self.couleurs['gris_clair'], (x, y), 25)
        pygame.draw.arc(screen, self.couleurs['rouge_pokemon'], 
                       (x - 25, y - 25, 50, 50), 0, 3.14, 3)
        pygame.draw.circle(screen, self.couleurs['blanc'], (x, y), 8)
        pygame.draw.circle(screen, self.couleurs['gris'], (x, y), 5)
    
    def dessiner(self, screen):
        """Dessine l'interface complète du Pokédex"""
        # Fond
        screen.fill(self.couleurs['fond'])
        
        # En-tête rouge style Pokémon
        self._dessiner_header(screen)
        
        # Grille de Pokémon
        self._dessiner_grille(screen)
        
        # Détails du Pokémon sélectionné
        if self.pokedex.obtenir_pokemon_selectionne():
            self._dessiner_details(screen)
    
    def _dessiner_header(self, screen):
        """Dessine l'en-tête style Pokédex"""
        # Barre rouge supérieure
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'], (0, 0, self.largeur, 100))
        pygame.draw.rect(screen, self.couleurs['rouge_fonce'], (0, 95, self.largeur, 5))
        
        # Cercle blanc à gauche (style Pokéball)
        pygame.draw.circle(screen, self.couleurs['blanc'], (80, 50), 35)
        pygame.draw.circle(screen, self.couleurs['rouge_pokemon'], (80, 50), 30)
        pygame.draw.circle(screen, self.couleurs['blanc'], (80, 50), 15)
        pygame.draw.circle(screen, self.couleurs['noir'], (80, 50), 8)
        
        # Petits cercles décoratifs
        for i, couleur in enumerate([self.couleurs['rouge_fonce'], (255, 150, 150), (255, 100, 100)]):
            pygame.draw.circle(screen, couleur, (150 + i*25, 50), 8)
        
        # Titre
        texte = self.font_titre.render("POKÉDEX", True, self.couleurs['blanc'])
        screen.blit(texte, (250, 35))
        
        # Compteur de Pokémon
        compteur = self.font_petit.render(f"{self.pokedex.nombre_pokemon()} Pokémon enregistrés", True, (255, 200, 200))
        screen.blit(compteur, (250, 70))
    
    def _dessiner_grille(self, screen):
        """Dessine la grille des cartes Pokémon"""
        zone_grille_y = 120
        zone_grille_hauteur = self.hauteur - 140
        
        # Calculer la largeur disponible pour la grille
        largeur_grille = self.largeur - 400 if self.pokedex.obtenir_pokemon_selectionne() else self.largeur
        
        x_depart = self.marge
        y_depart = zone_grille_y + self.marge - self.scroll_offset
        
        pokemon_list = self.pokedex.obtenir_tous_les_pokemon()
        
        for i, pokemon in enumerate(pokemon_list):
            ligne = i // self.pokemon_par_ligne
            colonne = i % self.pokemon_par_ligne
            
            x = x_depart + colonne * (self.taille_carte + self.marge)
            y = y_depart + ligne * (self.taille_carte + self.marge)
            
            # Ne dessiner que si visible
            if y + self.taille_carte < zone_grille_y or y > zone_grille_y + zone_grille_hauteur:
                continue
            
            self._dessiner_carte_pokemon(screen, pokemon, x, y, i)
    
    def _dessiner_carte_pokemon(self, screen, pokemon, x, y, index):
        """Dessine une carte Pokémon style trading card"""
        pokemon_selectionne = self.pokedex.obtenir_pokemon_selectionne()
        
        # Déterminer la couleur de fond
        if pokemon_selectionne and pokemon_selectionne.get('id') == pokemon.get('id'):
            couleur_fond = self.couleurs['carte_selectionnee']
            bordure_couleur = self.couleurs['rouge_pokemon']
            bordure_epaisseur = 4
        elif self.index_survol == index:
            couleur_fond = self.couleurs['carte_survol']
            bordure_couleur = self.couleurs['rouge_pokemon']
            bordure_epaisseur = 3
        else:
            couleur_fond = self.couleurs['carte']
            bordure_couleur = self.couleurs['gris_clair']
            bordure_epaisseur = 2
        
        # Ombre
        ombre_rect = pygame.Rect(x + 5, y + 5, self.taille_carte, self.taille_carte)
        pygame.draw.rect(screen, self.couleurs['ombre'], ombre_rect, border_radius=15)
        
        # Carte principale
        rect = pygame.Rect(x, y, self.taille_carte, self.taille_carte)
        pygame.draw.rect(screen, couleur_fond, rect, border_radius=15)
        pygame.draw.rect(screen, bordure_couleur, rect, bordure_epaisseur, border_radius=15)
        
        # Bande supérieure rouge
        bande_rect = pygame.Rect(x + 10, y + 10, self.taille_carte - 20, 40)
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'], bande_rect, border_radius=8)
        
        # Numéro sur la bande rouge
        num_texte = self.font_info.render(f"N° {pokemon.get('id', '?'):03d}", True, self.couleurs['blanc'])
        screen.blit(num_texte, (x + 20, y + 20))
        
        # Zone blanche pour l'image
        image_rect = pygame.Rect(x + 15, y + 60, self.taille_carte - 30, 80)
        pygame.draw.rect(screen, self.couleurs['blanc_casse'], image_rect, border_radius=10)
        pygame.draw.rect(screen, self.couleurs['gris_clair'], image_rect, 2, border_radius=10)
        
        # Dessiner le sprite du Pokémon
        centre_x = x + self.taille_carte // 2
        centre_y = y + 100
        self.dessiner_sprite(screen, pokemon, centre_x, centre_y, 70)
        
        # Nom du Pokémon
        nom_texte = self.font_nom.render(pokemon.get('name', 'Inconnu'), True, self.couleurs['noir'])
        nom_rect = nom_texte.get_rect(center=(x + self.taille_carte // 2, y + 155))
        screen.blit(nom_texte, nom_rect)
        
        # Types (badges arrondis)
        types = pokemon.get('type', [])
        y_type = y + 175
        
        for type_pokemon in types:
            # Normaliser le type (première lettre en majuscule)
            type_normalise = type_pokemon.capitalize()
            couleur_type = self.couleurs_types.get(type_normalise, (100, 100, 100))
            
            # Badge de type
            badge_largeur = self.taille_carte - 40
            type_rect = pygame.Rect(x + 20, y_type, badge_largeur, 28)
            pygame.draw.rect(screen, couleur_type, type_rect, border_radius=14)
            
            # Texte du type
            type_texte = self.font_info.render(type_normalise.upper(), True, self.couleurs['blanc'])
            type_texte_rect = type_texte.get_rect(center=type_rect.center)
            screen.blit(type_texte, type_texte_rect)
            
            y_type += 33
    
    def _dessiner_details(self, screen):
        """Dessine le panneau de détails style Pokédex officiel"""
        # Récupérer le Pokémon sélectionné
        pokemon = self.pokedex.obtenir_pokemon_selectionne()
        
        # Vérification de sécurité
        if not pokemon:
            return
        
        panel_x = self.largeur - 380
        panel_y = 120
        panel_largeur = 360
        panel_hauteur = self.hauteur - 140
        
        # Ombre du panneau
        pygame.draw.rect(screen, self.couleurs['ombre'], 
                        (panel_x + 5, panel_y + 5, panel_largeur, panel_hauteur),
                        border_radius=20)
        
        # Fond du panneau blanc
        pygame.draw.rect(screen, self.couleurs['blanc'], 
                        (panel_x, panel_y, panel_largeur, panel_hauteur),
                        border_radius=20)
        
        # Bordure rouge
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'],
                        (panel_x, panel_y, panel_largeur, panel_hauteur),
                        5, border_radius=20)
        
        # Bande décorative rouge en haut
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'],
                        (panel_x, panel_y, panel_largeur, 60),
                        border_radius=20)
        pygame.draw.rect(screen, self.couleurs['blanc'],
                        (panel_x, panel_y + 55, panel_largeur, 10))
        
        y_courant = panel_y + 15
        
        # Titre "DÉTAILS"
        titre = self.font_info.render("DÉTAILS", True, self.couleurs['blanc'])
        screen.blit(titre, (panel_x + 20, y_courant))
        
        y_courant = panel_y + 80
        
        # Nom du Pokémon
        nom = self.font_titre.render(pokemon.get('name', 'Inconnu'), True, self.couleurs['rouge_pokemon'])
        screen.blit(nom, (panel_x + 20, y_courant))
        y_courant += 50
        
        # Numéro
        num = self.font_info.render(f"N° {pokemon.get('id', '?'):03d}", True, self.couleurs['gris'])
        screen.blit(num, (panel_x + 20, y_courant))
        y_courant += 35
        
        # Zone pour le sprite du Pokémon
        sprite_zone_y = y_courant
        sprite_zone_hauteur = 120
        
        # Fond pour le sprite
        sprite_rect = pygame.Rect(panel_x + 20, sprite_zone_y, panel_largeur - 40, sprite_zone_hauteur)
        pygame.draw.rect(screen, self.couleurs['blanc_casse'], sprite_rect, border_radius=15)
        pygame.draw.rect(screen, self.couleurs['gris_clair'], sprite_rect, 2, border_radius=15)
        
        # Dessiner le sprite
        sprite_centre_x = panel_x + panel_largeur // 2
        sprite_centre_y = sprite_zone_y + sprite_zone_hauteur // 2
        self.dessiner_sprite(screen, pokemon, sprite_centre_x, sprite_centre_y, 100)
        
        y_courant = sprite_zone_y + sprite_zone_hauteur + 15
        
        # Section Types
        types_titre = self.font_info.render("TYPES", True, self.couleurs['noir'])
        screen.blit(types_titre, (panel_x + 20, y_courant))
        y_courant += 25
        
        types = pokemon.get('type', [])
        for type_pokemon in types:
            type_normalise = type_pokemon.capitalize()
            couleur_type = self.couleurs_types.get(type_normalise, (100, 100, 100))
            
            type_rect = pygame.Rect(panel_x + 20, y_courant, 140, 30)
            pygame.draw.rect(screen, couleur_type, type_rect, border_radius=15)
            
            type_texte = self.font_petit.render(type_normalise.upper(), True, self.couleurs['blanc'])
            type_texte_rect = type_texte.get_rect(center=type_rect.center)
            screen.blit(type_texte, type_texte_rect)
            y_courant += 35
        
        y_courant += 10
        
        # Section Statistiques
        stats_titre = self.font_info.render("STATISTIQUES", True, self.couleurs['noir'])
        screen.blit(stats_titre, (panel_x + 20, y_courant))
        y_courant += 30
        
        # Récupérer les stats
        stats_obj = pokemon.get('stats', {})
        
        stats_mapping = {
            'hp': 'PV',
            'attack': 'ATT',
            'defense': 'DEF',
            'speed': 'VIT'
        }
        
        stats_ordre = ['hp', 'attack', 'defense', 'speed']
        
        for stat_key in stats_ordre:
            if stat_key in stats_obj and stat_key != 'found':
                nom_stat = stats_mapping.get(stat_key, stat_key.upper())
                valeur = stats_obj[stat_key]
                
                # Label
                label = self.font_petit.render(nom_stat, True, self.couleurs['noir'])
                screen.blit(label, (panel_x + 20, y_courant))
                
                # Barre de progression
                barre_x = panel_x + 65
                barre_y = y_courant
                barre_largeur = 200
                barre_hauteur = 16
                
                # Fond
                pygame.draw.rect(screen, self.couleurs['gris_clair'],
                               (barre_x, barre_y, barre_largeur, barre_hauteur),
                               border_radius=8)
                
                # Barre remplie
                pourcentage = min(valeur / 200, 1.0)
                largeur_remplie = int(barre_largeur * pourcentage)
                
                if largeur_remplie > 0:
                    couleur_stat = self._couleur_stat(pourcentage)
                    pygame.draw.rect(screen, couleur_stat,
                                   (barre_x, barre_y, largeur_remplie, barre_hauteur),
                                   border_radius=8)
                
                # Bordure
                pygame.draw.rect(screen, self.couleurs['gris'],
                               (barre_x, barre_y, barre_largeur, barre_hauteur),
                               2, border_radius=8)
                
                # Valeur
                valeur_texte = self.font_petit.render(str(valeur), True, self.couleurs['rouge_pokemon'])
                screen.blit(valeur_texte, (barre_x + barre_largeur + 8, y_courant))
                
                y_courant += 28
        
        # Bouton de fermeture
        bouton_y = panel_y + panel_hauteur - 60
        bouton_rect = pygame.Rect(panel_x + 20, bouton_y, panel_largeur - 40, 40)
        pygame.draw.rect(screen, self.couleurs['rouge_pokemon'], bouton_rect, border_radius=20)
        
        fermer_texte = self.font_info.render("FERMER", True, self.couleurs['blanc'])
        fermer_rect = fermer_texte.get_rect(center=bouton_rect.center)
        screen.blit(fermer_texte, fermer_rect)
    
    def _couleur_stat(self, pourcentage):
        """Retourne une couleur basée sur le pourcentage de la stat"""
        if pourcentage < 0.33:
            return (255, 150, 150)
        elif pourcentage < 0.66:
            return (255, 200, 100)
        else:
            return (100, 220, 100)
    
    def est_clique(self, pos):
        """Gère les clics de souris"""
        x, y = pos
        
        # Vérifier le bouton fermer
        if self.pokedex.obtenir_pokemon_selectionne():
            panel_x = self.largeur - 380
            panel_y = 120
            panel_largeur = 360
            panel_hauteur = self.hauteur - 140
            bouton_y = panel_y + panel_hauteur - 60
            bouton_rect = pygame.Rect(panel_x + 20, bouton_y, panel_largeur - 40, 40)
            
            if bouton_rect.collidepoint(x, y):
                self.pokedex.deselectionner_pokemon()
                return
        
        # Vérifier les cartes Pokémon
        zone_grille_y = 120
        y_depart = zone_grille_y + self.marge - self.scroll_offset
        
        pokemon_list = self.pokedex.obtenir_tous_les_pokemon()
        
        for i, pokemon in enumerate(pokemon_list):
            ligne = i // self.pokemon_par_ligne
            colonne = i % self.pokemon_par_ligne
            
            carte_x = self.marge + colonne * (self.taille_carte + self.marge)
            carte_y = y_depart + ligne * (self.taille_carte + self.marge)
            
            rect = pygame.Rect(carte_x, carte_y, self.taille_carte, self.taille_carte)
            
            if rect.collidepoint(x, y):
                self.pokedex.selectionner_pokemon(pokemon)
                return
    
    def verifier_survol(self, pos):
        """Gère le survol de la souris"""
        x, y = pos
        
        zone_grille_y = 120
        y_depart = zone_grille_y + self.marge - self.scroll_offset
        
        self.index_survol = None
        
        pokemon_list = self.pokedex.obtenir_tous_les_pokemon()
        
        for i, pokemon in enumerate(pokemon_list):
            ligne = i // self.pokemon_par_ligne
            colonne = i % self.pokemon_par_ligne
            
            carte_x = self.marge + colonne * (self.taille_carte + self.marge)
            carte_y = y_depart + ligne * (self.taille_carte + self.marge)
            
            rect = pygame.Rect(carte_x, carte_y, self.taille_carte, self.taille_carte)
            
            if rect.collidepoint(x, y):
                self.index_survol = i
                return
    
    def defiler(self, direction):
        """Gère le défilement (molette ou flèches)"""
        vitesse_scroll = 40
        self.scroll_offset += direction * vitesse_scroll
        
        # Limiter le scroll
        self.scroll_offset = max(0, self.scroll_offset)