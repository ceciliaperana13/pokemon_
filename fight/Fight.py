from typing import Dict, List
from type_effectiveness import TypeEffectiveness
from level_up_system import LevelUpSystem


class Fight:
    """Classe principale gérant les combats et l'expérience."""
    
    def __init__(self, fichier_efficacite: str = "efficacite_types.txt"):
        """
        Initialise le système de combat.
        
        Args:
            fichier_efficacite: Chemin vers le fichier de configuration des types
        """
        self.type_system = TypeEffectiveness(fichier_efficacite)
        self.combat_log = []
    
    def calculate_damage(self, attaquant: Dict, defenseur: Dict) -> Dict:
        """
        Calcule les dégâts d'une attaque.
        
        Args:
            attaquant: Pokémon qui attaque (doit contenir 'type' et 'attack')
            defenseur: Pokémon qui défend (doit contenir 'type' et 'defense')
        
        Returns:
            {
                'damage': float,
                'effectiveness': float,
                'is_critical': bool
            }
        """
        type_attaquant = attaquant.get('type', 'normal')
        type_defenseur = defenseur.get('type', 'normal')
        
        multiplicateur = self.type_system.get_multiplicateur(type_attaquant, type_defenseur)
        
        degats_bruts = attaquant.get('attack', 50) * multiplicateur
        reduction = defenseur.get('defense', 50) * 0.5
        degats_finaux = max(1, degats_bruts - reduction)
        
        return {
            'damage': degats_finaux,
            'effectiveness': multiplicateur,
            'is_critical': False
        }
    
    def apply_damage(self, pokemon: Dict, damage: float) -> Dict:
        """
        Applique les dégâts à un Pokémon.
        
        Args:
            pokemon: Pokémon qui subit les dégâts (modifié in-place)
            damage: Montant des dégâts
        
        Returns:
            {
                'hp_before': float,
                'hp_after': float,
                'damage_dealt': float,
                'is_ko': bool
            }
        """
        hp_before = pokemon.get('current_hp', pokemon.get('hp', 100))
        pokemon['current_hp'] = max(0, hp_before - damage)
        hp_after = pokemon['current_hp']
        
        return {
            'hp_before': hp_before,
            'hp_after': hp_after,
            'damage_dealt': hp_before - hp_after,
            'is_ko': hp_after <= 0
        }
    
    def execute_turn(self, attaquant: Dict, defenseur: Dict) -> Dict:
        """
        Exécute un tour de combat.
        
        Args:
            attaquant: Pokémon qui attaque
            defenseur: Pokémon qui défend
        
        Returns:
            {
                'attacker_name': str,
                'defender_name': str,
                'damage_info': dict,
                'result': dict,
                'defender_ko': bool
            }
        """
        damage_info = self.calculate_damage(attaquant, defenseur)
        result = self.apply_damage(defenseur, damage_info['damage'])
        
        return {
            'attacker_name': attaquant.get('name', 'Unknown'),
            'defender_name': defenseur.get('name', 'Unknown'),
            'damage_info': damage_info,
            'result': result,
            'defender_ko': result['is_ko']
        }
    
    def battle(self, pokemon1: Dict, pokemon2: Dict, max_turns: int = 100) -> Dict:
        """
        Lance un combat complet entre deux Pokémon.
        
        Args:
            pokemon1: Premier Pokémon
            pokemon2: Deuxième Pokémon
            max_turns: Nombre maximum de tours (sécurité)
        
        Returns:
            {
                'winner': dict,
                'loser': dict,
                'turns': list,
                'total_turns': int
            }
        """
        self.combat_log = []
        turn_count = 0
        
        while turn_count < max_turns:
            turn_count += 1
            
            # Pokemon 1 attaque
            turn_result1 = self.execute_turn(pokemon1, pokemon2)
            self.combat_log.append(turn_result1)
            
            if turn_result1['defender_ko']:
                return {
                    'winner': pokemon1,
                    'loser': pokemon2,
                    'turns': self.combat_log,
                    'total_turns': turn_count
                }
            
            # Pokemon 2 attaque
            turn_result2 = self.execute_turn(pokemon2, pokemon1)
            self.combat_log.append(turn_result2)
            
            if turn_result2['defender_ko']:
                return {
                    'winner': pokemon2,
                    'loser': pokemon1,
                    'turns': self.combat_log,
                    'total_turns': turn_count
                }
        
        # Si max_turns atteint, celui avec le plus de HP gagne
        if pokemon1.get('current_hp', 0) > pokemon2.get('current_hp', 0):
            winner, loser = pokemon1, pokemon2
        else:
            winner, loser = pokemon2, pokemon1
        
        return {
            'winner': winner,
            'loser': loser,
            'turns': self.combat_log,
            'total_turns': turn_count
        }
    
    def process_victory(self, winner: Dict, loser: Dict, party: List[Dict] = None, 
                       is_wild: bool = True) -> Dict:
        """
        Traite la victoire : calcul et distribution d'expérience.
        
        Args:
            winner: Pokémon vainqueur
            loser: Pokémon vaincu
            party: Liste des Pokémon de l'équipe (None = solo)
            is_wild: Combat contre Pokémon sauvage ou dresseur
        
        Returns:
            {
                'exp_gains': {
                    pokemon_name: {
                        'exp_gained': int,
                        'level_ups': list
                    }
                },
                'total_exp': int
            }
        """
        if party is None:
            party = [winner]
        
        exp_gains = {}
        total_exp = 0
        
        for pokemon in party:
            if pokemon.get('current_hp', 0) <= 0:
                continue
            
            exp_gained = LevelUpSystem.calculate_exp_gain(loser, pokemon, is_wild)
            level_ups = LevelUpSystem.add_experience(pokemon, exp_gained)
            
            pokemon_name = pokemon.get('name', 'Unknown')
            exp_gains[pokemon_name] = {
                'exp_gained': exp_gained,
                'level_ups': level_ups
            }
            total_exp += exp_gained
        
        return {
            'exp_gains': exp_gains,
            'total_exp': total_exp
        }
    
    def full_battle_with_exp(self, pokemon1: Dict, pokemon2: Dict, 
                            party: List[Dict] = None, is_wild: bool = True) -> Dict:
        """
        Combat complet avec traitement de l'expérience.
        
        Args:
            pokemon1: Premier Pokémon (celui qui combat)
            pokemon2: Deuxième Pokémon
            party: Liste de l'équipe complète (None = solo)
            is_wild: Combat sauvage (True) ou dresseur (False)
        
        Returns:
            {
                'battle_result': dict,
                'exp_result': dict
            }
        """
        battle_result = self.battle(pokemon1, pokemon2)
        exp_result = self.process_victory(
            battle_result['winner'], 
            battle_result['loser'], 
            party, 
            is_wild
        )
        
        return {
            'battle_result': battle_result,
            'exp_result': exp_result
        }