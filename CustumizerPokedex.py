import pygame

class CustomizerPokedex:
    def __init__(self, pokedex, largeur, hauteur):
        """
        Initialise l'interface graphique du Pokédex
        
        Args:
            pokedex (list): Liste des Pokémon
            largeur (int): Largeur de la fenêtre
            hauteur (int): Hauteur de la fenêtre
        """
        self.pokedex = pokedex
        self.largeur = largeur
        self.hauteur = hauteur
        
        # État de l'interface
        self.pokemon_selectionne = None
        self.index_survol = None
        self.scroll_offset = 0
        
        # Configuration visuelle
        self.pokemon_par_ligne = 4
        self.taille_carte = 180
        self.marge = 25
        
        # Couleurs Pokémon (rouge et blanc)
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
    
    def dessiner(self, screen):
        """Dessine l'interface complète du Pokédex"""
        # Fond dégradé
        screen.fill(self.couleurs['fond'])
        
        # En-tête rouge style Pokémon
        self._dessiner_header(screen)
        
        # Grille de Pokémon
        self._dessiner_grille(screen)
        
        # Détails du Pokémon sélectionné
        if self.pokemon_selectionne:
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
        compteur = self.font_petit.render(f"{len(self.pokedex)} Pokémon enregistrés", True, (255, 200, 200))
        screen.blit(compteur, (250, 70))
    
    def _dessiner_grille(self, screen):
        """Dessine la grille des cartes Pokémon"""
        zone_grille_y = 120
        zone_grille_hauteur = self.hauteur - 140
        
        # Calculer la largeur disponible pour la grille
        largeur_grille = self.largeur - 400 if self.pokemon_selectionne else self.largeur
        
        x_depart = self.marge
        y_depart = zone_grille_y + self.marge - self.scroll_offset
        
        for i, pokemon in enumerate(self.pokedex):
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
        # Déterminer la couleur de fond
        if self.pokemon_selectionne == pokemon:
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
        
        # Zone blanche pour l'image (simulée)
        image_rect = pygame.Rect(x + 15, y + 60, self.taille_carte - 30, 80)
        pygame.draw.rect(screen, self.couleurs['blanc_casse'], image_rect, border_radius=10)
        pygame.draw.rect(screen, self.couleurs['gris_clair'], image_rect, 2, border_radius=10)
        
        # Icône Pokéball au centre (placeholder pour image)
        centre_x = x + self.taille_carte // 2
        centre_y = y + 100
        pygame.draw.circle(screen, self.couleurs['gris_clair'], (centre_x, centre_y), 25)
        pygame.draw.arc(screen, self.couleurs['rouge_pokemon'], 
                       (centre_x - 25, centre_y - 25, 50, 50), 0, 3.14, 3)
        pygame.draw.circle(screen, self.couleurs['blanc'], (centre_x, centre_y), 8)
        pygame.draw.circle(screen, self.couleurs['gris'], (centre_x, centre_y), 5)
        
        # Nom du Pokémon
        nom_texte = self.font_nom.render(pokemon.get('name', 'Inconnu'), True, self.couleurs['noir'])
        nom_rect = nom_texte.get_rect(center=(x + self.taille_carte // 2, y + 155))
        screen.blit(nom_texte, nom_rect)
        
        # Types (badges arrondis)
        types = pokemon.get('type', [])
        y_type = y + 175
        
        for type_pokemon in types:
            # Normaliser le type 
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
        
        pokemon = self.pokemon_selectionne
        y_courant = panel_y + 15
        
        # Titre 
        titre = self.font_info.render("DÉTAILS", True, self.couleurs['blanc'])
        screen.blit(titre, (panel_x + 20, y_courant))
        
        y_courant = panel_y + 80
        
        # Nom du Pokémon
        nom = self.font_titre.render(pokemon.get('name', 'Inconnu'), True, self.couleurs['rouge_pokemon'])
        screen.blit(nom, (panel_x + 20, y_courant))
        y_courant += 55
        
        # Numéro
        num = self.font_info.render(f"N° {pokemon.get('id', '?'):03d}", True, self.couleurs['gris'])
        screen.blit(num, (panel_x + 20, y_courant))
        y_courant += 40
        
        # Section Types
        types_titre = self.font_info.render("TYPES", True, self.couleurs['noir'])
        screen.blit(types_titre, (panel_x + 20, y_courant))
        y_courant += 30
        
        types = pokemon.get('type', [])
        for type_pokemon in types:
            # Normaliser le type
            type_normalise = type_pokemon.capitalize()
            couleur_type = self.couleurs_types.get(type_normalise, (100, 100, 100))
            
            # Badge de type plus large
            type_rect = pygame.Rect(panel_x + 20, y_courant, 150, 35)
            pygame.draw.rect(screen, couleur_type, type_rect, border_radius=17)
            
            type_texte = self.font_info.render(type_normalise.upper(), True, self.couleurs['blanc'])
            type_texte_rect = type_texte.get_rect(center=type_rect.center)
            screen.blit(type_texte, type_texte_rect)
            y_courant += 42
        
        y_courant += 20
        
        # Section Statistiques - Depuis le sous-objet "stats"
        stats_titre = self.font_info.render("STATISTIQUES", True, self.couleurs['noir'])
        screen.blit(stats_titre, (panel_x + 20, y_courant))
        y_courant += 35
        
        # Récupérer les stats depuis le sous-objet
        stats_obj = pokemon.get('stats', {})
        
        # Mapping des noms de stats
        stats_mapping = {
            'hp': 'PV',
            'attack': 'ATTAQUE',
            'defense': 'DÉFENSE',
            'speed': 'VITESSE'
        }
        
        # Ordre d'affichage des stats
        stats_ordre = ['hp', 'attack', 'defense', 'speed']
        
        for stat_key in stats_ordre:
            if stat_key in stats_obj and stat_key != 'found':
                nom_stat = stats_mapping.get(stat_key, stat_key.upper())
                valeur = stats_obj[stat_key]
                
                # Label de la stat
                label = self.font_info.render(nom_stat, True, self.couleurs['noir'])
                screen.blit(label, (panel_x + 20, y_courant))
                
                # Barre de progression style Pokémon
                barre_x = panel_x + 20
                barre_y = y_courant + 25
                barre_largeur = 280
                barre_hauteur = 18
                
                # Fond de la barre (gris clair)
                pygame.draw.rect(screen, self.couleurs['gris_clair'],
                               (barre_x, barre_y, barre_largeur, barre_hauteur),
                               border_radius=9)
                
                # Barre remplie (dégradé rouge)
                pourcentage = min(valeur / 200, 1.0)
                largeur_remplie = int(barre_largeur * pourcentage)
                
                if largeur_remplie > 0:
                    couleur_stat = self._couleur_stat(pourcentage)
                    pygame.draw.rect(screen, couleur_stat,
                                   (barre_x, barre_y, largeur_remplie, barre_hauteur),
                                   border_radius=9)
                
                # Bordure de la barre
                pygame.draw.rect(screen, self.couleurs['gris'],
                               (barre_x, barre_y, barre_largeur, barre_hauteur),
                               2, border_radius=9)
                
                # Valeur numérique
                valeur_texte = self.font_info.render(str(valeur), True, self.couleurs['rouge_pokemon'])
                screen.blit(valeur_texte, (barre_x + barre_largeur + 10, y_courant + 20))
                
                y_courant += 55
        
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
            return (255, 150, 150)  # Rouge clair
        elif pourcentage < 0.66:
            return (255, 200, 100)  # Orange
        else:
            return (100, 220, 100)  # Vert
    
    def est_clique(self, pos):
        """Gère les clics de souris"""
        x, y = pos
        
        # rectification ici
        if self.pokemon_selectionne:
            panel_x = self.largeur - 380
            panel_y = 120
            panel_largeur = 360
            panel_hauteur = self.hauteur - 140
            bouton_y = panel_y + panel_hauteur - 60
            bouton_rect = pygame.Rect(panel_x + 20, bouton_y, panel_largeur - 40, 40)
            
            if bouton_rect.collidepoint(x, y):
                self.pokemon_selectionne = None
                return
        
        zone_grille_y = 120
        y_depart = zone_grille_y + self.marge - self.scroll_offset
        
        for i, pokemon in enumerate(self.pokedex):
            ligne = i // self.pokemon_par_ligne
            colonne = i % self.pokemon_par_ligne
            
            carte_x = self.marge + colonne * (self.taille_carte + self.marge)
            carte_y = y_depart + ligne * (self.taille_carte + self.marge)
            
            rect = pygame.Rect(carte_x, carte_y, self.taille_carte, self.taille_carte)
            
            if rect.collidepoint(x, y):
                self.pokemon_selectionne = pokemon
                return
    
    def verifier_survol(self, pos):
        """Gère le survol de la souris"""
        x, y = pos
        
        zone_grille_y = 120
        y_depart = zone_grille_y + self.marge - self.scroll_offset
        
        self.index_survol = None
        
        for i, pokemon in enumerate(self.pokedex):
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