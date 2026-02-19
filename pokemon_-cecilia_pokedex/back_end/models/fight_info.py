class FightInfo():
    """
    A helper class used to store and format information about battle events.
    This data is typically consumed by the UI to display combat logs to the player.
    """
    def __init__(self,):
        self.efficiency = ""     # e.g., "Super effective", "Critical hit !!"
        self.attack_type = ""    # The elemental type of the attack used
        self.total_damage = 0    # Final calculated damage value
        self.actual_hp = 0       # Current HP of the target (for status bars)
        self.flee_message = ""   # Outcome message when attempting to run away

    def set_all_values(self, efficiency, attack_type, damage):
        """Updates the core combat data after an attack is executed."""
        self.efficiency = efficiency
        self.attack_type = attack_type
        self.total_damage = damage

    def set_who_attack_message(self, pokemon):
        """Generates a string identifying the attacker and the move type used."""
        return f"Attack type {self.attack_type} from {pokemon.name} "
    
    def get_damage_message(self):
        """
        Returns a formatted string describing the attack's effectiveness 
        and the amount of damage dealt, handling singular/plural grammar.
        """
        if self.total_damage > 1:
            return f"{self.efficiency} : {self.total_damage} damages"
        else:
            return f"{self.efficiency} : {self.total_damage} damage"

    # --- Fleeing Logic Messages ---

    def set_flee_trainer_message(self):
        """Message displayed when trying to escape a mandatory trainer battle."""
        self.flee_message = "You can't escape a fight against another pokemon trainer"
    
    def set_fail_flee_message(self):
        """Message displayed when a flee attempt from a wild Pokemon fails."""
        self.flee_message = "You failed to flee..."

    def set_success_flee_message(self):
        """Message displayed when the player successfully ends the encounter."""
        self.flee_message = "You escaped successfully"