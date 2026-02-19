import pygame
import pytmx
import pyscroll
from front_end.screen import Screen
from .switch import Switch
from front_end.gameplay.in_fight import InFight
from front_end.sounds import Sounds

sounds = Sounds()

class Map:
    def __init__(self, screen: Screen):
        """
        Manages map loading, camera scrolling, and world objects like 
        collisions, switches, and battle zones.
        """
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player = None
        self.switchs = None
        self.collisions = None
        self.battlepokemon = None
        self.in_battle = False  # Track if a battle is currently active
        
        # Initialize with a default starting map
        self.current_map: Switch = Switch("switch", "map_0", pygame.Rect(0, 0, 0, 0), 0)
        self.switch_map(self.current_map)
        self.map_world = "map_0"

    def switch_map(self, switch: Switch):
        """
        Loads a new TMX file, sets up the scrolling renderer, 
        and parses map objects (collisions, switches, grass).
        """
        # Load Tiled map data
        self.tmx_data = pytmx.load_pygame(f"./assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        
        # Setup scrolling layer
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        # Dynamic zoom: closer zoom for interiors, wider for the world map
        if switch.name.split("_")[0] == "map":
            self.map_layer.zoom = 3
        else:
            self.map_layer.zoom = 3.75

        self.switchs = []
        self.collisions = []
        self.battlepokemon = []
        
        # Parse objects defined in Tiled
        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collisionpokemon":
                # Tall grass / Wild encounter zones
                self.battlepokemon.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name and obj.name.startswith("switch"):
                # Portals/Doors: "switch map_name port_id"
                obj_type = obj.name.split(" ")[0]
                self.switchs.append(Switch(
                    obj_type,
                    obj.name.split(" ")[1],
                    pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                    int(obj.name.split(" ")[-1])
                ))

        # Re-inject the player into the new map environment
        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collisions(self.collisions)
            self.player.start_battle(self.battlepokemon)
            self.group.add(self.player)

        self.current_map = switch

        # --- Music Management ---
        sounds.stop_map_music()

        # Play specific tracks based on map naming conventions
        if switch.name.startswith("house_"):
            sounds.play_maison_music()
        elif switch.name.startswith("pokeshop"):
            sounds.play_pokeshop_music()
        elif switch.name.startswith("pokecenter"):
            sounds.play_pokecenter_music()
        elif switch.name.startswith("labo_") or switch.name.startswith("inter_"):
            sounds.play_labo_music()
        else:
            sounds.play_map_music()  # Default world music

    def add_player(self, player) -> None:
        """Connects the player entity to the map system."""
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.collisions)
        self.player.start_battle(self.battlepokemon)

    def update(self) -> None:
        """Main update loop handling map transitions and battle triggers."""
        if self.player:
            # Handle map switching when player hits a switch/door
            if self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None 

            this_battle_zone = (0,0,0,0)
            
            # Battle Detection Logic
            for battle_zone in self.battlepokemon:
                # Entering a battle zone
                if self.player.rect.colliderect(battle_zone) and not self.in_battle:
                    sounds.stop_map_music()
                    sounds.play_combat_music()
                    self.in_battle = True
                    # is_fleeing determines if the battle ended by running away
                    self.player.is_fleeing = self.start_battle()
                    this_battle_zone = battle_zone
                    
                    if not self.player.is_fleeing:
                        self.player.keyListener.keys = [] # Reset keys if battle was fought
               
                # Staying in a battle zone
                if self.player.rect.colliderect(battle_zone) and self.in_battle:
                    this_battle_zone = battle_zone
            
            # Leaving the battle zone resets the battle flag and restores map music
            if not self.player.rect.colliderect(this_battle_zone) and self.in_battle:
                self.in_battle = False
                sounds.play_map_music()

        # Update sprite positions and center camera on player
        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

    def start_battle(self):
        """Launches the InFight UI and cleans up player state upon return."""
        battle_screen = InFight(self.screen, self.player, self.player.active_pokemon).display()
        self.player.keyListener.clear() # Prevent movement input from carrying over
        self.player.flee_steps = 0
        return battle_screen
 
    def pose_player(self, switch: Switch):
        """Teleports the player to the corresponding spawn point on the new map."""
        # Finds object named "spawn [current_map_name] [port_id]" in the TMX file
        position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)