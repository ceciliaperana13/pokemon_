import json, os, random
from __settings__ import PLAYER_POKEDEX
from .wild_pokemons import get_random_wild_pokemon
from .pokemon_pokedex_service import save_pokemon_to_pokedex
from .bag_pokedex_service import save_bag_to_pokedex
from ..models.bag import Bag
from ..generate_pokemon.create_pokemon import level_from_stage
from ..models.pokemon import Pokemon

# back to front
def get_player_names():
    with open(PLAYER_POKEDEX, "r", encoding="UTF-8") as file:
        player_keys_dictionary = json.load(file)
    return player_keys_dictionary.keys()

def does_player_exist(player):
    if not os.path.exists(PLAYER_POKEDEX):
        with open(PLAYER_POKEDEX, "w", encoding="UTF-8") as file:
            json.dump({}, file)

    with open(PLAYER_POKEDEX, "r", encoding="UTF-8") as file:
        player_keys_dictionary = list(json.load(file).keys())

    return player in player_keys_dictionary


# front to back
def create_player(player, pokemon):

    with open(PLAYER_POKEDEX, "r", encoding="UTF-8") as file:
        players_dictionary = json.load(file)

    if player not in players_dictionary.keys():
        player_bag = Bag()
        players_dictionary[player] = {
            "bag" : {},
            "pokemons" : {}
            }
    else:
        return
            
    with open(PLAYER_POKEDEX, "w", encoding="UTF-8") as file:
        json.dump(players_dictionary, file, indent=4)
    
    save_pokemon_to_pokedex(player, pokemon)
    save_bag_to_pokedex(player, player_bag)


def create_specific_starter(name, first_stage_name, type_list, stage):
    """
    Crée un Pokémon starter spécifique avec les paramètres donnés.
    """
    level = 5  # Niveau de départ fixe
    
    # Stats de base pour un starter niveau 5
    hp = random.randrange(10, 31) + level * 3
    strength = random.randrange(2, 31) + level * 3
    speed = random.randrange(2, 31) + level * 3
    defense_point = random.randrange(2, 21) + level * 3
    
    # Créer le Pokémon
    my_pokemon = Pokemon(name, first_stage_name, hp, hp, strength, defense_point, type_list, level, speed, stage)
    
    # Définir l'XP
    xp = random.randrange(my_pokemon.get_level()**3, (my_pokemon.get_level()+1)**3)
    my_pokemon.set_xp(xp)
    
    return my_pokemon


# Compteur global pour les starters
_starter_index = 0

def get_starter_pokemon():
    """
    Retourne un des 3 starters classiques à chaque appel.
    Cycle entre Bulbizarre, Salamèche et Carapuce.
    """
    global _starter_index
    
    # Définir les 3 starters classiques
    starters = [
        {"name": "Bulbasaur", "first_stage_name": "Bulbasaur", "type_list": ["grass", "poison"], "stage": 1},
        {"name": "Charmander", "first_stage_name": "Charmander", "type_list": ["fire"], "stage": 1},
        {"name": "Squirtle", "first_stage_name": "Squirtle", "type_list": ["water"], "stage": 1}
    ]
    
    # Récupérer le starter actuel
    starter_data = starters[_starter_index % 3]
    
    # Incrémenter l'index pour le prochain appel
    _starter_index += 1
    
    # Créer le Pokémon starter
    my_pokemon = create_specific_starter(
        starter_data["name"],
        starter_data["first_stage_name"],
        starter_data["type_list"],
        starter_data["stage"]
    )
    
    print(f"✅ Starter généré: {my_pokemon.name} (Type: {', '.join(my_pokemon.type)})")
    
    return my_pokemon