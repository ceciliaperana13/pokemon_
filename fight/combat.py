import json


class Combat:
    """
    Classe gérant les combats entre Pokémon.
    
    Cette classe charge automatiquement :
    - Le tableau d'efficacité depuis efficacite_types.txt
    - Enregistre les Pokémon rencontrés dans pokedex.json
    """
    
    def __init__(self, pokemon1, pokemon2, fichier_efficacite="efficacite_types.txt"):
        """
        Initialise un combat entre deux Pokémon.
        
        Args:
            pokemon1: Le premier Pokémon (objet avec attributs: nom, type, pv, attaque, defense)
            pokemon2: Le deuxième Pokémon
            fichier_efficacite: Chemin vers le fichier d'efficacité des types
        """
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.vainqueur = None
        self.perdant = None
        
        # Charger le tableau d'efficacité depuis le fichier
        self.efficacite_types = self._charger_efficacite(fichier_efficacite)
    
    def _charger_efficacite(self, fichier):
        """
        Charge le tableau d'efficacité depuis un fichier texte.
        
        Format du fichier:
        attaquant|defenseur|multiplicateur
        
        Args:
            fichier: Chemin vers le fichier d'efficacité
            
        Returns:
            dict: Dictionnaire d'efficacité des types
        """
        efficacite = {}
        
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    # Ignorer les lignes vides et les commentaires
                    ligne = ligne.strip()
                    if not ligne or ligne.startswith('#'):
                        continue
                    
                    # Parser la ligne
                    parties = ligne.split('|')
                    if len(parties) == 3:
                        attaquant, defenseur, multiplicateur = parties
                        attaquant = attaquant.strip().lower()
                        defenseur = defenseur.strip().lower()
                        multiplicateur = float(multiplicateur.strip())
                        
                        # Créer la structure imbriquée
                        if attaquant not in efficacite:
                            efficacite[attaquant] = {}
                        efficacite[attaquant][defenseur] = multiplicateur
            
            return efficacite
            
        except FileNotFoundError:
            # Si le fichier n'existe pas, utiliser le tableau par défaut
            return self._get_efficacite_defaut()
        except Exception as e:
            # En cas d'erreur, utiliser le tableau par défaut
            return self._get_efficacite_defaut()
    
    def _get_efficacite_defaut(self):
        """Retourne le tableau d'efficacité par défaut."""
        return {
            'feu': {'feu': 0.5, 'eau': 0.5, 'plante': 2.0, 'electrique': 1.0, 'terre': 1.0, 'vol': 1.0},
            'eau': {'feu': 2.0, 'eau': 0.5, 'plante': 0.5, 'electrique': 1.0, 'terre': 2.0, 'vol': 1.0},
            'plante': {'feu': 0.5, 'eau': 2.0, 'plante': 0.5, 'electrique': 1.0, 'terre': 2.0, 'vol': 0.5},
            'electrique': {'feu': 1.0, 'eau': 2.0, 'plante': 0.5, 'electrique': 0.5, 'terre': 0.0, 'vol': 2.0},
            'terre': {'feu': 2.0, 'eau': 1.0, 'plante': 0.5, 'electrique': 2.0, 'terre': 1.0, 'vol': 0.0},
            'vol': {'feu': 1.0, 'eau': 1.0, 'plante': 2.0, 'electrique': 0.5, 'terre': 1.0, 'vol': 1.0}
        }
    
    def calculer_degats(self, attaquant, defenseur):
        """
        Calcule les dégâts infligés en fonction du type de l'attaquant et du défenseur.
        
        Args:
            attaquant: Le Pokémon qui attaque
            defenseur: Le Pokémon qui défend
            
        Returns:
            float: Les dégâts calculés avec le multiplicateur de type
        """
        type_attaquant = attaquant.type.lower()
        type_defenseur = defenseur.type.lower()
        
        # Récupère le multiplicateur d'efficacité
        if type_attaquant in self.efficacite_types:
            if type_defenseur in self.efficacite_types[type_attaquant]:
                multiplicateur = self.efficacite_types[type_attaquant][type_defenseur]
            else:
                multiplicateur = 1.0
        else:
            multiplicateur = 1.0
        
        # Calcule les dégâts de base
        degats = attaquant.attaque * multiplicateur
        
        return degats
    
    def infliger_degats(self, attaquant, defenseur):
        """
        Inflige des dégâts au défenseur en tenant compte de sa défense.
        
        Args:
            attaquant: Le Pokémon qui attaque
            defenseur: Le Pokémon qui subit les dégâts
            
        Returns:
            float: Les points de vie retirés
        """
        # Calcule les dégâts bruts
        degats_bruts = self.calculer_degats(attaquant, defenseur)
        
        # Applique la réduction de défense (défense réduit les dégâts)
        reduction = defenseur.defense * 0.5
        degats_finaux = max(1, degats_bruts - reduction)
        
        # Retire les PV
        pv_avant = defenseur.pv
        defenseur.pv = max(0, defenseur.pv - degats_finaux)
        pv_retires = pv_avant - defenseur.pv
        
        return pv_retires
    
    def est_termine(self):
        """
        Vérifie si le combat est terminé.
        
        Returns:
            bool: True si un Pokémon n'a plus de PV, False sinon
        """
        return self.pokemon1.pv <= 0 or self.pokemon2.pv <= 0
    
    def determiner_vainqueur(self):
        """
        Détermine le vainqueur et le perdant du combat.
        
        Returns:
            tuple: (vainqueur, perdant) - Les objets Pokémon
        """
        if self.pokemon1.pv <= 0:
            self.vainqueur = self.pokemon2
            self.perdant = self.pokemon1
        elif self.pokemon2.pv <= 0:
            self.vainqueur = self.pokemon1
            self.perdant = self.pokemon2
        else:
            # Si les deux sont encore debout, on compare les PV
            if self.pokemon1.pv > self.pokemon2.pv:
                self.vainqueur = self.pokemon1
                self.perdant = self.pokemon2
            else:
                self.vainqueur = self.pokemon2
                self.perdant = self.pokemon1
        
        return self.vainqueur, self.perdant
    
    def get_nom_vainqueur(self):
        """
        Renvoie le nom du Pokémon vainqueur.
        
        Returns:
            str: Le nom du vainqueur ou None si le combat n'est pas terminé
        """
        if self.vainqueur is None:
            self.determiner_vainqueur()
        
        return self.vainqueur.nom if self.vainqueur else None
    
    def get_nom_perdant(self):
        """
        Renvoie le nom du Pokémon perdant.
        
        Returns:
            str: Le nom du perdant ou None si le combat n'est pas terminé
        """
        if self.perdant is None:
            self.determiner_vainqueur()
        
        return self.perdant.nom if self.perdant else None
    
    def get_noms_participants(self):
        """
        Renvoie les noms du vainqueur et du perdant.
        
        Returns:
            dict: {'vainqueur': nom, 'perdant': nom}
        """
        if self.vainqueur is None or self.perdant is None:
            self.determiner_vainqueur()
        
        return {
            'vainqueur': self.vainqueur.nom if self.vainqueur else None,
            'perdant': self.perdant.nom if self.perdant else None
        }
    
    def enregistrer_dans_pokedex(self, pokemon, fichier_pokedex="pokedex.json"):
        """
        Enregistre un Pokémon rencontré dans le Pokédex (fichier JSON).
        
        Args:
            pokemon: Le Pokémon à enregistrer
            fichier_pokedex: Chemin vers le fichier pokedex.json
            
        Returns:
            bool: True si le Pokémon a été ajouté, False s'il était déjà présent
        """
        try:
            # Charger le Pokédex existant
            try:
                with open(fichier_pokedex, 'r', encoding='utf-8') as f:
                    pokedex = json.load(f)
            except FileNotFoundError:
                pokedex = []
            
            # Vérifier si le Pokémon existe déjà (par nom)
            for p in pokedex:
                if p.get('nom') == pokemon.nom:
                    return False
            
            # Ajouter le Pokémon
            pokemon_data = {
                'nom': pokemon.nom,
                'type': pokemon.type,
                'pv': getattr(pokemon, 'pv_max', pokemon.pv),
                'attaque': pokemon.attaque,
                'defense': pokemon.defense
            }
            
            # Ajouter l'ID si disponible
            if hasattr(pokemon, 'id'):
                pokemon_data['id'] = pokemon.id
            
            # Ajouter la description si disponible
            if hasattr(pokemon, 'description'):
                pokemon_data['description'] = pokemon.description
            
            pokedex.append(pokemon_data)
            
            # Sauvegarder le Pokédex
            with open(fichier_pokedex, 'w', encoding='utf-8') as f:
                json.dump(pokedex, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            return False
    
    def lancer_combat(self, afficher_details=True, fichier_pokedex="pokedex.json"):
        """
        Lance le combat complet entre les deux Pokémon.
        
        Args:
            afficher_details: Si True, affiche les détails du combat
            fichier_pokedex: Chemin vers le fichier pokedex.json
            
        Returns:
            str: Le nom du vainqueur
        """
        if afficher_details:
            print("\n" + "=" * 60)
            print(f"⚔️  COMBAT: {self.pokemon1.nom} VS {self.pokemon2.nom}  ⚔️".center(60))
            print("=" * 60)
        
        # Enregistre les deux Pokémon dans le Pokédex
        self.enregistrer_dans_pokedex(self.pokemon1, fichier_pokedex)
        self.enregistrer_dans_pokedex(self.pokemon2, fichier_pokedex)
        
        tour = 1
        
        # Boucle de combat
        while not self.est_termine():
            if afficher_details:
                print(f"\n--- Tour {tour} ---")
            
            # Le Pokémon 1 attaque
            self.infliger_degats(self.pokemon1, self.pokemon2)
            
            # Vérifie si le combat est terminé
            if self.est_termine():
                break
            
            # Le Pokémon 2 attaque
            self.infliger_degats(self.pokemon2, self.pokemon1)
            
            tour += 1
            
            # Sécurité pour éviter les boucles infinies
            if tour > 100:
                break
        
        # Détermine le vainqueur
        vainqueur, perdant = self.determiner_vainqueur()
        
        if afficher_details:
            print("\n" + "=" * 60)
            print(f"🏆 {vainqueur.nom} remporte le combat !".center(60))
            print("=" * 60)
        
        return vainqueur.nom