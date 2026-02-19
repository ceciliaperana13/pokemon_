import random, json, math
from .effortValue import EffortValue
from __settings__ import COEFFICIENT_PATH
from .evolution import Evolution

class Pokemon(Evolution):
    """
    Represents a Pokemon instance, inheriting evolution logic and managing 
    stats, types, and experience.
    """
    
    # Load type effectiveness coefficients from a JSON file at the class level
    coefficient = json.load(open(COEFFICIENT_PATH))
    
    def __init__(self, name, original_name, hp, hp_max, strength, defense, type, level, speed, stage):
        """Initializes Pokemon attributes including stats and base evolution data."""
        super().__init__(name, stage, original_name, type, level)
        self.__hp = hp
        self.__hp_max = hp_max
        self.__strength = strength
        self.__defense = defense
        self.__xp = 1
        self.__state = 'wild' # Can be 'wild' or 'domesticated'
        self.__ev = EffortValue() # Manages Effort Values for stat growth
        self.__speed = speed
        self.pet_name = 'Jean-Luc' # Default nickname
    
    def pokemon_dict(self):
        """Returns a dictionary representation of the Pokemon for saving or serialization."""
        return {
            "name" : self.name,
            "original_name" : self.get_original_name(),
            "pet_name" : self.pet_name,
            "hp_max" : self.get_hp_max(),
            "hp" : self.get_hp(),
            "xp" : self.get_xp(),
            "strength" : self.get_strength(),
            "defense" : self.get_defense(),
            "type" : self.type,
            "level" : self.get_level(),
            "speed" : self.get_speed(),
            "stage" : self.get_stage(),
            "ev" : self.get_effort_value().get_ev_dict(),
            "state" : self.get_state()
        }
    
    # --- Getters and Setters ---

    def set_pet_name(self, new_name):
        self.pet_name = new_name

    def get_effort_value(self):
        return self.__ev

    def get_hp(self):
        return self.__hp
    
    def set_hp(self, new_hp):
        self.__hp = new_hp
    
    def set_damage_hp(self, damage):
        """Subtracts damage from current HP."""
        self.__hp = self.get_hp() - damage

    def get_hp_max(self):
        return self.__hp_max
    
    def heal(self, heal_amount):
        """Restores HP without exceeding the maximum HP."""
        if self.get_hp() + heal_amount <= self.get_hp_max():
            self.set_hp(self.get_hp() + heal_amount)
        else:
            self.set_hp(self.get_hp_max())
    
    def set_hp_max(self, new_value):
        self.__hp_max = new_value
    
    def get_strength(self):
        return self.__strength
    
    def set_strength(self, new_value):
        self.__strength = new_value

    def get_defense(self):
        return self.__defense

    def set_defense(self, new_value):
        self.__defense = new_value
    
    def get_xp(self):
        return self.__xp
    
    def set_xp(self, new_value):
        self.__xp = new_value
    
    def get_speed(self):
        return self.__speed
    
    def set_speed(self, new_value):
        self.__speed = new_value
    
    def get_state(self):
        return self.__state
    
    def set_state(self, new_state):
        if new_state in ['wild', 'domesticated']:
            self.__state = new_state

    # --- Battle Logic ---
        
    def get_attack_coefficient(self, attack_type, enemy):
        """Calculates the damage multiplier based on attack type and enemy types."""
        if len(enemy.type) == 2:
            # For dual-type enemies, multiply both coefficients
            list_coefficient = []
            for index in range(len(enemy.type)):
                a_coefficient = Pokemon.coefficient[attack_type][enemy.type[index]]
                list_coefficient.append(a_coefficient)
            coefficient = list_coefficient[0] * list_coefficient[1]
        else:
            # Single type calculation
            coefficient = Pokemon.coefficient[attack_type][enemy.type[0]]

        return coefficient
    
    def attack_efficiency(self, chose_attack_type, enemy):
        """Returns the damage multiplier and a descriptive string of effectiveness."""
        coefficient = self.get_attack_coefficient(chose_attack_type, enemy)

        # Match coefficient to standard Pokemon effectiveness terminology
        match coefficient:
            case 4:
                efficiency = "Super effective attack"
            case 2:
                efficiency = "Very effective attack"
            case 1:
                efficiency = "Effective attack"
            case 0.25 | 0.5:
                efficiency = "Not so effective attack"
            case 0:
                efficiency = "Impossible to attack"

        return coefficient, efficiency

    # --- Growth and Evolution ---

    def check_evolution(self):
        """Triggers the evolution logic from the parent class."""
        is_evolving = self.evolve()
    
    def get_xp_gained(self, enemy):
        """Calculates XP rewards based on level differences and enemy state (wild vs trainer)."""
        enemy_level = enemy.get_level()

        # Calculation logic varies depending on relative levels
        if enemy_level > self._level:
            if enemy.get_state() == 'wild':
                xp_gained = int(math.floor(100 * enemy.get_level() / 6))
            else:
                xp_gained = int(math.floor(100 * enemy.get_level() / 5))
        elif enemy_level < self._level:
            xp_gained = int(math.floor(100 * enemy.get_level() / 9))
        else:
            xp_gained = int(math.floor(100 * enemy.get_level() / 7))
        return xp_gained

    def update_xp(self, enemy):
        """Updates XP after battle and checks for level-ups and evolutions."""
        xp_gained = self.get_xp_gained(enemy)
        self.set_xp(self.get_xp() + xp_gained)
        self.__ev.update_ev(enemy, self) # Gain EVs based on enemy defeated
        self.level_up(self) # Trigger level-up logic if XP threshold met
        self.evolve() # Check for evolution eligibility

    def __str__(self):
        """Returns a formatted string containing the Pokemon's current status and stats."""
        # Adjust display based on whether the Pokemon has one or two types
        if len(self.type) > 1:
            string = f"Pokemon : {self.name}\
                \nLevel : {self.get_level()}\
                \nXP : {self.get_xp()}\
                \nDefense : {self.get_defense()}\
                \nSpeed : {self.get_speed()}\
                \nHP max : {self.get_hp_max()}\
                \nHP: {self.get_hp()}\
                \nFirst type: {self.type[0]}\
                \nSecond type : {self.type[1]}\
                \nStrength : {self.get_strength()}\n"
        else:
            string = f"Pokemon : {self.name}\
                \nLevel : {self.get_level()}\
                \nXP : {self.get_xp()}\
                \nDefense : {self.get_defense()}\
                \nSpeed : {self.get_speed()}\
                \nHP max : {self.get_hp_max()}\
                \nHP: {self.get_hp()}\
                \nType : {self.type[0]}\
                \nStrength : {self.get_strength()}\n"
        return string + "\n"