import pygame
import sys
from data.pokedex import Pokedex
from data.CustumizerPokedex import CustomizerPokedex

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Configuration de la fenêtre
    LARGEUR = 1200
    HAUTEUR = 800
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Pokédex Ultime")
    
    # Charger l'icône
    try:
        pygame.display.set_icon(pygame.image.load("assets/icon.ico"))
    except:
        print("⚠️ Icône non trouvée, continuation sans icône")
    
    # Charger le Pokédex (le fichier JSON est dans le dossier data)
    try:
        pokedex = Pokedex("data/pokedex.json")  # ← CORRECTION ICI
        print(f"✅ {pokedex.nombre_pokemon()} Pokémon chargés avec succès !")
    except FileNotFoundError:
        print("❌ Erreur: Fichier pokedex.json non trouvé!")
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
                if event.button == 1:  # Clic gauche
                    interface.est_clique(event.pos)
                elif event.button == 4:  # Molette haut
                    interface.defiler(-1)
                elif event.button == 5:  # Molette bas
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
    print("🔴 POKÉDEX ULTIME 🔴")
    print("=" * 50)
    print("\n📋 Contrôles:")
    print("  • Clic sur un Pokémon pour voir ses stats")
    print("  • Molette / Flèches pour défiler")
    print("  • ESC pour quitter")
    print("\n" + "=" * 50 + "\n")
    
    main()