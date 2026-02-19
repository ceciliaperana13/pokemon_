import json, os, random, time
from __settings__ import WORLD_POKEMON_PATH, NAME_LIST_PATH
from ..generate_pokemon.create_pokemon import create_low_level_world_pokemons
from .util import instanciate_pokemon

def generate_pokemons_dict():
    """
    Populates a list of Pokemon dictionaries by generating new low-level Pokemon.
    Assigns unique 'Jean-X' pet names based on a name list and a timestamp for uniqueness.
    """
    with open(NAME_LIST_PATH, 'r', encoding="UTF-8") as file:
        name_list = json.load(file)

    # Generate a fresh set of starting Pokemon
    all_pokemons = create_low_level_world_pokemons()
    pokemons_dict_list = []
    
    for index, each_pokemon in enumerate(all_pokemons):
        # Reset name index if we have more Pokemon than names in the list
        if index >= len(name_list):
            index = index % len(name_list)

        # Give the Pokemon a unique pet name (e.g., Jean-Luc 1708392.42)
        each_pokemon.set_pet_name("Jean-" + name_list[index] + " " + str(time.time()))
        
        # Convert the object to a dictionary for JSON storage
        a_pokemon = each_pokemon.pokemon_dict()
        pokemons_dict_list.append(a_pokemon)
    
    return pokemons_dict_list

def save_world_pokemons(pokemons_dict_list):
    """Overwrites the world Pokemon storage file with a new list of Pokemon data."""
    if not os.path.exists(WORLD_POKEMON_PATH):
        with open(WORLD_POKEMON_PATH, "w", encoding="UTF-8") as file:
            json.dump({}, file)
            
    with open(WORLD_POKEMON_PATH, "w", encoding="UTF-8") as file:
        json.dump(pokemons_dict_list, file, indent=4)

def save_wild_pokemon(my_pokemon):
    """Appends a single Pokemon back into the world file and ensures its state is 'wild'."""
    with open(WORLD_POKEMON_PATH, "r") as file:
        pokemons_dict_list = json.load(file)
    
    my_pokemon.set_state('wild')
    pokemons_dict_list.append(my_pokemon.pokemon_dict())

    with open(WORLD_POKEMON_PATH, "w", encoding="UTF-8") as file:
        json.dump(pokemons_dict_list, file, indent=4)

def get_random_wild_pokemon():
    """
    Retrieves a random Pokemon from the wild pool for an encounter.
    If the pool is empty or nearly depleted, it triggers a generation of new Pokemon.
    """
    # Initialize file if it doesn't exist
    if not os.path.exists(WORLD_POKEMON_PATH):
        with open(WORLD_POKEMON_PATH, "w", encoding="UTF-8") as file:
            json.dump([], file)

    with open(WORLD_POKEMON_PATH, "r") as file:
        pokemons = json.load(file)

    # World Replenishment Logic: If 4 or fewer remain, generate a new batch
    if not pokemons or len(pokemons) <= 4:
        other_pokemons = generate_pokemons_dict()
        pokemons = pokemons + other_pokemons
        
    # Select one Pokemon for the encounter and remove it from the 'wild' file
    a_pokemon_data = random.choice(pokemons)
    pokemons.pop(pokemons.index(a_pokemon_data))

    # Save the updated list (minus the selected Pokemon)
    save_world_pokemons(pokemons)
    
    # Transform dictionary data back into a Pokemon object instance
    my_pokemon = instanciate_pokemon(a_pokemon_data)

    return my_pokemon