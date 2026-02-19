import random, json
from __settings__ import TYPES_PATH, EVOLUTION_STAGE_PATH
from back_end.models.pokemon import Pokemon

def get_first_type_dict(first_type):
    """Retrieves the sub-dictionary of potential second types and Pokemon for a given primary type."""
    with open(TYPES_PATH, 'r') as file:
        second_type_dict = json.load(file)[first_type]
        return second_type_dict
     
def __get_pokemon_from_type(type_list):
    """
    Selects a random Pokemon species and its corresponding evolution stage 
    based on the provided type combination (single or dual type).
    """
    type_name_dictionary = get_first_type_dict(type_list[0])

    if len(type_list) == 2:
        # Access names for dual-type Pokemon
        get_name_list = type_name_dictionary[type_list[1]]["names"]     
    else:
        # Access names for single-type Pokemon
        get_name_list = type_name_dictionary["alone"]["names"]
    
    # Randomly pick a species (first_stage_name) and then a specific form (name)
    choice_list = list(get_name_list.keys())
    first_stage_name = random.choice(choice_list)
    name = random.choice(list(get_name_list[first_stage_name].keys()))
    stage = get_name_list[first_stage_name][name]
    
    return name, first_stage_name, stage

def level_from_stage(stage):
    """Assigns a logical level range based on the Pokemon's evolution stage."""
    if stage == 4:
        level = random.randrange(40, 50)
    elif stage == 3:
        level = random.randrange(25, 36)
    elif stage == 2:
        level = random.randrange(12, 20)
    else:
        level = random.randrange(1, 10) 
    return level

def create_pokemon(first_type):
    """
    Procedurally generates a complete Pokemon object starting from a primary type.
    Handles secondary type probability, stat randomization, and level scaling.
    """
    final_type_list = [first_type]
    get_second_type_dict = get_first_type_dict(first_type)
    
    # Weighted random selection for the secondary type
    second_type_list = []
    for type_key in get_second_type_dict:
        probability_weight = get_second_type_dict[type_key]["probability"]
        for _ in range(probability_weight):
            second_type_list.append(type_key)
    
    second_type_random = random.choice(second_type_list)
    if second_type_random != "alone":
        final_type_list.append(second_type_random)

    # Determine species, stage, and level
    name, first_stage_name, stage = __get_pokemon_from_type(final_type_list)
    level = level_from_stage(stage)

    # Generate randomized base stats scaled by level
    hp = random.randrange(10, 31) + level * 3
    strength = random.randrange(2, 31) + level * 3
    speed = random.randrange(2, 31) + level * 3
    defense_point = random.randrange(2, 15) + level * 3

    # Instantiate the Pokemon
    my_pokemon = Pokemon(name, first_stage_name, hp, hp, strength, defense_point, final_type_list, level, speed, stage)
    
    # Set XP to a random value within the current level's threshold
    xp = random.randrange(my_pokemon.get_level()**3, (my_pokemon.get_level()+1)**3)
    my_pokemon.set_xp(xp)

    return my_pokemon

def create_world_pokemons():
    """Generates a diverse list containing one random Pokemon of every primary type."""
    with open(TYPES_PATH, 'r') as file:
        types = json.load(file)
        type_list = list(types.keys())

    all_pokemons = []
    for t in type_list:
        all_pokemons.append(create_pokemon(t))
    
    return all_pokemons

def create_low_level_world_pokemons():
    """
    Generates a list of 'starter' or 'wild' Pokemon, 
    filtering for only those at the first evolution stage.
    """
    with open(EVOLUTION_STAGE_PATH, 'r') as file:
        pokemons_original_name = json.load(file)
        pokemons_original_name_list = list(pokemons_original_name.keys()) 

    all_pokemons = []
    for name in pokemons_original_name_list:
        # Check if the species is in its first evolution stage
        if pokemons_original_name[name][name] == 1:
            type_list = []
            first_type, second_type, stage = get_type_low_level_pokemon(name)
            type_list.append(first_type)
            if second_type != "alone":
                type_list.append(second_type)

            level = level_from_stage(stage)

            # Randomize stats for the low-level encounter
            hp = random.randrange(10, 31) + level * 3
            strength = random.randrange(2, 31) + level * 3
            speed = random.randrange(2, 31) + level * 3
            defense_point = random.randrange(2, 21) + level * 3

            my_pokemon = Pokemon(name, name, hp, hp, strength, defense_point, type_list, level, speed, stage)
            
            # Set appropriate XP
            xp = random.randrange(my_pokemon.get_level()**3, (my_pokemon.get_level()+1)**3)
            my_pokemon.set_xp(xp)
            all_pokemons.append(my_pokemon)
            
    random.shuffle(all_pokemons)
    return all_pokemons

def get_type_low_level_pokemon(original_name):
    """
    Reverse-searches the types database to find the elemental types 
    associated with a specific Pokemon name.
    """
    with open(TYPES_PATH, 'r') as file:
        types = json.load(file)
        type_list = list(types.keys())

    for first_type in type_list:
        second_type_list = list(types[first_type].keys())

        for second_type in second_type_list:
            names_list = list(types[first_type][second_type]["names"].keys())

            for name in names_list:
                final_name_dict = types[first_type][second_type]["names"][name]
                final_name_list = list(final_name_dict.keys())
                
                # Identify the name linked to stage 1 evolution
                if 1 in list(final_name_dict.values()):
                    final_name = final_name_list[list(final_name_dict.values()).index(1)]

                    if final_name == original_name:
                        return first_type, second_type, 1