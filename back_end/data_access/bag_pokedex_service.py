import json
from .util import instanciate_bag
from __settings__ import PLAYER_POKEDEX

def save_bag_to_pokedex(player, bag):
    """
    Saves the current state of a player's bag to the permanent storage.
    Converts the Bag object into a dictionary before updating the JSON file.
    """
    # Load the existing database
    with open(PLAYER_POKEDEX, "r") as file:
        player_pokedex = json.load(file)

    # Update the specific player's 'bag' section with the new quantities
    player_pokedex[player]["bag"].update(bag.get_dict())

    # Write the updated data back to the file with clean formatting
    with open(PLAYER_POKEDEX, "w", encoding="UTF-8") as file:
        json.dump(player_pokedex, file, indent=4)

def get_bag_from_pokedex(player):
    """
    Retrieves the bag data for a specific player and reconstructs it into a Bag object.
    Used when loading a game session to restore item counts.
    """
    with open(PLAYER_POKEDEX, "r") as file:
        # Extract only the inventory data for the specified player
        player_bag_data = json.load(file)[player]["bag"]

    # Reconstruct the Bag object from the raw dictionary data (Hydration)
    bag = instanciate_bag(player_bag_data)
    return bag