import random, math
from .fight_info import FightInfo
from ..data_access.pokemon_pokedex_service import save_pokemon_to_pokedex

class Fight:
    """
    Manages the battle logic between two Pokemon.
    Handles turn order, damage calculation, item usage, and fleeing.
    """
    def __init__(self, pokemon1, pokemon2):
        self.first_pokemon = pokemon1
        self.second_pokemon = pokemon2
        self.fightinfo = FightInfo() # Stores data about the last action for the UI
    
    def set_first_pokemon(self, new_pokemon):
        """Updates the player's active Pokemon (e.g., after a switch)."""
        self.first_pokemon = new_pokemon

    def attack(self, pokemon, enemy, attack_type):
        """
        Executes an attack and calculates damage based on stats, 
        type effectiveness, and critical hits.
        """
        # Get type effectiveness multiplier and descriptive string
        coefficient, efficency = pokemon.attack_efficiency(attack_type, enemy)
        
        # Determine if the attack misses (1 in 8 chance)
        miss = random.randint(1, 8)

        # Basic damage formula: (Atk * multiplier) - Def
        damage = ((pokemon.get_strength() * coefficient) - enemy.get_defense())
        
        # Critical hit logic: based on the Pokemon's speed stat
        critical_rate = pokemon.get_speed() / 2
        critical = random.randint(1, 255)

        if miss == 1:
            efficency = "Missed attack..."
            final_damage = 0
        else:
            if damage > 0:
                # Normal damage scenario
                if enemy.get_hp() - damage >= 0:
                    if critical < critical_rate:
                        efficency = "Critical hit !!"
                        final_damage = damage * 2
                    else:
                        final_damage = damage
                else:
                    # Enemy would faint
                    if enemy.get_hp() - damage < 0:
                        final_damage = enemy.get_hp()
                    else:
                        final_damage = 0
                    
                    # Grant XP to the victor
                    pokemon.update_xp(enemy)
            else:
                # Low damage/High defense scenario (minimum damage logic)
                if critical < critical_rate:
                    efficency = "Critical hit !!"
                    final_damage = 20 # Guaranteed minimum for criticals
                    if enemy.get_hp() - final_damage < 0:
                        final_damage = enemy.get_hp()
                else:
                    final_damage = 1 # Guaranteed minimum for normal hits
                    if enemy.get_hp() - final_damage < 0:
                        final_damage = 0
                        
            final_damage = math.ceil(final_damage)
            enemy.set_damage_hp(final_damage)
        
        # Log action details for the UI
        self.fightinfo.set_all_values(efficency, attack_type, final_damage)

    def is_player_first(self):
        """Determines turn priority based on the Speed stat."""
        return self.first_pokemon.get_speed() > self.second_pokemon.get_speed()
        
    def player_attack(self, attack_type):
        """Triggers the player's Pokemon's attack."""
        self.attack(self.first_pokemon, self.second_pokemon, attack_type)

    def bot_attack(self):
        """Triggers the AI opponent's attack, choosing a type based on its own types."""
        if len(self.second_pokemon.type) == 2:
            attack_type = random.choice(self.second_pokemon.type)
        else:
            attack_type = self.second_pokemon.type[0]

        self.attack(self.second_pokemon, self.first_pokemon, attack_type)

    def run_away(self):
        """
        Attempts to flee the battle. 
        Impossible against trainers ('domesticated' state).
        """
        miss = random.randint(1, 7)
        if self.second_pokemon.get_state() == "domesticated":
            self.fightinfo.set_fail_flee_message()
            return False
            
        if miss == 1:
            # Flee failed: AI gets a free turn
            self.fightinfo.set_fail_flee_message()
            self.bot_attack()
            return False
        else:
            self.fightinfo.set_success_flee_message()
            return True

    def use_potion(self, pokemon, bag):
        """Uses a potion from the inventory to heal 20 HP."""
        if bag.get_potion() > 0:
            pokemon.heal(20)
            bag.set_potion(bag.get_potion() - 1)
            return None
        else:
            return "Back"

    def use_pokeball(self, player, bag, pokemon, pokemon_enemy):
        """
        Attempts to capture a wild Pokemon. 
        Success probability increases as the enemy's HP decreases.
        """
        if bag.get_pokeball() > 0:
            # Capture check: higher chance if enemy HP is low
            capture = random.randint(1, pokemon_enemy.get_hp_max())
            bag.set_pokeball(bag.get_pokeball() - 1)

            if capture >= pokemon_enemy.get_hp():
                return "Success"
            else:
                # Capture failed: AI gets a free turn
                self.bot_attack()
                return "Fail"
        else:
            return "Back"

    def use(self, player, bag, bag_option, pokemon, pokemon_enemy):
        """Generic bag usage handler for different item types."""
        if bag_option == "Potions":
            pokemon.heal(20)
        else:
            if bag.get_pokeball() > 0:
                # Logic for Pokeball usage via generic menu
                capture = random.randint(1, pokemon_enemy.get_hp())
                bag.set_pokeball(bag.get_pokeball() - 1)

                if capture <= 10:
                    save_pokemon_to_pokedex(player, pokemon)
                else:
                    self.bot_attack()