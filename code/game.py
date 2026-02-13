import pygame
import sys
from keylistener import KeyListener
from map import Map  
from player import Player
from screen import Screen
from fight.interfaceFight import InterfaceFight


class Game:
    def __init__(self):
        self.running: bool = True
        self.screen: Screen = Screen()
        self.map: Map = Map(self.screen)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.keylistener, self.screen, 512, 288)
        self.map.add_player(self.player)
        
        # Configuration du callback de combat
        self.map.set_battle_callback(self.launch_battle)
        
        # État du jeu
        self.in_battle: bool = False
        self.clock = pygame.time.Clock()

    def launch_battle(self) -> None:
        """Lance l'interface de combat."""
        print(f"Combat déclenché à la position: "
              f"({int(self.player.position.x // 16)}, {int(self.player.position.y // 16)})")
        self.in_battle = True

    def handle_battle(self) -> None:
        """Gère le combat et le retour à la carte."""
        # Sauvegarde temporaire de l'écran de jeu (optionnel)
        # game_surface = self.screen.get_display().copy()
        
        # Lance l'interface de combat
        battle = InterfaceFight()
        battle.run()
        
        # Après le combat
        if battle.get_result():
            print("Retour à la carte après le combat")
            
            # Réinitialise l'état
            self.in_battle = False
            
            # Réinitialise pygame display après la fermeture de l'interface de combat
            pygame.init()
            self.screen = Screen()
            
            # Recrée la carte avec le joueur
            old_position = self.player.position.copy()
            self.map = Map(self.screen)
            self.player = Player(self.keylistener, self.screen, 
                                int(old_position.x), int(old_position.y))
            self.map.add_player(self.player)
            self.map.set_battle_callback(self.launch_battle)

    def run(self) -> None:
        while self.running:
            if self.in_battle:
                # Mode combat
                self.handle_battle()
            else:
                # Mode exploration normal
                self.handle_input()
                self.map.update()
                self.screen.update()
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)

