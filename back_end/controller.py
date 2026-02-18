import back_end.data_access.player_pokedex_service as player_pokedex_service
import back_end.data_access.pokemon_pokedex_service as pokemon_pokedex_service
import back_end.data_access.wild_pokemons as wild_pokemons
import back_end.data_access.bag_pokedex_service as bag_pokedex_service
import json
import os

# Player pokedex service
def get_player_names():
    player_names = list(player_pokedex_service.get_player_names())
    return player_names

def get_player_pokemons(player):
    player_pokemons = list(player_pokedex_service.get_player_pokemons(player))
    return player_pokemons

def create_player(player, pokemon):
    player_pokedex_service.create_player(player, pokemon)

def get_starter_pokemons():
    pokemon_list = []
    for index in range(3):
        pokemon = player_pokedex_service.get_starter_pokemon()
        pokemon_list.append(pokemon)
    return pokemon_list

def does_player_exist(player):
    is_player = player_pokedex_service.does_player_exist(player)
    return is_player

# Pokemon pokedex service
def get_all_pokemons_from_pokedex(player_name):
    pokemon_list = pokemon_pokedex_service.get_all_pokemons_from_pokedex(player_name)
    return pokemon_list

def get_first_pokemon(player_name):
    pokemon = pokemon_pokedex_service.get_first_pokemon(player_name)
    return pokemon

def save_pokemon_to_pokedex(player, pokemon):
    pokemon_pokedex_service.save_pokemon_to_pokedex(player, pokemon)

# Wild pokemon
def get_random_wild_pokemon():
    return wild_pokemons.get_random_wild_pokemon()

def save_wild_pokemon(my_pokemon):
    wild_pokemons.save_wild_pokemon(my_pokemon)

# Bag
def get_bag_from_pokedex(player):
    bag = bag_pokedex_service.get_bag_from_pokedex(player)
    return bag

def save_bag_to_pokedex(player, bag):
    bag_pokedex_service.save_bag_to_pokedex(player, bag)


# ========================================
# 🆕 FONCTIONS DE SAUVEGARDE DU POKÉDEX DÉCOUVERT
# ========================================

def save_player_data(player_name, data):
    try:
        # 🟢 CORRECTION : "back_end/..." au lieu de "/back_end/..."
        json_path = "back_end/data/player_pokedex.json"
        
        if not os.path.exists(json_path):
            print(f"❌ Erreur : Le fichier {json_path} est introuvable.")
            return False

        with open(json_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        if player_name not in all_data:
            print(f"⚠ Joueur {player_name} n'existe pas dans player_pokedex.json")
            return False
        
        if "player_pokedex" in data:
            all_data[player_name]["player_pokedex"] = data["player_pokedex"]
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Pokédex sauvegardé pour {player_name}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        return False

def load_player_data(player_name):
    try:
        json_path = "back_end/data/player_pokedex.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        if player_name not in all_data:
            return None
        
        player_data = all_data[player_name]
        
        # On renvoie la structure attendue par le menu de pause
        return {
            "player_name": player_name,
            "player_pokedex": player_data.get("player_pokedex", [])
        }
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        return None