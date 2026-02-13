import pygame
import pyscroll
import pytmx

from player import Player
from screen import Screen
from switch import Switch
from battle_trigger import BattleTrigger


class Map:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None

        self.player: Player | None = None
        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.battle_triggers: list[BattleTrigger] | None = None

        self.current_map: Switch = Switch("switch", "map_0", pygame.Rect(0, 0, 0, 0), 0)
        
        # Callback pour lancer le combat
        self.battle_callback = None

        self.switch_map(self.current_map)

    def switch_map(self, switch: Switch) -> None:
        self.tmx_data = pytmx.load_pygame(f"./assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        if switch.name.split("_")[0] == "map":
            self.map_layer.zoom = 3
        else:
            self.map_layer.zoom = 3.75

        self.switchs = []
        self.collisions = []
        self.battle_triggers = []

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            
            type_name = obj.name.split(" ")[0]
            
            if type_name == "switch":
                self.switchs.append(Switch(
                    type_name, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                    int(obj.name.split(" ")[-1])
                ))
            
            # Détection des zones de combat dans TMX
            elif type_name == "battle":
                # Format: "battle tile_x tile_y"
                parts = obj.name.split(" ")
                if len(parts) >= 3:
                    tile_x = int(parts[1])
                    tile_y = int(parts[2])
                    trigger = BattleTrigger(tile_x, tile_y)
                    if self.battle_callback:
                        trigger.set_callback(self.battle_callback)
                    self.battle_triggers.append(trigger)

        # Configuration manuelle pour la tuile (20, 12) si pas dans TMX
        if switch.name == "map_0":  # Changez selon votre carte
            trigger = BattleTrigger(20, 12)
            if self.battle_callback:
                trigger.set_callback(self.battle_callback)
            self.battle_triggers.append(trigger)

        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collisions(self.collisions)
            self.group.add(self.player)
            if switch.name.split("_")[0] != "map":
                self.player.switch_bike(True)

        self.current_map = switch

    def add_player(self, player) -> None:
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.collisions)

    def set_battle_callback(self, callback):
        """
        Définit la fonction à appeler pour lancer un combat.
        
        Args:
            callback: Fonction qui lance l'interface de combat
        """
        self.battle_callback = callback
        # Met à jour tous les triggers existants
        if self.battle_triggers:
            for trigger in self.battle_triggers:
                trigger.set_callback(callback)

    def check_battle_triggers(self) -> bool:
        """
        Vérifie si le joueur déclenche un combat.
        
        Returns:
            True si un combat a été déclenché, False sinon
        """
        if not self.player or not self.battle_triggers:
            return False
        
        for trigger in self.battle_triggers:
            if trigger.check_collision(self.player.hitbox):
                trigger.trigger()
                return True
        
        return False

    def update(self) -> None:
        if self.player:
            if self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None
            
            # Vérification des déclencheurs de combat
            self.check_battle_triggers()
        
        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

    def pose_player(self, switch: Switch):
        position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)
