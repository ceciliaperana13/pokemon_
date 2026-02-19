import json
from typing import Dict, List, Optional


class Pokedex:
    """Class to manage Pokedex data loaded from a JSON file."""

    def __init__(self, json_path: str = "back_end/data/pokedex.json"):
        self.json_path = json_path
        self.pokemon_data: List[Dict] = []
        self.selected_pokemon: Optional[Dict] = None
        self.load_data()

    # ─────────────────────────── Persistence ───────────────────────────

    def load_data(self):
        """
        Loads data from the JSON file.
        Initializes the 'found' status to False for all entries to start fresh in memory.
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.pokemon_data = data.get('pokemon', [])
            
            # Force all 'found' statuses to False — progression is managed in runtime memory
            for p in self.pokemon_data:
                p.setdefault('stats', {})['found'] = False
            print(f"✓ Pokedex loaded: {len(self.pokemon_data)} Pokémon")
        except FileNotFoundError:
            print(f"⚠ File {self.json_path} not found")
            self.pokemon_data = []
        except json.JSONDecodeError as e:
            print(f"⚠ JSON read error: {e}")
            self.pokemon_data = []

    def save_data(self):
        """Saves current memory state back to the JSON file."""
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump({'pokemon': self.pokemon_data}, f, indent=4, ensure_ascii=False)
            print("✓ Pokedex saved to disk")
        except Exception as e:
            print(f"⚠ Save error: {e}")

    def load_save_state(self, saved_pokedex: List[Dict]):
        """Updates the Pokedex state using data from a save file."""
        for pokemon_save in saved_pokedex or []:
            pokemon = self.get_pokemon_by_id(pokemon_save.get('id'))
            if pokemon:
                pokemon.setdefault('stats', {})['found'] = (
                    pokemon_save.get('stats', {}).get('found', False)
                )
        print("✓ Pokedex state updated from save file")

    def get_save_data(self) -> List[Dict]:
        """Prepares a minimal data list for saving progression."""
        return [
            {"id": p.get("id"), "stats": {"found": p.get("stats", {}).get("found", False)}}
            for p in self.pokemon_data
        ]

    # ─────────────────────────── Accessors ────────────────────────────

    def get_all_pokemon(self) -> List[Dict]:
        """Returns the full list of Pokémon data."""
        return self.pokemon_data

    def get_pokemon_by_id(self, pokemon_id: int) -> Optional[Dict]:
        """Finds a Pokémon by its unique ID."""
        return next((p for p in self.pokemon_data if p.get('id') == pokemon_id), None)

    def get_pokemon_by_name(self, name: str) -> Optional[Dict]:
        """Finds a Pokémon by its name (case-insensitive)."""
        name_lower = name.lower()
        return next((p for p in self.pokemon_data if p.get('name', '').lower() == name_lower), None)

    def get_pokemon_by_type(self, pokemon_type: str) -> List[Dict]:
        """Returns a list of Pokémon matching a specific type."""
        type_lower = pokemon_type.lower()
        return [
            p for p in self.pokemon_data
            if type_lower in [t.lower() for t in self._normalize_types(p.get('type', []))]
        ]

    def get_found_pokemon(self) -> List[Dict]:
        """Returns all Pokémon marked as discovered."""
        return [p for p in self.pokemon_data if p.get('stats', {}).get('found', False)]

    def get_unfound_pokemon(self) -> List[Dict]:
        """Returns all Pokémon that haven't been discovered yet."""
        return [p for p in self.pokemon_data if not p.get('stats', {}).get('found', False)]

    # ─────────────────────────── Selection ─────────────────────────────

    def select_pokemon(self, pokemon: Dict):
        """Sets the currently active Pokémon in the UI."""
        self.selected_pokemon = pokemon

    def deselect_pokemon(self):
        """Clears the current selection."""
        self.selected_pokemon = None

    def get_selected_pokemon(self) -> Optional[Dict]:
        """Returns the currently active Pokémon."""
        return self.selected_pokemon

    # ─────────────────────────── Progression ───────────────────────────

    def is_found(self, pokemon_id: int) -> bool:
        """Checks if a specific Pokémon ID has been discovered."""
        pokemon = self.get_pokemon_by_id(pokemon_id)
        return bool(pokemon and pokemon.get('stats', {}).get('found', False))

    def mark_as_found(self, pokemon_id: int) -> bool:
        """Marks a Pokémon as found. Returns True if it was previously undiscovered."""
        pokemon = self.get_pokemon_by_id(pokemon_id)
        if not pokemon:
            return False
        pokemon.setdefault('stats', {})
        is_new_discovery = not pokemon['stats'].get('found', False)
        pokemon['stats']['found'] = True
        return is_new_discovery

    def reset_progression(self):
        """Resets all Pokémon discovery statuses to False."""
        for p in self.pokemon_data:
            p.setdefault('stats', {})['found'] = False
        print("✓ Progression reset")

    def unlock_all(self):
        """Cheat/Debug: Marks every Pokémon in the data as found."""
        for p in self.pokemon_data:
            p.setdefault('stats', {})['found'] = True
        print("✓ All Pokémon unlocked")

    # ─────────────────────────── Statistics ──────────────────────────

    def total_count(self) -> int:
        """Returns the total number of Pokémon in the database."""
        return len(self.pokemon_data)

    def found_count(self) -> int:
        """Returns the count of discovered Pokémon."""
        return len(self.get_found_pokemon())

    def completion_percentage(self) -> float:
        """Calculates the percentage of the Pokedex completed."""
        total = self.total_count()
        return (self.found_count() / total * 100) if total else 0.0

    def get_statistics(self) -> Dict:
        """Compiles a comprehensive report of Pokedex progress."""
        found_list = self.get_found_pokemon()
        type_distribution: Dict[str, int] = {}
        
        for p in found_list:
            for t in self._normalize_types(p.get('type', [])):
                t_cap = t.capitalize()
                type_distribution[t_cap] = type_distribution.get(t_cap, 0) + 1
                
        return {
            'total': self.total_count(),
            'found': len(found_list),
            'missing': self.total_count() - len(found_list),
            'percentage': self.completion_percentage(),
            'type_distribution': type_distribution,
        }

    # ─────────────────────────── Utilities ───────────────────────────

    @staticmethod
    def _normalize_types(types) -> List[str]:
        """Ensures types are returned as a list of strings, whether input is a string or list."""
        return [types] if isinstance(types, str) else list(types)