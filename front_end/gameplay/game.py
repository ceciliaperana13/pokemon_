import pygame
from .keylistener import KeyListener
from .map import Map
from .player import Player
from .CustumizerPokedex import CustomizerPokedex
from .pokedexButton import PokedexButton
from front_end.menu.pause_menu import PauseMenu  # 🆕 Import du menu pause


class Game:
    def __init__(self, screen, player_name, pokemon, pokedex):
        """
        Initializes the game, setting up the main components such as the map, player, and key listener.
        """
        self.running = True  # Determines if the game loop should continue running
        self.screen = screen  # Reference to the game screen
        self.map: Map = Map(self.screen)  # Create the game map
        self.keylistener = KeyListener()  # Initialize the key listener to track player input
        self.player: Player = Player(self.keylistener, self.screen, 100, 300, player_name, pokemon)  # Create the player character
        self.map.add_player(self.player)  # Add the player to the map 
        self.pokemon = pokemon
        self.player_name = player_name  # Nom du joueur
        self.pokedex = pokedex  # Pokédex passé depuis le menu
        
        # ========================================
        # 🆕 INITIALISATION DE L'INTERFACE POKÉDEX
        # ========================================
        
        # Obtenir les dimensions de l'écran
        if hasattr(self.screen, 'width') and hasattr(self.screen, 'height'):
            largeur_ecran = self.screen.width
            hauteur_ecran = self.screen.height
        elif hasattr(self.screen, 'get_width') and hasattr(self.screen, 'get_height'):
            largeur_ecran = self.screen.get_width()
            hauteur_ecran = self.screen.get_height()
        else:
            largeur_ecran = 1200
            hauteur_ecran = 800
        
        # 🔧 Trouver et stocker la surface pygame dès le début
        self.pygame_surface = self._find_pygame_surface()
        
        # Interface graphique du Pokédex
        self.pokedex_ui = CustomizerPokedex(
            self.pokedex,
            largeur_ecran,
            hauteur_ecran
        )
        
        # 🆕 Bouton pour ouvrir le Pokédex (en bas à droite)
        bouton_x = largeur_ecran - 130
        bouton_y = hauteur_ecran - 130
        self.bouton_pokedex = PokedexButton(
            bouton_x,
            bouton_y,
            image_path="assets/logo/pokedex.png",
            taille=100
        )
        
        # État du Pokédex (ouvert ou fermé)
        self.pokedex_ouvert = False
        
        print(f"✓ Interface Pokédex initialisée ({largeur_ecran}x{hauteur_ecran})")
        print(f"✓ Surface pygame: {self.pygame_surface}")

    def run(self):
        """
        Main game loop that continuously updates and renders the game.
        """
        while self.running:
            self.handle_input()  # Process user input events
            
            # 🆕 Ne mettre à jour le jeu que si le Pokédex est fermé
            if not self.pokedex_ouvert:
                self.map.update()  # Update the map (including objects, NPCs, etc.)
                self.player.update()  # Update the player's position and state
                
                # 🆕 Mettre à jour l'animation du bouton
                self.bouton_pokedex.update()
                
                # 🆕 Dessiner le bouton Pokédex par-dessus le jeu
                if self.pygame_surface:
                    self.bouton_pokedex.dessiner(self.pygame_surface)
            else:
                # Quand le Pokédex est ouvert, afficher le Pokédex en plein écran
                if self.pygame_surface:
                    self.pokedex_ui.dessiner(self.pygame_surface)
            
            self.screen.update()  # Refresh the game screen

    def handle_input(self):
        """
        Handles user input by listening for key presses and game quit events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the player closes the window, exit the game
                pygame.quit()
            
            # ========================================
            # 🆕 GESTION DES ÉVÉNEMENTS SOURIS
            # ========================================
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    
                    if self.pokedex_ouvert:
                        # Gérer les clics dans le Pokédex ouvert
                        self.pokedex_ui.est_clique(event.pos)
                    else:
                        # Vérifier si on clique sur le bouton Pokédex
                        if self.bouton_pokedex.verifier_clic(event.pos):
                            self.ouvrir_pokedex()
                
                elif event.button == 4:  # Molette haut
                    if self.pokedex_ouvert:
                        self.pokedex_ui.defiler(-1)
                
                elif event.button == 5:  # Molette bas
                    if self.pokedex_ouvert:
                        self.pokedex_ui.defiler(1)
            
            elif event.type == pygame.MOUSEMOTION:
                # Gérer le survol de la souris
                if self.pokedex_ouvert:
                    self.pokedex_ui.verifier_survol(event.pos)
                else:
                    self.bouton_pokedex.verifier_survol(event.pos)
            
            # ========================================
            # GESTION DU CLAVIER
            # ========================================
            
            elif event.type == pygame.KEYDOWN:  # When a key is pressed
                
                # 🆕 Touche P pour ouvrir/fermer le Pokédex
                if event.key == pygame.K_p:
                    if self.pokedex_ouvert:
                        self.fermer_pokedex()
                    else:
                        self.ouvrir_pokedex()
                
                # 🆕 Touche ECHAP : Fermer Pokédex OU Ouvrir le menu pause
                elif event.key == pygame.K_ESCAPE:
                    if self.pokedex_ouvert:
                        # Si le Pokédex est ouvert, juste le fermer
                        self.fermer_pokedex()
                    else:
                        # Si on est dans le jeu, ouvrir le menu pause
                        self.open_pause_menu()
                
                # Ne gérer les touches de jeu que si le Pokédex est fermé
                elif not self.pokedex_ouvert:
                    self.keylistener.add_key(event.key)
            
            elif event.type == pygame.KEYUP:  # When a key is released
                # Ne gérer les touches de jeu que si le Pokédex est fermé
                if not self.pokedex_ouvert:
                    self.keylistener.remove_key(event.key)
    
    def open_pause_menu(self):
        """
        🆕 Ouvre le menu pause
        """
        print("⏸️  Menu pause ouvert")
        
        # Créer et afficher le menu pause
        pause_menu = PauseMenu(
            self.player_name,
            self.pokemon,
            self.screen,
            self.pokedex
        )
        
        # Afficher le menu et récupérer le résultat
        result_player, result_pokemon = pause_menu.display()
        
        # Si le résultat est None, cela signifie "retour au menu principal"
        if result_player is None and result_pokemon is None:
            print("🔙 Retour au menu principal...")
            self.running = False
        else:
            # Mettre à jour le joueur et le Pokémon si changés
            if result_player:
                self.player_name = result_player
            if result_pokemon:
                self.pokemon = result_pokemon
            
            print("▶️  Reprise du jeu")
    
    def _find_pygame_surface(self):
        """
        🔧 Trouve et retourne la surface pygame depuis l'objet Screen
        
        Returns:
            pygame.Surface: La surface sur laquelle dessiner
        """
        # Si c'est déjà une Surface pygame
        if isinstance(self.screen, pygame.Surface):
            return self.screen
        
        # Essayer différents attributs communs
        attributs_a_essayer = ['screen', 'surface', 'display', '_surface', '_screen']
        
        for attr in attributs_a_essayer:
            if hasattr(self.screen, attr):
                obj = getattr(self.screen, attr)
                if isinstance(obj, pygame.Surface):
                    print(f"✓ Surface pygame trouvée via self.screen.{attr}")
                    return obj
        
        
        surface = pygame.display.get_surface()
        if surface:
            print(f"✓ Surface pygame trouvée via pygame.display.get_surface()")
            return surface
        
        # Dernière tentative : chercher dans __dict__
        if hasattr(self.screen, '__dict__'):
            for key, value in self.screen.__dict__.items():
                if isinstance(value, pygame.Surface):
                    print(f"✓ Surface pygame trouvée via self.screen.{key}")
                    return value
        
        # Aucune surface trouvée
        print(f"⚠ ERREUR: Impossible de trouver la surface pygame!")
        print(f"   Type de self.screen: {type(self.screen)}")
        print(f"   Attributs disponibles: {dir(self.screen)[:10]}...")
        
        return None
    
    def ouvrir_pokedex(self):
        """
        🆕 Ouvre le Pokédex
        """
        self.pokedex_ouvert = True
        print("📱 Pokédex ouvert")
    
    def fermer_pokedex(self):
        """
        🆕 Ferme le Pokédex
        """
        self.pokedex_ouvert = False
        self.pokedex.deselectionner_pokemon()
        print("📱 Pokédex fermé")
    
    def decouvrir_pokemon(self, pokemon_id):
        """
        🆕 Marque un Pokémon comme découvert dans le Pokédex
        
        Args:
            pokemon_id (int): ID du Pokémon à découvrir
        
        Returns:
            bool: True si c'est une nouvelle découverte, False sinon
        """
        est_nouvelle_decouverte = self.pokedex.marquer_comme_trouve(pokemon_id)
        
        if est_nouvelle_decouverte:
            pokemon = self.pokedex.obtenir_pokemon_par_id(pokemon_id)
            if pokemon:
                nom = pokemon.get('name', 'Inconnu')
                print(f"✨ {nom} découvert et ajouté au Pokédex !")
                # Vous pouvez ajouter une notification visuelle ici
        
        return est_nouvelle_decouverte