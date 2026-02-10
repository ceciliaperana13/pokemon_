import json

def charger_pokedex(fichier):
    """
    Charge les données du Pokédex depuis un fichier JSON
    
    Args:
        fichier (str): Chemin vers le fichier JSON
        
    Returns:
        list: Liste des Pokémon
    """
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Si le JSON contient un dictionnaire avec une clé 'pokemon'
    if isinstance(data, dict) and 'pokemon' in data:
        return data['pokemon']
    
    # Si le JSON contient directement une liste
    if isinstance(data, list):
        return data
    
    return []


class Pokedex:
    """Classe pour gérer les données du Pokédex"""
    
    def __init__(self, fichier_json):
        """
        Initialise le Pokédex
        
        Args:
            fichier_json (str): Chemin vers le fichier JSON
        """
        self.pokemon_list = charger_pokedex(fichier_json)
        self.pokemon_selectionne = None
    
    def obtenir_pokemon(self, pokemon_id):
        """
        Récupère un Pokémon par son ID
        
        Args:
            pokemon_id (int): ID du Pokémon
            
        Returns:
            dict: Données du Pokémon ou None
        """
        for pokemon in self.pokemon_list:
            if pokemon.get('id') == pokemon_id:
                return pokemon
        return None
    
    def obtenir_pokemon_par_nom(self, nom):
        """
        Récupère un Pokémon par son nom
        
        Args:
            nom (str): Nom du Pokémon
            
        Returns:
            dict: Données du Pokémon ou None
        """
        for pokemon in self.pokemon_list:
            if pokemon.get('name', '').lower() == nom.lower():
                return pokemon
        return None
    
    def obtenir_tous_les_pokemon(self):
        """
        Retourne tous les Pokémon
        
        Returns:
            list: Liste de tous les Pokémon
        """
        return self.pokemon_list
    
    def filtrer_par_type(self, type_pokemon):
        """
        Filtre les Pokémon par type
        
        Args:
            type_pokemon (str): Type de Pokémon
            
        Returns:
            list: Liste des Pokémon du type spécifié
        """
        return [p for p in self.pokemon_list if type_pokemon.capitalize() in [t.capitalize() for t in p.get('type', [])]]
    
    def nombre_pokemon(self):
        """
        Retourne le nombre total de Pokémon
        
        Returns:
            int: Nombre de Pokémon
        """
        return len(self.pokemon_list)
    
    def selectionner_pokemon(self, pokemon):
        """
        Sélectionne un Pokémon
        
        Args:
            pokemon (dict): Pokémon à sélectionner
        """
        self.pokemon_selectionne = pokemon
        print(f" Pokémon sélectionné dans Pokedex: {pokemon.get('name')}")  # DEBUG
    
    def deselectionner_pokemon(self):
        """Désélectionne le Pokémon actuel"""
        self.pokemon_selectionne = None
        print(" Pokémon désélectionné")  # DEBUG
    
    def obtenir_pokemon_selectionne(self):
        """
        Retourne le Pokémon actuellement sélectionné
        
        Returns:
            dict: Pokémon sélectionné ou None
        """
        return self.pokemon_selectionne