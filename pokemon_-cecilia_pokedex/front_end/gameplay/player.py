import pygame
from front_end.gameplay.entity import Entity
from .keylistener import KeyListener
from front_end.screen import Screen
from .switch import Switch
from front_end.gameplay.battlescreen import BattleScreen
from front_end.gameplay.in_fight import InFight
from front_end.menu.pause_menu import PauseMenu

class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int, player_name: str, pokemon: object):
        """
        Initializes the Player entity with input handling, screen context, and inventory.
        """
        super().__init__(keylistener, screen, x, y)
        self.switchs: list[Switch] | None = None  # Teleportation points or interactive triggers
        self.change_map = None                   # Current switch pending a map transition
        self.collisions = None                   # Rect objects the player cannot walk through
        
        # Load the bicycle spritesheet for faster movement
        self.spritesheet_bike = pygame.image.load("assets/sprite/hero_01_red_m_cycle_roll.png")
        
        self.player_name = player_name
        self.name = player_name
        self.is_fleeing = False
        self.speed = 1                           # Base movement speed (Walking)
        self.active_pokemon = pokemon
        self.flee_steps = 0                      # Counter for escape mechanics
        self.max_flee_steps = 100
        self.pause_menu = False

    def update(self) -> None:
        """Core update loop for the player logic."""
        self.check_input()
        self.check_move()
        super().update()

    def check_move(self) -> None:
        """Handles movement logic, collision detection, and menu triggers."""
        
        # ESC key opens the Pause Menu
        if self.keyListener.key_pressed(pygame.K_ESCAPE):
            self.player_name, self.active_pokemon = PauseMenu(
                self.player_name, self.active_pokemon, self.screen
            ).display()
            self.keyListener.remove_key(pygame.K_ESCAPE)      

        # Only check for new movement if the previous step animation is finished
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            
            # Left Movement (Q or Left Arrow)
            if self.keyListener.key_pressed(pygame.K_q) or self.keyListener.key_pressed(pygame.K_LEFT):
                temp_hitbox.x -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_left()
                else:
                    self.direction = "left" # Turn toward wall if blocked
            
            # Right Movement (D or Right Arrow)
            elif self.keyListener.key_pressed(pygame.K_d) or self.keyListener.key_pressed(pygame.K_RIGHT):
                temp_hitbox.x += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"
            
            # Up Movement (Z or Up Arrow)
            elif self.keyListener.key_pressed(pygame.K_z) or self.keyListener.key_pressed(pygame.K_UP):
                temp_hitbox.y -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"
            
            # Down Movement (S or Down Arrow)
            elif self.keyListener.key_pressed(pygame.K_s) or self.keyListener.key_pressed(pygame.K_DOWN):
                temp_hitbox.y += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"

    def add_switchs(self, switchs: list[Switch]):
        """Populates the list of map-triggers (doors, portals)."""
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox):
        """Checks if the next step will trigger a map transition."""
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
        return None

    def add_collisions(self, collisions):
        """Populates the list of physical obstacles."""
        self.collisions = collisions

    def check_collisions(self, temp_hitbox: pygame.Rect):
        """Returns True if the proposed position overlaps with any collision rect."""
        for collision in self.collisions:
            if temp_hitbox.colliderect(collision):
                return True
        return False

    def check_input(self):
        """Handles non-directional key inputs (Action buttons)."""
        if self.keyListener.key_pressed(pygame.K_b):
            self.switch_bike()

    def switch_bike(self, deactive=False):
        """Toggles between walking (1) and biking (2) speeds and updates sprites."""
        if self.speed == 1 and not deactive:
            self.speed = 2
            self.all_images = self.get_all_images(self.spritesheet_bike)
        else:
            self.speed = 1
            self.all_images = self.get_all_images(self.spritesheet)
        self.keyListener.remove_key(pygame.K_b)

    def start_battle(self, battle_zones):
        """Checks if the player is currently inside a tall grass / wild encounter zone."""
        for battle_zone in battle_zones:
            if self.rect.colliderect(battle_zone):
                print("Wild Pokémon encounter!")
                battle_screen = BattleScreen(self.screen, self)
                battle_screen.run()
                break

    def battle(self):
        """Force-starts a combat sequence (e.g., for scripted trainer fights)."""
        print("Scripted battle sequence initiated.")
        battle_screen = InFight(self.screen, self.player_name).display()
        self.in_battle = False