from back_end.models.pokemon import Pokemon
from ..models.bag import Bag

def instanciate_pokemon(pokemon):
    """
    Transforms a dictionary of Pokemon data into a functional Pokemon object instance.
    This reconstructs the full state of the Pokemon, including hidden stats like Effort Values (EVs).
    """
    # Create the base object with core attributes
    my_pokemon = Pokemon(
        pokemon['name'], 
        pokemon['original_name'], 
        pokemon['hp'],
        pokemon['hp_max'],
        pokemon['strength'], 
        pokemon['defense'],
        pokemon['type'],
        pokemon['level'], 
        pokemon['speed'], 
        pokemon['stage']
    )
    
    # Restore progression and state
    my_pokemon.set_xp(pokemon['xp'])
    my_pokemon.set_state(pokemon['state'])
    my_pokemon.set_pet_name(pokemon['pet_name'])

    # Restore Effort Values (EVs) from the nested dictionary
    # These points determine how much a Pokemon's stats grow beyond their base level
    ev_manager = my_pokemon.get_effort_value()
    ev_manager.set_ev_hp(pokemon['ev']['hp'])
    ev_manager.set_ev_strength(pokemon['ev']['strength'])
    ev_manager.set_ev_defense(pokemon['ev']['defense'])
    ev_manager.set_ev_speed(pokemon['ev']['speed'])
    ev_manager.set_ev_xp(pokemon['ev']['xp'])

    return my_pokemon

def instanciate_bag(player):
    """
    Reconstructs the player's Bag object from saved inventory data.
    Ensures that the player starts with the correct number of consumables.
    """
    player_bag = Bag()
    player_bag.set_potion(player["potions"])
    player_bag.set_pokeball(player["pokeball"])

    return player_bag