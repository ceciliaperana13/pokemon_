import json

def charger_pokedex(fichier):
    
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Si le JSON contient un dictionnaire avec la clé 
    if isinstance(data, dict) and 'pokemon' in data:
        return data['pokemon']
    
    
    if isinstance(data, list):
        return data
    
    return []