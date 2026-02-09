import pygame
import sys
from pokedex import charger_pokedex
from CustumizerPokedex import CustomizerPokedex


def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Configuration de la fenêtre
    LARGEUR = 1200
    HAUTEUR = 800
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Pokédex Ultime ")
    
    
    # pygame.display.set_icon(pygame.image.load("icon.png"))
    pygame.display.set_icon(pygame.image.load("./assets/icon.ico"))
    # Charger le Pokédex
    try:
        pokedex = charger_pokedex("pokedex.json")
        print(f" {len(pokedex)} Pokémon chargés avec succès !")
    except FileNotFoundError:
        print(" Erreur: Fichier pokemon_data.json non trouvé!")
        sys.exit(1)
    
    # Créer l'interface
    interface = CustomizerPokedex(pokedex, LARGEUR, HAUTEUR)
    
    
    clock = pygame.time.Clock()
    FPS = 60
    
    # Boucle principale
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    interface.est_clique(event.pos)
                elif event.button == 4:  
                    interface.defiler(-1)
                elif event.button == 5:  
                    interface.defiler(1)
            
            elif event.type == pygame.MOUSEMOTION:
                interface.verifier_survol(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    interface.defiler(-1)
                elif event.key == pygame.K_DOWN:
                    interface.defiler(1)
        
        # Dessiner l'interface
        interface.dessiner(screen)
        
        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(FPS)
    
    # Quitter proprement
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("=" * 50)
    print(" POKÉDEX ULTIME ")
    print("=" * 50)
    print("\n Contrôles:")
    print("  • Clic sur un Pokémon pour voir ses stats")
    print("  • Molette / Flèches pour défiler")
    print("  • ESC pour quitter")
    print("\n" + "=" * 50 + "\n")
    
    main()