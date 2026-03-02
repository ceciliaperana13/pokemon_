import json
from __settings__ import PLAYER_POKEDEX
from .util import instanciate_pokemon

def save_pokemon_to_pokedex(player, pokemon):   
    """
    Saves a Pokemon to the player's Pokedex file.
    Changes the Pokemon's state to 'domesticated' (owned) and updates the JSON record.
    """
    with open(PLAYER_POKEDEX, "r") as file:
        player_pokedex = json.load(file)

    # Update state to prevent it from being treated as a wild Pokemon
    pokemon.set_state('domesticated')
    
    # Use pet_name as the unique key within the player's pokemon collection
    player_pokedex[player]["pokemons"].update({pokemon.pet_name : pokemon.pokemon_dict()})

    with open(PLAYER_POKEDEX, "w", encoding="UTF-8") as file:
        json.dump(player_pokedex, file, indent=4)

def get_pokemon_from_pokedex(player_name, pokemon_pet_name):
    """
    Retrieves a specific Pokemon by its pet name for a given player.
    Returns a 'hydrated' Pokemon object instance.
    """
    with open(PLAYER_POKEDEX, "r") as file:
        pokemons = json.load(file)[player_name]["pokemons"]

    for pokemon in pokemons:
        if pokemon == pokemon_pet_name:
            # Convert dictionary data back into a Pokemon object
            my_pokemon = instanciate_pokemon(pokemons[pokemon])
            return my_pokemon
        
def get_all_pokemons_from_pokedex(player_name):
    """
    Retrieves the entire collection of Pokemon owned by a player.
    Returns a list of Pokemon object instances.
    """
    with open(PLAYER_POKEDEX, "r") as file:
        pokemons = json.load(file)[player_name]["pokemons"]

    pokemon_list = []
    for pokemon in pokemons:
        my_pokemon = instanciate_pokemon(pokemons[pokemon])
        pokemon_list.append(my_pokemon)

    return pokemon_list

def get_first_pokemon(player_name):
    """
    Retrieves the first Pokemon in the player's collection.
    Usually used to determine the default lead Pokemon for battles.
    """
    with open(PLAYER_POKEDEX, "r") as file:
        pokemons = json.load(file)[player_name]["pokemons"]
        pokemon_keys = list(pokemons.keys())

    # Reconstruct the first Pokemon found in the dictionary keys
    my_pokemon = instanciate_pokemon(pokemons[pokemon_keys[0]])
    return my_pokemon

def get_player_pokemons(player):
    """Returns a list of all pet names (keys) owned by the player."""
    with open(PLAYER_POKEDEX, "r", encoding="UTF-8") as file:
        pokemons_dictionary = json.load(file)
        player_pokemons = pokemons_dictionary[player]["pokemons"].keys()
    return player_pokemons