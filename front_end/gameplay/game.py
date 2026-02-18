import pygame
from .keylistener import KeyListener
from .map import Map
from .player import Player
from .CustumizerPokedex import CustomizerPokedex
from .pokedexButton import PokedexButton
from front_end.menu.pause_menu import PauseMenu


# ══════════════════════════════════════════════════════════════════════════════
#  Table de correspondance : nom anglais (save) → ID Pokédex (pokedex.json FR)
#  Couvre le nom actuel ET le nom original (avant évolution)
# ══════════════════════════════════════════════════════════════════════════════
POKEMON_NAME_TO_ID = {
    # Starters & évolutions
    "bulbasaur": 1,   "ivysaur": 2,     "venusaur": 3,
    "charmander": 4,  "charmeleon": 5,  "charizard": 6,
    "squirtle": 7,    "wartortle": 8,   "blastoise": 9,
    # Insectes
    "caterpie": 10,   "metapod": 11,    "butterfree": 12,
    "weedle": 13,     "kakuna": 14,     "beedrill": 15,
    # Oiseaux
    "pidgey": 16,     "pidgeotto": 17,  "pidgeot": 18,
    # Rongeurs
    "rattata": 19,    "raticate": 20,
    # Rapaces
    "spearow": 21,    "fearow": 22,
    # Serpents
    "ekans": 23,      "arbok": 24,
    # Électriques
    "pikachu": 25,    "raichu": 26,
    # Taupes
    "sandshrew": 27,  "sandslash": 28,
    # Nidoran
    "nidoran": 29,    "nidorino": 30,   "nidoking": 31,
    # Fées
    "clefairy": 32,   "clefable": 33,
    # Renards
    "vulpix": 34,     "ninetales": 35,
    # Ballons
    "jigglypuff": 36, "wigglytuff": 37,
    # Chauves-souris
    "zubat": 38,      "golbat": 39,
    # Plantes/Poison
    "oddish": 40,     "gloom": 41,      "vileplume": 42,
    "paras": 43,      "parasect": 44,
    "venonat": 45,    "venomoth": 46,
    # Taupes fouisseuses
    "diglett": 47,    "dugtrio": 48,
    # Chats
    "meowth": 49,     "persian": 50,
    # Canards
    "psyduck": 51,    "golduck": 52,
    # Singes
    "mankey": 53,     "primeape": 54,
    # Chiens de feu
    "growlithe": 55,  "arcanine": 56,
    # Têtards
    "poliwag": 57,    "poliwhirl": 58,  "poliwrath": 59,
    # Psy
    "abra": 60,       "kadabra": 61,    "alakazam": 62,
    # Combat
    "machop": 63,     "machoke": 64,    "machamp": 65,
    # Plantes grimpantes
    "bellsprout": 66, "weepinbell": 67, "victreebel": 68,
    # Méduses
    "tentacool": 69,  "tentacruel": 70,
    # Rochers
    "geodude": 71,    "graveler": 72,   "golem": 73,
    # Chevaux
    "ponyta": 74,     "rapidash": 75,
    # Ramoloss
    "slowpoke": 76,   "slowbro": 77,
    # Magnéti
    "magnemite": 78,  "magneton": 79,
    # Canard poireau
    "farfetch'd": 80, "farfetchd": 80,
    # Doduo
    "doduo": 81,      "dodrio": 82,
    # Phoques
    "seel": 83,       "dewgong": 84,
    # Boue
    "grimer": 85,     "muk": 86,
    # Coquillages
    "shellder": 87,   "cloyster": 88,
    # Fantômes
    "gastly": 89,     "haunter": 90,    "gengar": 91,
    # Onix
    "onix": 92,
    # Endormeurs
    "drowzee": 93,    "hypno": 94,
    # Crabes
    "krabby": 95,     "kingler": 96,
    # Voltorbe
    "voltorb": 97,    "electrode": 98,
    # Nœux-nœux
    "exeggcute": 99,  "exeggutor": 100,
    # Ossatueur
    "cubone": 101,    "marowak": 102,
    # Combat 2
    "hitmonlee": 103, "hitmonchan": 104,
    # Excelangue
    "lickitung": 105,
    # Smog
    "koffing": 106,   "weezing": 107,
    # Rhinocorne
    "rhyhorn": 108,   "rhydon": 109,
    # Leveinard
    "chansey": 110,
    # Saquedeneu
    "tangela": 111,
    # Kangourex
    "kangaskhan": 112,
    # Hippocampes
    "horsea": 113,    "seadra": 114,
    # Poissons rouges
    "goldeen": 115,   "seaking": 116,
    # Étoiles de mer
    "staryu": 117,    "starmie": 118,
    # M. Mime
    "mr. mime": 119,  "mr mime": 119,   "mrmime": 119,
    # Insécateur
    "scyther": 120,
    # Lippoutou
    "jynx": 121,
    # Élektek
    "electabuzz": 122,
    # Magmar
    "magmar": 123,
    # Scarabrute
    "pinsir": 124,
    # Tauros
    "tauros": 125,
    # Magicarpe / Léviator
    "magikarp": 126,  "gyarados": 127,
    # Lokhlass
    "lapras": 128,
    # Métamorph
    "ditto": 129,
    # Évoli & évolutions
    "eevee": 130,     "vaporeon": 131,  "jolteon": 132,  "flareon": 133,
    # Porygon
    "porygon": 134,
    # Fossiles
    "omanyte": 135,   "omastar": 136,
    "kabuto": 137,    "kabutops": 138,
    # Ptéra
    "aerodactyl": 139,
    # Ronflex
    "snorlax": 140,
    # Légendaires oiseaux
    "articuno": 141,  "zapdos": 142,    "moltres": 143,
    # Dragons
    "dratini": 144,   "dragonair": 145, "dragonite": 146,
    # Légendaires psy
    "mewtwo": 147,    "mew": 148,
}


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
            print(f"✨ {nouveaux} Pokémon ajouté(s) au Pokédex depuis l'équipe.")
        if non_resolus:
            print(f"⚠ Pokémon non résolus (absents de POKEMON_NAME_TO_ID) : {non_resolus}")

    @staticmethod
    def _resoudre_id_depuis_save(poke) -> int | None:
        """
        Fonctionne avec un dict (save brute) OU un objet Pokemon instancié.
        Ordre : id direct → original_name → name
        """
        def get_attr(key):
            if isinstance(poke, dict):
                return poke.get(key, '')
            return str(getattr(poke, key, ''))

        # 1. ID direct
        pid = get_attr('id')
        if pid:
            return int(pid)

        # 2. original_name puis name
        for champ in ('original_name', 'name'):
            valeur = get_attr(champ).strip().lower()
            if valeur in POKEMON_NAME_TO_ID:
                return POKEMON_NAME_TO_ID[valeur]

        return None

    # ══════════════════════════════════════════════════════════════════════════
    #  Boucle principale
    # ══════════════════════════════════════════════════════════════════════════

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

    # ══════════════════════════════════════════════════════════════════════════
    #  Gestion des entrées
    # ══════════════════════════════════════════════════════════════════════════

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

    # ══════════════════════════════════════════════════════════════════════════
    #  Menu pause
    # ══════════════════════════════════════════════════════════════════════════

    def open_pause_menu(self):
        print("⏸️  Menu pause ouvert")
        pause_menu = PauseMenu(self.player_name, self.pokemon, self.screen, self.pokedex)
        result_player, result_pokemon = pause_menu.display()
        if result_player is None and result_pokemon is None:
            print("🔙 Retour au menu principal...")
            self.running = False
        else:
            if result_player:
                self.player_name = result_player
            if result_pokemon:
                self.pokemon = result_pokemon
                self._enregistrer_equipe_dans_pokedex()
            print("▶️  Reprise du jeu")

    # ══════════════════════════════════════════════════════════════════════════
    #  Pokédex
    # ══════════════════════════════════════════════════════════════════════════

    def ouvrir_pokedex(self):
        self.pokedex_ouvert = True
        print("📱 Pokédex ouvert")

    def fermer_pokedex(self):
        self.pokedex_ouvert = False
        self.pokedex.deselectionner_pokemon()
        print("📱 Pokédex fermé")

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

    # ══════════════════════════════════════════════════════════════════════════
    #  Utilitaire : trouver la surface pygame
    # ══════════════════════════════════════════════════════════════════════════

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
            print("✓ Surface trouvée via pygame.display.get_surface()")
            return surface
        if hasattr(self.screen, '__dict__'):
            for key, value in self.screen.__dict__.items():
                if isinstance(value, pygame.Surface):
                    print(f"✓ Surface trouvée via self.screen.{key}")
                    return value
        print("⚠ Impossible de trouver la surface pygame!")
        return None