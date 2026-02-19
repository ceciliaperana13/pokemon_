import random, json
from __settings__ import TYPES_PATH, EVOLUTION_STAGE_PATH, ABSOLUTE_IMAGE_PATH

class Evolution():
    """
    Parent class for Pokemon that manages leveling up, stat growth, 
    and the evolution transition logic.
    """
    def __init__(self, name, stage, original_name, type, level):
        self.name = name
        self.__stage = stage              # Current stage in the evolution line (1, 2, or 3)
        self.__original_name = original_name # The base form name (e.g., 'Eevee')
        self._level = level
        self.type = type                  # List of types (e.g., ['fire'])
        
        # Asset management
        self.__evolution_number = self.get_evolution_name_list()
        self.image = self.get_image()
        self.back_image = self.get_back_image()

    # --- Getters and Setters ---

    def set_stage(self, new_stage):
        self.__stage = new_stage
    
    def get_stage(self):
        return self.__stage

    def get_image(self):
        """Returns the absolute path for the front-facing sprite."""
        image = ABSOLUTE_IMAGE_PATH + self.name + ".png"
        return image
    
    def get_back_image(self):
        """Returns the absolute path for the back-facing battle sprite."""
        image = ABSOLUTE_IMAGE_PATH + "BackPoke/" + self.name + ".png"
        return image

    def get_evolution_stage_json(self):
        """Loads evolution data for this specific Pokemon species from JSON."""
        with open(EVOLUTION_STAGE_PATH, 'r') as evolution_stage:
            data = json.load(evolution_stage)[self.__original_name]
        return data
   
    def get_evolution_name_list(self):
        """Determines how many total evolution stages exist for this Pokemon."""
        evolution_stage = self.get_evolution_stage_json()
        name_list = list(evolution_stage.keys())

        # Special handling for Eevee due to its multiple branching paths
        if self.__original_name != 'Eevee':
            evolution_number = len(name_list)
        else:
            evolution_number = 2
            
        return evolution_number
    
    def update_name(self, new_name):
        self.name = new_name

    # --- Special Evolution Branching ---

    def update_evolution_meowth(self):
        """Handles specific type changes for Meowth's forms."""
        if self.type[0] != 'normal':
            self.type = ['dark']

    def update_evolution_eevee(self):
        """Randomly evolves Eevee into one of its elemental forms."""
        types = ['water', 'electric', 'fire']
        new_type = random.choice(types) 
        self.type.append(new_type)
        # Remove the 'normal' type as it evolves
        self.type.pop(self.type.index('normal'))
        
        match new_type:
            case 'water':
                new_name = 'Vaporeon'
            case 'electric':
                new_name = 'Jolteon'
            case 'fire':
                new_name = 'Flareon'
        self.update_name(new_name)

    def update_evolution_slowpoke(self):
        """Handles specific type changes for the Slowpoke line."""
        if self.type[0] == 'psychic':
            self.type = ['poison', 'psychic']

    def update_evolution_stage(self):
        """Updates the Pokemon's name and type attributes when it evolves."""
        evolution_stage = self.get_evolution_stage_json()

        if self.__original_name != 'Eevee':
            evolution_stage_value = list(evolution_stage.values())
            # Find the name corresponding to the new stage number
            new_name = list(evolution_stage.keys())[evolution_stage_value.index(self.__stage)]
            self.update_name(new_name)
            
        self.update_type()
        self.image = self.get_image() # Refresh sprite path

    def update_type(self):
        """Updates the type list based on the new evolution form."""
        if len(self.type) == 1 and self.__original_name not in ['Eevee', 'Meowth', 'Slowpoke']:
            with open(TYPES_PATH, 'r') as file:
                data = json.load(file)
                my_pokemon_data = data[self.type[0]]

            data_list = list(my_pokemon_data.keys())
            
            # Check if a sub-type should be added for the evolved form
            for sub_type in data_list:
                if sub_type != "alone":
                    sub_type_dict = my_pokemon_data[sub_type]
                    if self.__original_name in sub_type_dict["names"]: 
                        if self.name in sub_type_dict["names"][self.__original_name]:
                            self.type.append(sub_type)
        
        # Trigger special case updates
        if self.__original_name == "Eevee":
            self.update_evolution_eevee()
        elif self.__original_name == "Meowth":
            self.update_evolution_meowth()
        elif self.__original_name == "Slowpoke":
            self.update_evolution_slowpoke()

    # --- Leveling and Evolution Logic ---

    def level_up(self, pokemon):
        """Checks if the current XP exceeds the Level^3 threshold and increments levels."""
        level = self.get_level()
        xp_value = pokemon.get_xp()
        add_level = 0
        
        # Standard Cubic XP curve: Level 10 requires 1000 XP
        while xp_value >= level**3:
            add_level += 1
            xp_value -= level**3
            level += 1
            
        if add_level != 0:
            self.set_level_up(pokemon, add_level)

    def evolve(self):
        """
        Determines if a Pokemon is eligible to evolve based on its level.
        Includes a 'luck' factor for early evolution between specific levels.
        """
        level = self.get_level()
        if self.__stage < self.__evolution_number:
            # Logic for 3-stage evolution lines (e.g., Charmander -> Charmeleon -> Charizard)
            if self.__evolution_number == 3:
                match self.__stage:
                    case 1:
                        if level in range(10, 20):
                            if random.randrange(100) > 60: # 40% chance per level up
                                self.__stage += 1
                                self.update_evolution_stage()
                                return True
                        elif level >= 20: # Forced evolution
                            self.__stage += 1
                            self.update_evolution_stage()
                            return True
                    case 2:
                        if level in range(22, 32):
                            if random.randrange(100) > 60:
                                self.__stage += 1
                                self.update_evolution_stage()
                                return True
                        elif level >= 32:
                            self.__stage += 1
                            self.update_evolution_stage()
                            return True
            
            # Logic for 2-stage evolution lines
            if self.__evolution_number == 2: 
                match self.__stage:
                    case 1:
                        if level in range(17, 25):
                            if random.randrange(100) > 60:
                                self.__stage += 1
                                self.update_evolution_stage()
                                return True
                        elif level >= 25:
                            self.__stage += 1
                            self.update_evolution_stage()
                            return True
                
    def set_level_up(self, pokemon, add_level):
        """Increments stats randomly upon leveling up."""
        self._level += add_level
        # Stats grow by a random range multiplied by levels gained
        pokemon.set_strength(pokemon.get_strength() + random.randrange(add_level*5, add_level*15))
        pokemon.set_defense(pokemon.get_defense() + random.randrange(add_level*5, add_level*15))
        pokemon.set_speed(pokemon.get_speed() + random.randrange(add_level*5, add_level*15))
        pokemon.set_hp_max(pokemon.get_hp_max() + random.randrange(add_level*5, add_level*15))
        
    def get_level(self):
        return self._level
    
    def get_original_name(self):
        return self.__original_name