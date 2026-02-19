import math, random

class EffortValue():
    """
    Manages a Pokemon's Effort Values (EVs). 
    EVs are hidden points gained by defeating enemies that lead to 
    permanent stat increases (HP, Strength, Defense, etc.).
    """
    def __init__(self):
        # Internal accumulators for effort points
        self.__ev_hp = 0
        self.__ev_strength = 0
        self.__ev_defense = 0
        self.__ev_speed = 0
        self.__ev_xp = 0

    def get_ev_dict(self):
        """Returns a dictionary representation of current EV points."""
        ev = {
            "hp" : self.get_ev_hp(),
            "strength" : self.get_ev_strength(),
            "defense" : self.get_ev_defense(),
            "speed" : self.get_ev_speed(),
            "xp" : self.get_ev_xp()
        }
        return ev
    
    def declare_range_ev(self, enemy, divisor):
        """
        Calculates the potential range of EV gain based on the enemy's stats.
        Higher divisors (used for lower level enemies) result in smaller gains.
        """
        rand_range_hp = math.ceil(enemy.get_hp_max() / divisor)
        rand_range_strength = math.ceil((enemy.get_strength() / divisor))
        rand_range_defense = math.ceil(enemy.get_defense() / divisor)
        rand_range_speed = math.ceil((enemy.get_speed() / divisor))
        rand_range_xp = math.ceil((enemy.get_xp() / divisor))

        return rand_range_hp, rand_range_strength, rand_range_defense, rand_range_speed, rand_range_xp
    
    def update_ev(self, enemy, pokemon):
        """
        Awards EVs after defeating an enemy. 
        Gains are scaled based on the level difference between the two Pokemon.
        """
        # Determine the scaling factor based on difficulty
        if enemy.get_level() > pokemon.get_level():
            # Higher reward for tougher enemies
            rand_range_hp, rand_range_strength, rand_range_defense,\
                rand_range_speed, rand_range_xp = self.declare_range_ev(enemy, 6)

        elif enemy.get_level() == pokemon.get_level():
            rand_range_hp, rand_range_strength, rand_range_defense,\
                rand_range_speed, rand_range_xp = self.declare_range_ev(enemy, 9)

        elif enemy.get_level() < pokemon.get_level():
            # Lower reward for weaker enemies
            rand_range_hp, rand_range_strength, rand_range_defense,\
                rand_range_speed, rand_range_xp = self.declare_range_ev(enemy, 12)

        # Increment internal EV counters with a random value within the calculated range
        self.set_ev_hp(self.get_ev_hp() + math.floor(random.randrange(rand_range_hp * 2, rand_range_hp * 4)))
        self.set_ev_strength(self.get_ev_strength() + math.floor(random.randrange(rand_range_strength * 2, rand_range_strength * 4)))
        self.set_ev_defense(self.get_ev_defense() + math.floor(random.randrange(rand_range_defense * 2, rand_range_defense * 4)))
        self.set_ev_speed(self.get_ev_speed() + math.floor(random.randrange(rand_range_speed * 2, rand_range_speed * 4)))
        self.set_ev_xp(self.get_ev_xp() + math.floor(random.randrange(rand_range_xp * 2, rand_range_xp * 4)))
        
        # Check if accumulated EVs should be converted to actual stats
        self.__update_stats(pokemon)

    def __update_stats(self, pokemon):
        """
        Private method to convert accumulated EVs into permanent stat boosts.
        Every 4 EV points in a category are converted into +1 to the base stat.
        """
        # HP Update
        if self.get_ev_hp() > 4:
            hp = pokemon.get_hp_max() + self.get_ev_hp() // 4
            self.set_ev_hp(self.get_ev_hp() % 4) # Keep the remainder
            pokemon.set_hp_max(hp)     

        # Strength Update
        if self.get_ev_strength() > 4:
            strength = pokemon.get_strength() + self.get_ev_strength() // 4
            self.set_ev_strength(self.get_ev_strength() % 4)
            pokemon.set_strength(strength)
            
        # Defense Update
        if self.get_ev_defense() > 4:
            defense = pokemon.get_defense() + self.get_ev_defense() // 4
            self.set_ev_defense(self.get_ev_defense() % 4)
            pokemon.set_defense(defense)
            
        # Speed Update
        if self.get_ev_speed() > 4:
            speed = pokemon.get_speed() + self.get_ev_speed() // 4
            self.set_ev_speed(self.get_ev_speed() % 4)
            pokemon.set_speed(speed)
            
        # XP Update (Special EV that contributes to base XP)
        if self.get_ev_xp() > 4:
            xp = pokemon.get_xp() + self.get_ev_xp() // 4
            self.set_ev_xp(self.get_ev_xp() % 4)
            pokemon.set_xp(xp)
          
    # --- Getters and Setters ---
    
    def get_ev_hp(self):
            return self.__ev_hp
    
    def get_ev_strength(self):
            return self.__ev_strength
    
    def get_ev_defense(self):
            return self.__ev_defense
    
    def get_ev_speed(self):
            return self.__ev_speed
    
    def get_ev_xp(self):
            return self.__ev_xp
    
    def set_ev_hp(self, new_value):
        self.__ev_hp = new_value
    
    def set_ev_strength(self, new_value):
        self.__ev_strength = new_value
    
    def set_ev_defense(self, new_value):
        self.__ev_defense = new_value

    def set_ev_speed(self, new_value):
        self.__ev_speed = new_value
    
    def set_ev_xp(self, new_value):
        self.__ev_xp = new_value