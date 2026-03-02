import pygame, sys
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

        if hasattr(self.screen, 'get_width') and hasattr(self.screen, 'get_height'):
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
        elif hasattr(self.screen, 'width') and hasattr(self.screen, 'height'):
            screen_width = self.screen.width
            screen_height = self.screen.height
        else:
            screen_width, screen_height = 1200, 800

        self.pygame_surface = self._find_pygame_surface()
        self.pokedex_ui = CustomizerPokedex(self.pokedex, screen_width, screen_height)
        self.pokedex_button = PokedexButton(
            screen_width - 130, screen_height - 130,
            image_path="assets/logo/pokedex.png", size=100
        )
        self.pokedex_open = False

        print(f"✓ Pokédex interface initialized ({screen_width}x{screen_height})")
        self._register_team_in_pokedex()

    def _register_team_in_pokedex(self):
        if not self.pokemon:
            print("⚠ No Pokémon in the loaded team.")
            return

        if isinstance(self.pokemon, dict):
            pokemon_to_process = list(self.pokemon.values())
        elif isinstance(self.pokemon, list):
            pokemon_to_process = self.pokemon
        else:
            pokemon_to_process = [self.pokemon]

        new_discoveries = 0
        unresolved = []

        for poke in pokemon_to_process:
            pokemon_id = self._resolve_id_from_save(poke)
            if pokemon_id:
                if self.discover_pokemon(pokemon_id):
                    new_discoveries += 1
            else:
                name = poke.get('name', '?') if isinstance(poke, dict) else getattr(poke, 'name', '?')
                original = poke.get('original_name', '?') if isinstance(poke, dict) else getattr(poke, 'original_name', '?')
                unresolved.append(f"{name} (original: {original})")

        if new_discoveries:
            print(f" {new_discoveries} Pokémon added to the Pokédex from the team.")
        if unresolved:
            print(f"⚠ Unresolved Pokémon (missing from POKEMON_NAME_TO_ID): {unresolved}")

    def _resolve_id_from_save(self, poke) -> int | None:
        def get_attr(key):
            if isinstance(poke, dict):
                return poke.get(key, '')
            return str(getattr(poke, key, ''))

        pid = get_attr('id')
        if pid:
            try:
                return int(pid)
            except (ValueError, TypeError):
                pass

        all_pokemon = {p.get('name', '').lower(): p.get('id')
                       for p in self.pokedex.get_all_pokemon()}

        for field in ('name', 'original_name'):
            name = get_attr(field).strip().lower()
            if name and name in all_pokemon:
                return all_pokemon[name]

        return None

    # ─────────────────────────────────────────────────────────────
    #  Main loop
    # ─────────────────────────────────────────────────────────────

    def run(self):
        while self.running:
            self.handle_input()

            if not self.running:
                break

            if not self.pokedex_open:
                self.map.update()
                self.player.update()
                self.pokedex_button.update()
                if self.pygame_surface:
                    self.pokedex_button.draw(self.pygame_surface)
            else:
                if self.pygame_surface:
                    self.pokedex_ui.draw(self.pygame_surface)
            self.screen.update()

    # ─────────────────────────────────────────────────────────────
    #  Input handling
    # ─────────────────────────────────────────────────────────────

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.pokedex_open:
                        self.pokedex_ui.check_click(event.pos)
                    elif self.pokedex_button.check_click(event.pos):
                        self.open_pokedex()
                elif event.button == 4 and self.pokedex_open:
                    self.pokedex_ui.scroll(-1)
                elif event.button == 5 and self.pokedex_open:
                    self.pokedex_ui.scroll(1)

            elif event.type == pygame.MOUSEMOTION:
                if self.pokedex_open:
                    self.pokedex_ui.check_hover(event.pos)
                else:
                    self.pokedex_button.check_hover(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.close_pokedex() if self.pokedex_open else self.open_pokedex()
                elif event.key == pygame.K_ESCAPE:
                    if self.pokedex_open:
                        self.close_pokedex()
                    else:
                        self.open_pause_menu()
                elif not self.pokedex_open:
                    self.keylistener.add_key(event.key)

            elif event.type == pygame.KEYUP:
                if not self.pokedex_open:
                    self.keylistener.remove_key(event.key)

    # ─────────────────────────────────────────────────────────────
    #  Pause menu
    # ─────────────────────────────────────────────────────────────

    def open_pause_menu(self):
        print("⏸  Pause menu opened")
        pause_menu = PauseMenu(self.player_name, self.pokemon, self.screen, self.pokedex)
        result_player, result_pokemon, result_pokedex = pause_menu.display()
        if result_player is None and result_pokemon is None:
            print(" Returning to main menu...")
            self.running = False
        else:
            if result_player:
                self.player_name = result_player
            if result_pokemon:
                self.pokemon = result_pokemon
            if result_pokedex is not None:
                self.pokedex = result_pokedex
                self.pokedex_ui.pokedex = self.pokedex
            self._register_team_in_pokedex()
            print("▶️  Resuming game")

    # ─────────────────────────────────────────────────────────────
    #  Pokédex
    # ─────────────────────────────────────────────────────────────

    def open_pokedex(self):
        self.pokedex_open = True
        print(" Pokédex opened")

    def close_pokedex(self):
        self.pokedex_open = False
        self.pokedex.deselect_pokemon()
        print(" Pokédex closed")

    def discover_pokemon(self, pokemon_id: int) -> bool:
        is_new = self.pokedex.mark_as_found(pokemon_id)
        if is_new:
            p = self.pokedex.get_pokemon_by_id(pokemon_id)
            name = p.get('name', str(pokemon_id)) if p else str(pokemon_id)
            print(f"✨ {name} discovered and added to the Pokédex!")
        return is_new

    # ─────────────────────────────────────────────────────────────
    #  Utility: find the pygame surface
    # ─────────────────────────────────────────────────────────────

    def _find_pygame_surface(self):
        if isinstance(self.screen, pygame.Surface):
            return self.screen
        for attr in ('screen', 'surface', 'display', '_surface', '_screen'):
            obj = getattr(self.screen, attr, None)
            if isinstance(obj, pygame.Surface):
                print(f"✓ Surface found via self.screen.{attr}")
                return obj
        surface = pygame.display.get_surface()
        if surface:
            print(" Surface found via pygame.display.get_surface()")
            return surface
        if hasattr(self.screen, '__dict__'):
            for key, value in self.screen.__dict__.items():
                if isinstance(value, pygame.Surface):
                    print(f" Surface found via self.screen.{key}")
                    return value
        print("⚠ Unable to find the pygame surface!")
        return None