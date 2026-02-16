import json
import os

class SaveManager:
    # On définit les deux fichiers séparés
    GAME_FILE = "sauvegarde.json"
    POKEDEX_FILE = "pokedex.json"

    @classmethod
    def init_files(cls):
        """Crée les fichiers par défaut s'ils n'existent pas."""
        if not os.path.exists(cls.GAME_FILE):
            cls.save_game_data({"current_pokemon": "1", "x": 400, "y": 300})
            print("Fichier sauvegarde.json initialisé.")
            
        if not os.path.exists(cls.POKEDEX_FILE):
            cls.save_pokedex_data({"discovered": []})
            print("Fichier pokedex.json initialisé.")

    @classmethod
    def load_exists(cls):
        """Vérifie si la sauvegarde de jeu existe."""
        return os.path.exists(cls.GAME_FILE)
    
    @classmethod
    def reset_game(cls):
        """Supprime la sauvegarde de progression pour recommencer à zéro."""
        if os.path.exists(cls.GAME_FILE):
            os.remove(cls.GAME_FILE)
            print("Sauvegarde supprimée. Nouvelle partie prête.")

    @classmethod
    def reset_pokedex(cls):
        """Réinitialise complètement le Pokédex (à utiliser avec prudence !)."""
        if os.path.exists(cls.POKEDEX_FILE):
            os.remove(cls.POKEDEX_FILE)
            cls.save_pokedex_data({"discovered": []})
            print("Pokédex réinitialisé.")

    # --- GESTION DE LA SAUVEGARDE (sauvegarde.json) ---
    @classmethod
    def get_game_data(cls):
        """Récupère les données de progression avec sécurité anti-crash."""
        if not os.path.exists(cls.GAME_FILE):
            cls.init_files()
            
        with open(cls.GAME_FILE, "r", encoding="utf-8") as f:
            try:
                # On essaie de lire le JSON
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                # SI LE FICHIER EST VIDE OU CORROMPU :
                print(f"Attention : {cls.GAME_FILE} était vide ou invalide. Réinitialisation...")
                default_data = {"current_pokemon": "1", "x": 400, "y": 300}
                cls.save_game_data(default_data) # On réécrit un fichier propre
                return default_data

    @classmethod
    def save_game_data(cls, data):
        """Sauvegarde la progression (position, pokemon actuel)."""
        with open(cls.GAME_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def save_pokemon_choice(cls, pokemon_id):
        """Met à jour le Pokémon actuel du joueur."""
        data = cls.get_game_data()
        data["current_pokemon"] = str(pokemon_id).split(" - ")[0].strip()
        cls.save_game_data(data)

    # --- GESTION DU POKEDEX (pokedex.json) ---
    @classmethod
    def get_pokedex_data(cls):
        """Récupère la liste des Pokémon rencontrés."""
        if not os.path.exists(cls.POKEDEX_FILE): cls.init_files()
        with open(cls.POKEDEX_FILE, "r") as f:
            return json.load(f)

    @classmethod
    def save_pokedex_data(cls, data):
        """Sauvegarde la collection du Pokédex."""
        with open(cls.POKEDEX_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def register_encounter(cls, pokemon_id):
        """Ajoute un Pokémon au Pokédex (sans doublon)."""
        data = cls.get_pokedex_data()
        clean_id = str(pokemon_id).split(" - ")[0].strip()
        
        if clean_id not in data["discovered"]:
            data["discovered"].append(clean_id)
            cls.save_pokedex_data(data)
            print(f"Pokédex : {clean_id} enregistré !")

    @classmethod
    def reset_game(cls):
        """Réinitialise la progression mais GARDE le Pokédex."""
        data = {"current_pokemon": "1", "x": 400, "y": 300}
        cls.save_game_data(data)