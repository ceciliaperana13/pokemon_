import json, os, random
from __settings__ import PLAYER_POKEDEX
from .wild_pokemons import get_random_wild_pokemon
from .pokemon_pokedex_service import save_pokemon_to_pokedex
from .bag_pokedex_service import save_bag_to_pokedex
from ..models.bag import Bag
from ..generate_pokemon.create_pokemon import level_from_stage
from ..models.pokemon import Pokemon

# --- Back-to-Front (Data Retrieval) ---

def get_player_names():
    """Retrieves all registered player names from the Pokedex JSON file."""
    with open(PLAYER_POKEDEX, "r", encoding="UTF-8") as file:
        player_keys_dictionary = json.load(file)
    return player_keys_dictionary.keys()

def does_player_exist(player):
    """
    Checks if a player name is already taken.
    Initializes an empty Pokedex file if it doesn't exist.
    """
    if not os.path.exists(PLAYER_POKEDEX):
        with open(PLAYER_POKEDEX, "w", encoding="UTF-8") as file:
            json.dump({}, file)

    with open(PLAYER_POKEDEX, "r", encoding="UTF-8") as file:
        player_keys_dictionary = list(json.load(file).keys())

    return player in player_keys_dictionary


# --- Front-to-Back (Data Storage) ---

def create_player(player, pokemon):
    """
    Registers a new player with a default inventory and their first Pokemon.
    Saves the profile to the Pokedex database.
    """
    with open(PLAYER_POKEDEX, "r", encoding="UTF-8") as file:
        players_dictionary = json.load(file)

    # Only create if the name is unique
    if player not in players_dictionary.keys():
        player_bag = Bag()
        players_dictionary[player] = {
            "bag" : {},
            "pokemons" : {}
            }
    else:
        return # Abort if player exists
            
    with open(PLAYER_POKEDEX, "w", encoding="UTF-8") as file:
        json.dump(players_dictionary, file, indent=4)
    
    # Save the associated starter and the new bag
    save_pokemon_to_pokedex(player, pokemon)
    save_bag_to_pokedex(player, player_bag)


def create_specific_starter(name, first_stage_name, type_list, stage):
    """
    Factory function to create a standardized Level 5 starter Pokemon.
    Calculates randomized base stats.
    """
    level = 5  # Fixed starting level
    
    # Calculate base stats with a random variance
    hp = random.randrange(10, 31) + level * 3
    strength = random.randrange(2, 31) + level * 3
    speed = random.randrange(2, 31) + level * 3
    defense_point = random.randrange(2, 21) + level * 3
    
    # Instantiate the Pokemon object
    my_pokemon = Pokemon(name, first_stage_name, hp, hp, strength, defense_point, type_list, level, speed, stage)
    
    # Set experience points appropriate for Level 5
    xp = random.randrange(my_pokemon.get_level()**3, (my_pokemon.get_level()+1)**3)
    my_pokemon.set_xp(xp)
    
    return my_pokemon


# Global counter to cycle through choices in the UI
_starter_index = 0

def get_starter_pokemon():
    """
    Returns one of the 3 classic starters (Bulbasaur, Charmander, Squirtle).
    Cycles to the next one on each call, useful for a 'Next' button in the UI.
    """
    global _starter_index
    
    # The classic Generation 1 trio
    starters = [
        {"name": "Bulbasaur", "first_stage_name": "Bulbasaur", "type_list": ["grass", "poison"], "stage": 1},
        {"name": "Charmander", "first_stage_name": "Charmander", "type_list": ["fire"], "stage": 1},
        {"name": "Squirtle", "first_stage_name": "Squirtle", "type_list": ["water"], "stage": 1}
    ]
    
    # Select data based on index
    starter_data = starters[_starter_index % 3]
    
    # Increment for the next selection
    _starter_index += 1
    
    # Generate the actual Pokemon object
    my_pokemon = create_specific_starter(
        starter_data["name"],
        starter_data["first_stage_name"],
        starter_data["type_list"],
        starter_data["stage"]
    )
    
    print(f"✅ Starter generated: {my_pokemon.name} (Type: {', '.join(my_pokemon.type)})")
    
    return my_pokemon