class Pokedex:
    def __init__(self):
        self.pokemon = {}

    def add_pokemon(self, name, type):
        self.pokemon[name] = type

    def get_pokemon_type(self, name):
        return self.pokemon.get(name, "Unknown")

    def list_pokemon(self):
        return list(self.pokemon.keys())