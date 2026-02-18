import json
from typing import Dict, List, Optional


class Pokedex:
    """Classe pour gérer les données du Pokédex depuis pokedex.json"""

    def __init__(self, json_path: str = "back_end/data/pokedex.json"):
        self.json_path = json_path
        self.pokemon_data: List[Dict] = []
        self.pokemon_selectionne: Optional[Dict] = None
        self.charger_donnees()


    def charger_donnees(self):
        """Charge les données depuis le fichier JSON."""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.pokemon_data = data.get('pokemon', [])
            print(f"✓ Pokédex chargé : {len(self.pokemon_data)} Pokémon")
        except FileNotFoundError:
            print(f"⚠ Fichier {self.json_path} non trouvé")
            self.pokemon_data = []
        except json.JSONDecodeError as e:
            print(f"⚠ Erreur de lecture JSON : {e}")
            self.pokemon_data = []

    def sauvegarder_donnees(self):
        """Sauvegarde les données dans le fichier JSON."""
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump({'pokemon': self.pokemon_data}, f, indent=4, ensure_ascii=False)
            print("✓ Pokédex sauvegardé")
        except Exception as e:
            print(f"⚠ Erreur de sauvegarde : {e}")
     #changement a venir ici le chargement de sauvegarde dois ce faire a partir player_pokedex.json
     
    def charger_donnees_sauvegarde(self, pokedex_sauvegarde: List[Dict]):
        """Met à jour l'état du Pokédex à partir d'une sauvegarde."""
        for pokemon_save in pokedex_sauvegarde or []:
            pokemon = self.obtenir_pokemon_par_id(pokemon_save.get('id'))
            if pokemon:
                pokemon.setdefault('stats', {})['found'] = (
                    pokemon_save.get('stats', {}).get('found', False)
                )
        print("✓ État du Pokédex mis à jour depuis la sauvegarde")

    def obtenir_donnees_sauvegarde(self) -> List[Dict]:
        """Prépare les données minimales pour la sauvegarde."""
        return [
            {"id": p.get("id"), "stats": {"found": p.get("stats", {}).get("found", False)}}
            for p in self.pokemon_data
        ]

    # ─────────────────────────── Accesseurs ────────────────────────────

    def obtenir_tous_les_pokemon(self) -> List[Dict]:
        return self.pokemon_data

    def obtenir_pokemon_par_id(self, pokemon_id: int) -> Optional[Dict]:
        return next((p for p in self.pokemon_data if p.get('id') == pokemon_id), None)

    def obtenir_pokemon_par_nom(self, nom: str) -> Optional[Dict]:
        nom_lower = nom.lower()
        return next((p for p in self.pokemon_data if p.get('name', '').lower() == nom_lower), None)

    def obtenir_pokemon_par_type(self, type_pokemon: str) -> List[Dict]:
        type_lower = type_pokemon.lower()
        return [
            p for p in self.pokemon_data
            if type_lower in [t.lower() for t in self._normaliser_types(p.get('type', []))]
        ]

    def obtenir_pokemon_trouves(self) -> List[Dict]:
        return [p for p in self.pokemon_data if p.get('stats', {}).get('found', False)]

    def obtenir_pokemon_non_trouves(self) -> List[Dict]:
        return [p for p in self.pokemon_data if not p.get('stats', {}).get('found', False)]

    # ─────────────────────────── Sélection ─────────────────────────────

    def selectionner_pokemon(self, pokemon: Dict):
        self.pokemon_selectionne = pokemon

    def deselectionner_pokemon(self):
        self.pokemon_selectionne = None

    def obtenir_pokemon_selectionne(self) -> Optional[Dict]:
        return self.pokemon_selectionne

    # ─────────────────────────── Progression ───────────────────────────

    def est_trouve(self, pokemon_id: int) -> bool:
        pokemon = self.obtenir_pokemon_par_id(pokemon_id)
        return bool(pokemon and pokemon.get('stats', {}).get('found', False))

    def marquer_comme_trouve(self, pokemon_id: int) -> bool:
        """Marque un Pokémon comme trouvé. Retourne True si c'est une nouveauté."""
        pokemon = self.obtenir_pokemon_par_id(pokemon_id)
        if not pokemon:
            return False
        pokemon.setdefault('stats', {})
        nouvelle_decouverte = not pokemon['stats'].get('found', False)
        pokemon['stats']['found'] = True
        return nouvelle_decouverte

    def reinitialiser_progression(self):
        for p in self.pokemon_data:
            p.setdefault('stats', {})['found'] = False
        print("✓ Progression réinitialisée")

    def debloquer_tous(self):
        for p in self.pokemon_data:
            p.setdefault('stats', {})['found'] = True
        print("✓ Tous les Pokémon débloqués")

    # ─────────────────────────── Statistiques ──────────────────────────

    def nombre_pokemon(self) -> int:
        return len(self.pokemon_data)

    def nombre_pokemon_trouves(self) -> int:
        return len(self.obtenir_pokemon_trouves())

    def pourcentage_completion(self) -> float:
        total = self.nombre_pokemon()
        return (self.nombre_pokemon_trouves() / total * 100) if total else 0.0

    def obtenir_statistiques(self) -> Dict:
        trouves = self.obtenir_pokemon_trouves()
        types_count: Dict[str, int] = {}
        for p in trouves:
            for t in self._normaliser_types(p.get('type', [])):
                t_cap = t.capitalize()
                types_count[t_cap] = types_count.get(t_cap, 0) + 1
        return {
            'total': self.nombre_pokemon(),
            'trouves': len(trouves),
            'non_trouves': self.nombre_pokemon() - len(trouves),
            'pourcentage': self.pourcentage_completion(),
            'types_distribution': types_count,
        }

    # ─────────────────────────── Utilitaires ───────────────────────────

    @staticmethod
    def _normaliser_types(types) -> List[str]:
        """Normalise types en liste de strings, qu'il s'agisse d'une str ou d'une list."""
        return [types] if isinstance(types, str) else list(types)