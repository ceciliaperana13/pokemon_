import back_end.data_access.player_pokedex_service as player_pokedex_service
import back_end.data_access.pokemon_pokedex_service as pokemon_pokedex_service
import back_end.data_access.wild_pokemons as wild_pokemons
import back_end.data_access.bag_pokedex_service as bag_pokedex_service
import json
import os

# --- Player Pokedex Service ---

def get_player_names():
    """Retrieves the list of all existing player profile names."""
    player_names = list(player_pokedex_service.get_player_names())
    return player_names

def get_player_pokemons(player):
    """Retrieves the current team of Pokemon for a specific player."""
    player_pokemons = list(player_pokedex_service.get_player_pokemons(player))
    return player_pokemons

def create_player(player, pokemon):
    """Initializes a new player profile with their chosen starter."""
    player_pokedex_service.create_player(player, pokemon)

def get_starter_pokemons():
    """Retrieves the standard selection of 3 starter Pokemon."""
    pokemon_list = []
    for index in range(3):
        pokemon = player_pokedex_service.get_starter_pokemon()
        pokemon_list.append(pokemon)
    return pokemon_list

def does_player_exist(player):
    """Checks if a player name is already registered in the database."""
    is_player = player_pokedex_service.does_player_exist(player)
    return is_player

# --- Pokemon Pokedex Service ---

def get_all_pokemons_from_pokedex(player_name):
    """Fetches the full collection of Pokemon associated with a player."""
    pokemon_list = pokemon_pokedex_service.get_all_pokemons_from_pokedex(player_name)
    return pokemon_list

def get_first_pokemon(player_name):
    """Gets the lead Pokemon from the player's team."""
    pokemon = pokemon_pokedex_service.get_first_pokemon(player_name)
    return pokemon

def save_pokemon_to_pokedex(player, pokemon):
    """Persists a new or updated Pokemon to the player's collection."""
    pokemon_pokedex_service.save_pokemon_to_pokedex(player, pokemon)

# --- Wild Pokemon ---

def get_random_wild_pokemon():
    """Generates a random Pokemon encounter from the wild encounter table."""
    return wild_pokemons.get_random_wild_pokemon()

def save_wild_pokemon(my_pokemon):
    """Saves the state of a wild Pokemon (used for persistence during battles)."""
    wild_pokemons.save_wild_pokemon(my_pokemon)

# --- Bag / Inventory ---

def get_bag_from_pokedex(player):
    """Retrieves the player's inventory (items, potions, etc.)."""
    bag = bag_pokedex_service.get_bag_from_pokedex(player)
    return bag

def save_bag_to_pokedex(player, bag):
    """Saves the current state of the player's inventory."""
    bag_pokedex_service.save_bag_to_pokedex(player, bag)


# ========================================
#   DISCOVERED POKEDEX SAVE FUNCTIONS
# ========================================

def save_player_data(player_name, data):
    """
    Updates the 'player_pokedex' (the list of seen/caught IDs) in the JSON database.
    """
    try:
        json_path = "back_end/data/player_pokedex.json"
        
        # Check if the database file exists
        if not os.path.exists(json_path):
            print(f" Error: The file {json_path} was not found.")
            return False

        # Load current database state
        with open(json_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        # Validate that the player exists in the record
        if player_name not in all_data:
            print(f"⚠ Player {player_name} does not exist in player_pokedex.json")
            return False
        
        # Update the specific Pokedex discovery list
        if "player_pokedex" in data:
            all_data[player_name]["player_pokedex"] = data["player_pokedex"]
        
        # Write back to JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)
        
        print(f" Pokedex successfully saved for {player_name}")
        return True
        
    except Exception as e:
        print(f" Error during save process: {e}")
        return False

def load_player_data(player_name):
    """
    Loads the discovery data for a specific player.
    Returns a dictionary structured for the UI components.
    """
    try:
        json_path = "back_end/data/player_pokedex.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        if player_name not in all_data:
            return None
        
        player_data = all_data[player_name]
        
        # Return the structure required by the Pause Menu and Pokedex UI
        return {
            "player_name": player_name,
            "player_pokedex": player_data.get("player_pokedex", [])
        }
        
    except Exception as e:
        print(f"❌ Error during loading: {e}")
        return None