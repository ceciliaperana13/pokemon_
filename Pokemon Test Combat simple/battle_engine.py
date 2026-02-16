import random
from savemanager import SaveManager

class BattleEngine:
    def __init__(self):
        # Dictionnaire qui associe l'ID au type
        self.pokemon_types = {
            "1": "Plante", "2": "Plante", "3": "Plante",      # Famille Bulbizarre
            "4": "Feu", "5": "Feu", "6": "Feu",            # Famille Salameche
            "7": "L'eau", "8": "L'eau", "9": "L'eau",      # Famille Carapuce
            "10": "L'eau", "11": "Dragon", "13": "Feu",    # Artikodin, Electhor, Sulfura
            "14": "Dragon", "15": "Dragon", "16": "Dragon",   # Minidraco...
            "17": "Psy", "18": "Psy"                 # Mewtwo, Mew
        }

        self.type_chart = {
            "L'eau": {"L'eau": 1, "Feu": 2, "Plante": 0.5, "Dragon": 1},
            "Feu":   {"L'eau": 0.5, "Feu": 1, "Plante": 2, "Dragon": 1},
            "Plante": {"L'eau": 2, "Feu": 0.5, "Plante": 1, "Dragon": 1},
            "Dragon":{"L'eau": 0.75, "Feu": 0.75, "Plante": 0.75, "Dragon": 1}
        }

    def compute_damage(self, attacker_type, defender_type):
        """Méthode qui enlève des points de vie en fonction de la défense (multiplicateurs)."""
        base_atk = random.randint(15, 25)
        # On récupère le multiplicateur, par défaut 1 si type inconnu
        multiplier = self.type_chart.get(attacker_type, {}).get(defender_type, 1)
        
        final_damage = int(base_atk * multiplier)
        return final_damage, multiplier

    def get_result(self, p_hp, e_hp, p_name, e_name):
        """Méthode qui renvoie le nom du vainqueur et du perdant."""
        if e_hp <= 0:
            return p_name, e_name # Gagnant, Perdant
        elif p_hp <= 0:
            return e_name, p_name # Gagnant, Perdant
        return None, None

    # Dans battle_engine.py
    def register_encounter(self, pokemon_id):
        # On délègue tout au SaveManager qui sait gérer le fichier pokedex.json
        SaveManager.register_encounter(pokemon_id)
    
    def get_pokemon_type(self, pokemon_id):
        """Récupère le type en fonction de l'ID (extrait le numéro du nom de fichier)."""
        # On force en string pour éviter l'erreur si c'est un chiffre
        clean_id = str(pokemon_id).split(" - ")[0]
        return self.pokemon_types.get(clean_id, "Dragon")
    