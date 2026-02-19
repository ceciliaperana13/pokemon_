class Bag:
    """
    Manages the player's inventory of consumable items.
    Used during battles to heal Pokemon or capture wild ones.
    """
    def __init__(self):
        # Default starting inventory
        self.potion = 10
        self.pokeball = 15

    # --- Getters ---

    def get_potion(self):
        """Returns the current count of potions available."""
        return self.potion
    
    def get_pokeball(self):
        """Returns the current count of Pokeballs available."""
        return self.pokeball
    
    # --- Setters ---

    def set_potion(self, new_value):
        """Updates the potion count (e.g., after purchase or use)."""
        self.potion = new_value

    def set_pokeball(self, new_value):
        """Updates the Pokeball count (e.g., after a capture attempt)."""
        self.pokeball = new_value

    def get_dict(self):
        """
        Returns a dictionary representation of the bag.
        Useful for JSON serialization and saving player progress.
        """
        return {
            "potions" : self.get_potion(),
            "pokeball" : self.get_pokeball()
        }