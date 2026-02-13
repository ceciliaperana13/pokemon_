import re

class Utilitaire:
    @staticmethod
    def natural_sort_key(s):
       # Cette ligne découpe "10 - chenipan" en [10, " - chenipan"]
        # Python saura alors que 2 est plus petit que 10
        return [int(text) if text.isdigit() else text.lower() 
                for text in re.split('([0-9]+)', s)]

    @staticmethod
    def format_name(name): 
        """Nettoie le nom du fichier pour l'affichage (ex: '001_pika-chu' -> '001 Pika Chu')."""
        return name.replace("_", " ").replace("-", " ").title()
