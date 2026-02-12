from typing import Dict


class TypeEffectiveness:
    """Gère le tableau d'efficacité des types."""
    
    def __init__(self, fichier: str = "efficacite_types.txt"):
        """
        Initialise le système d'efficacité des types.
        
        Args:
            fichier: Chemin vers le fichier de configuration des types
        """
        self.efficacite = self._charger_efficacite(fichier)
    
    def _charger_efficacite(self, fichier: str) -> Dict[str, Dict[str, float]]:
        """
        Charge le tableau d'efficacité depuis un fichier.
        
        Format attendu : type_attaquant|type_defenseur|multiplicateur
        
        Args:
            fichier: Chemin vers le fichier
            
        Returns:
            Dictionnaire imbriqué {type_attaquant: {type_defenseur: multiplicateur}}
        """
        efficacite = {}
        
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if not ligne or ligne.startswith('#'):
                        continue
                    
                    parties = ligne.split('|')
                    if len(parties) == 3:
                        attaquant, defenseur, multiplicateur = parties
                        attaquant = attaquant.strip().lower()
                        defenseur = defenseur.strip().lower()
                        multiplicateur = float(multiplicateur.strip())
                        
                        if attaquant not in efficacite:
                            efficacite[attaquant] = {}
                        efficacite[attaquant][defenseur] = multiplicateur
            
            return efficacite
            
        except:
            return self._get_efficacite_defaut()
    
    def _get_efficacite_defaut(self) -> Dict[str, Dict[str, float]]:
        """
        Retourne le tableau d'efficacité par défaut.
        
        Returns:
            Dictionnaire d'efficacité avec les types de base
        """
        return {
            'feu': {
                'feu': 0.5, 'eau': 0.5, 'plante': 2.0, 
                'electrique': 1.0, 'terre': 1.0, 'vol': 1.0, 'normal': 1.0
            },
            'eau': {
                'feu': 2.0, 'eau': 0.5, 'plante': 0.5, 
                'electrique': 1.0, 'terre': 2.0, 'vol': 1.0, 'normal': 1.0
            },
            'plante': {
                'feu': 0.5, 'eau': 2.0, 'plante': 0.5, 
                'electrique': 1.0, 'terre': 2.0, 'vol': 0.5, 'normal': 1.0
            },
            'electrique': {
                'feu': 1.0, 'eau': 2.0, 'plante': 0.5, 
                'electrique': 0.5, 'terre': 0.0, 'vol': 2.0, 'normal': 1.0
            },
            'terre': {
                'feu': 2.0, 'eau': 1.0, 'plante': 0.5, 
                'electrique': 2.0, 'terre': 1.0, 'vol': 0.0, 'normal': 1.0
            },
            'vol': {
                'feu': 1.0, 'eau': 1.0, 'plante': 2.0, 
                'electrique': 0.5, 'terre': 1.0, 'vol': 1.0, 'normal': 1.0
            },
            'normal': {
                'feu': 1.0, 'eau': 1.0, 'plante': 1.0, 
                'electrique': 1.0, 'terre': 1.0, 'vol': 1.0, 'normal': 1.0
            }
        }
    
    def get_multiplicateur(self, type_attaquant: str, type_defenseur: str) -> float:
        """
        Retourne le multiplicateur d'efficacité entre deux types.
        
        Args:
            type_attaquant: Type du Pokémon qui attaque
            type_defenseur: Type du Pokémon qui défend
            
        Returns:
            Multiplicateur (0.0, 0.5, 1.0, ou 2.0)
        """
        type_attaquant = type_attaquant.lower()
        type_defenseur = type_defenseur.lower()
        
        if type_attaquant in self.efficacite:
            return self.efficacite[type_attaquant].get(type_defenseur, 1.0)
        return 1.0
