import pygame
from .keylistener import KeyListener
from .map import Map
from .player import Player
from .CustumizerPokedex import CustomizerPokedex
from .pokedexButton import PokedexButton
from front_end.menu.pause_menu import PauseMenu


class Game:
    def __init__(self, screen, player_name, pokemon, pokedex):
        self.running = True
        self.screen = screen
        self.map: Map = Map(self.screen)
        self.keylistener = KeyListener()
        self.player: Player = Player(self.keylistener, self.screen, 100, 300, player_name, pokemon)
        self.map.add_player(self.player)
        self.pokemon = pokemon
        self.player_name = player_name
        self.pokedex = pokedex

        # Dimensions de l'écran
        if hasattr(self.screen, 'get_width') and hasattr(self.screen, 'get_height'):
            largeur_ecran = self.screen.get_width()
            hauteur_ecran = self.screen.get_height()
        elif hasattr(self.screen, 'width') and hasattr(self.screen, 'height'):
            largeur_ecran = self.screen.width
            hauteur_ecran = self.screen.height
        else:
            largeur_ecran, hauteur_ecran = 1200, 800

        self.pygame_surface = self._find_pygame_surface()
        self.pokedex_ui = CustomizerPokedex(self.pokedex, largeur_ecran, hauteur_ecran)
        self.bouton_pokedex = PokedexButton(
            largeur_ecran - 130, hauteur_ecran - 130,
            image_path="assets/logo/pokedex.png", taille=100
        )
        self.pokedex_ouvert = False

        print(f"✓ Interface Pokédex initialisée ({largeur_ecran}x{hauteur_ecran})")

        # ── Enregistrer automatiquement les Pokémon de l'équipe chargée ─────
        self._enregistrer_equipe_dans_pokedex()

    # ══════════════════════════════════════════════════════════════════════════
    #  Enregistrement de l'équipe au chargement
    # ══════════════════════════════════════════════════════════════════════════

    def _enregistrer_equipe_dans_pokedex(self):
        """
        Parcourt self.pokemon et marque chaque Pokémon comme découvert.

        Format attendu de la save :
            {
                "Jean-Marie": {"name": "Sandslash", "original_name": "Sandshrew", ...},
                "Jean-Luc":   {"name": "Raichu",    "original_name": "Pikachu",   ...},
                ...
            }
        Fonctionne aussi si self.pokemon est une liste de dicts.
        """
        if not self.pokemon:
            print("⚠ Aucun Pokémon dans l'équipe chargée.")
            return

        # Normaliser en liste de dicts
        if isinstance(self.pokemon, dict):
            # Valeurs du dict (les dicts de chaque Pokémon)
            pokemons_a_traiter = list(self.pokemon.values())
        elif isinstance(self.pokemon, list):
            pokemons_a_traiter = self.pokemon
        else:
            pokemons_a_traiter = [self.pokemon]

        nouveaux = 0
        non_resolus = []

        for poke in pokemons_a_traiter:
            pokemon_id = self._resoudre_id_depuis_save(poke)

            if pokemon_id:
                if self.decouvrir_pokemon(pokemon_id):
                    nouveaux += 1
            else:
                nom = poke.get('name', '?') if isinstance(poke, dict) else getattr(poke, 'name', '?')
                orig = poke.get('original_name', '?') if isinstance(poke, dict) else getattr(poke, 'original_name', '?')
                non_resolus.append(f"{nom} (original: {orig})")

        if nouveaux:
            print(f" {nouveaux} Pokémon ajouté(s) au Pokédex depuis l'équipe.")
        if non_resolus:
            print(f"⚠ Pokémon non résolus (absents de POKEMON_NAME_TO_ID) : {non_resolus}")

    def _resoudre_id_depuis_save(self, poke) -> int | None:
        """
        Fonctionne avec un dict (save brute) OU un objet Pokemon instancié.
        Priorité : name (forme actuelle) → original_name (forme de base).
        Un seul ID retourné par Pokémon, pas de doublons.
        """
        def get_attr(key):
            if isinstance(poke, dict):
                return poke.get(key, '')
            return str(getattr(poke, key, ''))

        # 1. ID direct
        pid = get_attr('id')
        if pid:
            try:
                return int(pid)
            except (ValueError, TypeError):
                pass

        # 2. Cherche par name d'abord (forme actuelle = évoluée),
        #    puis original_name en fallback (forme de base)
        tous = {p.get('name', '').lower(): p.get('id') 
                for p in self.pokedex.obtenir_tous_les_pokemon()}

        for champ in ('name', 'original_name'):
            nom = get_attr(champ).strip().lower()
            if nom and nom in tous:
                return tous[nom]

        return None

    
    #  Boucle principale
   

    def run(self):
        while self.running:
            self.handle_input()
            if not self.pokedex_ouvert:
                self.map.update()
                self.player.update()
                self.bouton_pokedex.update()
                if self.pygame_surface:
                    self.bouton_pokedex.dessiner(self.pygame_surface)
            else:
                if self.pygame_surface:
                    self.pokedex_ui.dessiner(self.pygame_surface)
            self.screen.update()

    
    #  Gestion des entrées
    

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.pokedex_ouvert:
                        self.pokedex_ui.est_clique(event.pos)
                    elif self.bouton_pokedex.verifier_clic(event.pos):
                        self.ouvrir_pokedex()
                elif event.button == 4 and self.pokedex_ouvert:
                    self.pokedex_ui.defiler(-1)
                elif event.button == 5 and self.pokedex_ouvert:
                    self.pokedex_ui.defiler(1)

            elif event.type == pygame.MOUSEMOTION:
                if self.pokedex_ouvert:
                    self.pokedex_ui.verifier_survol(event.pos)
                else:
                    self.bouton_pokedex.verifier_survol(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.fermer_pokedex() if self.pokedex_ouvert else self.ouvrir_pokedex()
                elif event.key == pygame.K_ESCAPE:
                    if self.pokedex_ouvert:
                        self.fermer_pokedex()
                    else:
                        self.open_pause_menu()
                elif not self.pokedex_ouvert:
                    self.keylistener.add_key(event.key)

            elif event.type == pygame.KEYUP:
                if not self.pokedex_ouvert:
                    self.keylistener.remove_key(event.key)

    
    #  Menu pause
    

    def open_pause_menu(self):
        print("⏸  Menu pause ouvert")
        pause_menu = PauseMenu(self.player_name, self.pokemon, self.screen, self.pokedex)
        result_player, result_pokemon, result_pokedex = pause_menu.display()
        if result_player is None and result_pokemon is None:
            print(" Retour au menu principal...")
            self.running = False
        else:
            if result_player:
                self.player_name = result_player
            if result_pokemon:
                self.pokemon = result_pokemon
            if result_pokedex is not None:
                #  Remplace le Pokédex (peut être vierge si changement de save)
                self.pokedex = result_pokedex
                self.pokedex_ui.pokedex = self.pokedex  # Sync l'UI
            # Réenregistre l'équipe dans le Pokédex (vierge ou non)
            self._enregistrer_equipe_dans_pokedex()
            print("▶️  Reprise du jeu")

    
    #  Pokédex
    

    def ouvrir_pokedex(self):
        self.pokedex_ouvert = True
        print(" Pokédex ouvert")

    def fermer_pokedex(self):
        self.pokedex_ouvert = False
        self.pokedex.deselectionner_pokemon()
        print(" Pokédex fermé")

    def decouvrir_pokemon(self, pokemon_id: int) -> bool:
        """
        Marque un Pokémon comme découvert dans le Pokédex.
        À appeler lors d'une rencontre, d'une capture, ou au chargement.
        Retourne True si c'est une nouvelle découverte.
        """
        est_nouveau = self.pokedex.marquer_comme_trouve(pokemon_id)
        if est_nouveau:
            p = self.pokedex.obtenir_pokemon_par_id(pokemon_id)
            nom = p.get('name', str(pokemon_id)) if p else str(pokemon_id)
            print(f"✨ {nom} découvert et ajouté au Pokédex !")
        return est_nouveau

    
    #  Utilitaire : trouver la surface pygame
    

    def _find_pygame_surface(self):
        if isinstance(self.screen, pygame.Surface):
            return self.screen
        for attr in ('screen', 'surface', 'display', '_surface', '_screen'):
            obj = getattr(self.screen, attr, None)
            if isinstance(obj, pygame.Surface):
                print(f"✓ Surface trouvée via self.screen.{attr}")
                return obj
        surface = pygame.display.get_surface()
        if surface:
            print(" Surface trouvée via pygame.display.get_surface()")
            return surface
        if hasattr(self.screen, '__dict__'):
            for key, value in self.screen.__dict__.items():
                if isinstance(value, pygame.Surface):
                    print(f" Surface trouvée via self.screen.{key}")
                    return value
        print("⚠ Impossible de trouver la surface pygame!")
        return None