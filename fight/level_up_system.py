import random
from typing import Dict, List, Optional


class LevelUpSystem:
    """Gère la montée de niveau des Pokémon."""
    
    MAX_LEVEL = 100
    
    @staticmethod
    def exp_required_for_level(level: int) -> int:
        """
        Calcule l'expérience totale requise pour atteindre un niveau.
        
        Formule : 4 × level³ / 5
        
        Args:
            level: Le niveau cible
            
        Returns:
            L'expérience totale nécessaire
        """
        if level <= 1:
            return 0
        return int(4 * (level ** 3) / 5)
    
    @staticmethod
    def exp_for_next_level(current_level: int) -> int:
        """
        Calcule l'expérience nécessaire pour passer au niveau suivant.
        
        Args:
            current_level: Le niveau actuel
            
        Returns:
            L'expérience nécessaire pour le prochain niveau
        """
        return (LevelUpSystem.exp_required_for_level(current_level + 1) - 
                LevelUpSystem.exp_required_for_level(current_level))
    
    @staticmethod
    def calculate_exp_gain(defeated_pokemon: Dict, winner_pokemon: Dict, 
                          is_wild: bool = True) -> int:
        """
        Calcule l'expérience gagnée après avoir vaincu un Pokémon.
        
        Formule : (base_exp × defeated_level) / 7
        Bonus dresseur : ×1.5
        
        Args:
            defeated_pokemon: Le Pokémon vaincu (doit contenir 'level' et 'base_exp')
            winner_pokemon: Le Pokémon vainqueur
            is_wild: True si Pokémon sauvage, False si dresseur
            
        Returns:
            L'expérience gagnée
        """
        base_exp = defeated_pokemon.get('base_exp', 100)
        defeated_level = defeated_pokemon.get('level', 5)
        
        exp_gain = (base_exp * defeated_level) / 7
        
        if not is_wild:
            exp_gain *= 1.5
        
        return int(exp_gain)
    
    @staticmethod
    def calculate_stat_gains(pokemon: Dict) -> Dict[str, int]:
        """
        Calcule les gains de statistiques lors d'une montée de niveau.
        
        Formule : Gain = max(1, base_stat / 20 + random(-1, 1))
        
        Args:
            pokemon: Le dictionnaire du Pokémon (doit contenir 'base_stats')
            
        Returns:
            Dictionnaire des gains {'hp': X, 'attack': Y, ...}
        """
        base_stats = pokemon.get('base_stats', {
            'hp': 45,
            'attack': 49,
            'defense': 49,
            'sp_attack': 65,
            'sp_defense': 65,
            'speed': 45
        })
        
        stat_gains = {}
        
        for stat, base_value in base_stats.items():
            gain = max(1, int(base_value / 20))
            variation = random.randint(-1, 1)
            gain = max(1, gain + variation)
            stat_gains[stat] = gain
        
        return stat_gains
    
    @staticmethod
    def check_new_move(pokemon: Dict, level: int) -> Optional[Dict]:
        """
        Vérifie si le Pokémon apprend une nouvelle attaque à ce niveau.
        
        Nouvelles attaques tous les 5 niveaux (10, 15, 20, etc.)
        
        Args:
            pokemon: Le dictionnaire du Pokémon
            level: Le niveau actuel
            
        Returns:
            Dictionnaire de la nouvelle attaque ou None
        """
        if level % 5 != 0 or level <= 5:
            return None
        
        move_pools = {
            'fire': [
                {'name': 'Flamethrower', 'power': 90, 'accuracy': 100, 'pp': 15},
                {'name': 'Fire Blast', 'power': 110, 'accuracy': 85, 'pp': 5},
            ],
            'water': [
                {'name': 'Hydro Pump', 'power': 110, 'accuracy': 80, 'pp': 5},
                {'name': 'Surf', 'power': 90, 'accuracy': 100, 'pp': 15},
            ],
            'grass': [
                {'name': 'Solar Beam', 'power': 120, 'accuracy': 100, 'pp': 10},
                {'name': 'Leaf Storm', 'power': 130, 'accuracy': 90, 'pp': 5},
            ],
            'electric': [
                {'name': 'Thunderbolt', 'power': 90, 'accuracy': 100, 'pp': 15},
                {'name': 'Thunder', 'power': 110, 'accuracy': 70, 'pp': 10},
            ],
            'normal': [
                {'name': 'Hyper Beam', 'power': 150, 'accuracy': 90, 'pp': 5},
                {'name': 'Body Slam', 'power': 85, 'accuracy': 100, 'pp': 15},
            ]
        }
        
        pokemon_type = pokemon.get('type', 'normal').lower()
        available_moves = move_pools.get(pokemon_type, move_pools['normal'])
        
        move_index = min((level // 5) - 2, len(available_moves) - 1)
        if move_index >= 0:
            return available_moves[move_index]
        
        return None
    
    @staticmethod
    def add_experience(pokemon: Dict, exp_gained: int) -> List[Dict]:
        """
        Ajoute de l'expérience à un Pokémon et gère les montées de niveau.
        
        Modifie le dictionnaire pokemon in-place :
        - Ajoute l'expérience
        - Monte de niveau si nécessaire
        - Met à jour les statistiques
        - Restaure les HP au maximum
        
        Args:
            pokemon: Le dictionnaire du Pokémon (modifié in-place)
            exp_gained: L'expérience à ajouter
            
        Returns:
            Liste des informations de level-up (un dict par niveau gagné)
        """
        level_ups = []
        
        current_exp = pokemon.get('exp', 0)
        pokemon['exp'] = current_exp + exp_gained
        
        current_level = pokemon.get('level', 1)
        
        while current_level < LevelUpSystem.MAX_LEVEL:
            exp_needed = LevelUpSystem.exp_required_for_level(current_level + 1)
            
            if pokemon['exp'] >= exp_needed:
                current_level += 1
                pokemon['level'] = current_level
                
                stat_gains = LevelUpSystem.calculate_stat_gains(pokemon)
                for stat, gain in stat_gains.items():
                    if stat in pokemon:
                        pokemon[stat] += gain
                
                pokemon['current_hp'] = pokemon['hp']
                
                level_up_info = {
                    'new_level': current_level,
                    'stat_gains': stat_gains,
                    'pokemon_name': pokemon.get('name', 'Unknown')
                }
                
                new_move = LevelUpSystem.check_new_move(pokemon, current_level)
                if new_move:
                    level_up_info['new_move'] = new_move
                
                level_ups.append(level_up_info)
            else:
                break
        
        return level_ups
