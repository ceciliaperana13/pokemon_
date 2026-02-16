import json
from typing import Dict, List, Optional


class Pokedex:
    """Classe pour gérer les données du Pokédex depuis pokedex.json"""
    
    def __init__(self, json_path: str = "back_end/data/pokedex.json"):
        """
        Initialise le Pokédex
        
        Args:
            json_path: Chemin vers le fichier pokedex.json
        """
        self.json_path = json_path
        self.pokemon_data: List[Dict] = []
        self.pokemon_selectionne: Optional[Dict] = None
        self.charger_donnees()
    
    def charger_donnees(self):
        """Charge les données depuis le fichier JSON"""
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
        """Sauvegarde les données dans le fichier JSON"""
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump({'pokemon': self.pokemon_data}, f, indent=4, ensure_ascii=False)
            print(f"✓ Pokédex sauvegardé")
        except Exception as e:
            print(f"⚠ Erreur de sauvegarde : {e}")
    
    def obtenir_tous_les_pokemon(self) -> List[Dict]:
        """
        Retourne la liste de tous les Pokémon
        
        Returns:
            Liste des Pokémon
        """
        return self.pokemon_data
    
    def obtenir_pokemon_par_id(self, pokemon_id: int) -> Optional[Dict]:
        """
        Récupère un Pokémon par son ID
        
        Args:
            pokemon_id: ID du Pokémon
            
        Returns:
            Dictionnaire du Pokémon ou None
        """
        for pokemon in self.pokemon_data:
            if pokemon.get('id') == pokemon_id:
                return pokemon
        return None
    
    def obtenir_pokemon_par_nom(self, nom: str) -> Optional[Dict]:
        """
        Récupère un Pokémon par son nom
        
        Args:
            nom: Nom du Pokémon
            
        Returns:
            Dictionnaire du Pokémon ou None
        """
        nom_lower = nom.lower()
        for pokemon in self.pokemon_data:
            if pokemon.get('name', '').lower() == nom_lower:
                return pokemon
        return None
    
    def marquer_comme_trouve(self, pokemon_id: int) -> bool:
        """
        Marque un Pokémon comme trouvé
        
        Args:
            pokemon_id: ID du Pokémon
            
        Returns:
            True si le Pokémon a été marqué, False sinon
        """
        pokemon = self.obtenir_pokemon_par_id(pokemon_id)
        if pokemon:
            if 'stats' not in pokemon:
                pokemon['stats'] = {}
            
            # Vérifier si c'est une nouvelle découverte
            est_nouvelle_decouverte = not pokemon['stats'].get('found', False)
            
            pokemon['stats']['found'] = True
            return est_nouvelle_decouverte
        return False
    
    def est_trouve(self, pokemon_id: int) -> bool:
        """
        Vérifie si un Pokémon a été trouvé
        
        Args:
            pokemon_id: ID du Pokémon
            
        Returns:
            True si trouvé, False sinon
        """
        pokemon = self.obtenir_pokemon_par_id(pokemon_id)
        if pokemon and 'stats' in pokemon:
            return pokemon['stats'].get('found', False)
        return False
    
    def obtenir_pokemon_trouves(self) -> List[Dict]:
        """
        Retourne la liste des Pokémon trouvés
        
        Returns:
            Liste des Pokémon trouvés
        """
        return [p for p in self.pokemon_data 
                if p.get('stats', {}).get('found', False)]
    
    def obtenir_pokemon_non_trouves(self) -> List[Dict]:
        """
        Retourne la liste des Pokémon non trouvés
        
        Returns:
            Liste des Pokémon non trouvés
        """
        return [p for p in self.pokemon_data 
                if not p.get('stats', {}).get('found', False)]
    
    def nombre_pokemon(self) -> int:
        """
        Retourne le nombre total de Pokémon
        
        Returns:
            Nombre de Pokémon
        """
        return len(self.pokemon_data)
    
    def nombre_pokemon_trouves(self) -> int:
        """
        Retourne le nombre de Pokémon trouvés
        
        Returns:
            Nombre de Pokémon trouvés
        """
        return len(self.obtenir_pokemon_trouves())
    
    def pourcentage_completion(self) -> float:
        """
        Calcule le pourcentage de complétion du Pokédex
        
        Returns:
            Pourcentage (0-100)
        """
        total = self.nombre_pokemon()
        if total == 0:
            return 0.0
        return (self.nombre_pokemon_trouves() / total) * 100
    
    def selectionner_pokemon(self, pokemon: Dict):
        """
        Sélectionne un Pokémon pour afficher ses détails
        
        Args:
            pokemon: Dictionnaire du Pokémon
        """
        self.pokemon_selectionne = pokemon
    
    def deselectionner_pokemon(self):
        """Désélectionne le Pokémon actuel"""
        self.pokemon_selectionne = None
    
    def obtenir_pokemon_selectionne(self) -> Optional[Dict]:
        """
        Retourne le Pokémon actuellement sélectionné
        
        Returns:
            Pokémon sélectionné ou None
        """
        return self.pokemon_selectionne
    
    def obtenir_pokemon_par_type(self, type_pokemon: str) -> List[Dict]:
        """
        Retourne tous les Pokémon d'un type donné
        
        Args:
            type_pokemon: Type de Pokémon (ex: "Feu", "Eau")
            
        Returns:
            Liste des Pokémon du type spécifié
        """
        type_lower = type_pokemon.lower()
        resultat = []
        
        for pokemon in self.pokemon_data:
            types = pokemon.get('type', [])
            # Gérer le cas où type est une string ou une liste
            if isinstance(types, str):
                types = [types]
            
            for t in types:
                if t.lower() == type_lower:
                    resultat.append(pokemon)
                    break
        
        return resultat
    
    def obtenir_statistiques(self) -> Dict:
        """
        Retourne des statistiques sur le Pokédex
        
        Returns:
            Dictionnaire avec les statistiques
        """
        trouves = self.obtenir_pokemon_trouves()
        
        # Compter les types
        types_count = {}
        for pokemon in trouves:
            types = pokemon.get('type', [])
            if isinstance(types, str):
                types = [types]
            for t in types:
                t_cap = t.capitalize()
                types_count[t_cap] = types_count.get(t_cap, 0) + 1
        
        return {
            'total': self.nombre_pokemon(),
            'trouves': len(trouves),
            'non_trouves': self.nombre_pokemon() - len(trouves),
            'pourcentage': self.pourcentage_completion(),
            'types_distribution': types_count
        }
    
    def reinitialiser_progression(self):
        """Réinitialise tous les Pokémon comme non trouvés"""
        for pokemon in self.pokemon_data:
            if 'stats' in pokemon:
                pokemon['stats']['found'] = False
        print("✓ Progression réinitialisée")
    
    def debloquer_tous(self):
        """Marque tous les Pokémon comme trouvés (pour le debug)"""
        for pokemon in self.pokemon_data:
            if 'stats' not in pokemon:
                pokemon['stats'] = {}
            pokemon['stats']['found'] = True
        print("✓ Tous les Pokémon débloqués")