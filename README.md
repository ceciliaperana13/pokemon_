# pokemon_
📋 Prérequis

Python 3.10+
Les dépendances suivantes :

bashpip install pygame pytmx pyscroll

🚀 Lancer le jeu
bashpython main.py

🗂️ Structure du projet
pokemon_/
│
├── main.py                      # Point d'entrée
├── __settings__.py              # Constantes globales (couleurs, polices, chemins)
│
├── assets/
│   ├── map/                     # Fichiers de carte (.tmx)
│   ├── sprite/                  # Sprites joueur et Pokémon
│   ├── wallpaper/               # Fond animé du menu (wallpaper.mp4)
│   └── logo/                    # Icône Pokédex
│
├── back_end/
│   ├── controller.py            # Fonctions de sauvegarde/chargement
│   ├── data/
│   │   └── pokedex.json         # Base de données des Pokémon
│   └── models/
│       └── fight.py             # Logique des combats
│
└── front_end/
    ├── screen.py                # Gestion de l'écran pygame
    ├── sounds.py                # Contrôleur audio
    ├── menu/
    │   ├── menu.py              # Menu principal
    │   ├── pause_menu.py        # Menu pause
    │   ├── name_input.py        # Saisie du nom du joueur
    │   ├── select_player.py     # Sélection de sauvegarde
    │   ├── change_pokemon.py    # Changement de Pokémon actif
    │   ├── change_pokemon_infight.py  # Changement pendant le combat
    │   ├── attack_type_menu.py  # Menu des attaques
    │   ├── bagmenu.py           # Menu du sac
    │   ├── infomenu.py          # Menu d'information
    │   ├── util_tool.py         # Utilitaires d'affichage
    │   └── display_pokemon_stat.py   # Stats des Pokémon
    └── gameplay/
        ├── game.py              # Boucle principale du jeu
        ├── map.py               # Gestion de la carte et des zones
        ├── player.py            # Joueur et déplacements
        ├── entity.py            # Classe de base des entités
        ├── in_fight.py          # Écran de combat
        ├── healthdisplay.py     # Barre de vie
        ├── pokedex_manager.py   # Logique du Pokédex
        ├── CustumizerPokedex.py # Interface UI du Pokédex
        ├── pokedexButton.py     # Bouton Pokédex en jeu
        ├── keylistener.py       # Gestion des touches
        └── switch.py            # Gestion des transitions de carte

🎮 Contrôles
ToucheActionZ / ↑Se déplacer vers le hautS / ↓Se déplacer vers le basQ / ←Se déplacer vers la gaucheD / →Se déplacer vers la droiteBActiver / désactiver le véloÉCHAPOuvrir le menu pausePOuvrir / fermer le PokédexEntréeConfirmer une sélection↑ / ↓ dans les menusNaviguer entre les options

🧭 Menu principal

Start Game — Créer une nouvelle partie (saisie du nom + choix du Pokémon de départ)
Resume Game — Charger une sauvegarde existante
Exit — Quitter le jeu


⚔️ Système de combat
Les combats se déclenchent automatiquement en marchant dans les zones d'herbe. Le combat est au tour par tour :

Attack — Choisir une attaque parmi celles du Pokémon actif
Bag — Utiliser une potion ou une Pokéball
Team — Changer de Pokémon actif (affiche la team de la sauvegarde)
Info — Voir les stats des Pokémon
Flee / Exit — Tenter de fuir ou quitter après une victoire

Résultat du combat

Victoire — Gain d'XP, niveau possible, évolution possible
Capture — Le Pokémon ennemi rejoint la collection
Défaite — L'ennemi gagne de l'XP


💾 Sauvegarde
Les données sont sauvegardées automatiquement après chaque combat (victoire, fuite ou capture). La sauvegarde inclut :

L'équipe de Pokémon et leurs HP/XP
Le contenu du sac (potions, Pokéballs)
Les Pokémon sauvages capturés


📖 Pokédex
Le Pokédex se consulte en appuyant sur P ou via le bouton en bas à droite de l'écran. Les Pokémon sont automatiquement enregistrés lors d'un chargement de sauvegarde ou d'une rencontre.

🗺️ Cartes disponibles
CarteDescriptionmap_0Carte principale extérieurehouse_*Intérieurs de maisonspokeshopBoutique PokémonpokecenterCentre Pokémonlabo_*Laboratoireinter_*Zones de transition

⚙️ Paramètres (__settings__.py)
Les constantes globales configurables :
pythonREGULAR_FONT      # Police standard
POKE_FONT         # Police titre style Pokémon
BACKGROUND        # Couleur de fond des fenêtres
DARK_GREEN        # Couleur principale UI
LIGHT_GREEN       # Couleur de sélection UI
BATTLE_BACKGROUND # Image de fond des combats
BATTLE_FLOOR      # Image du sol en combat

🐛 Bugs connus et corrections apportées
ProblèmeFichier corrigéSolutionCrash display Surface quit à la fermeturegame.pypygame.quit() + sys.exit() dans le handler QUITTeam incorrecte en combat (toujours Pokémon 1)in_fight.py, player.py, map.pyPassage de self.team (liste complète) à ChangePokemonInFightFermeture via la croix relançait un menugame.pyRemplacement de self.running = False par sys.exit()Menu pause recréait une boucle Game imbriquéepause_menu.pySuppression du game.run() dans le case 2Nom du Pokémon absent de l'écran de victoireutil_tool.pyAjout de "{pokemon.name} is victorious!"
