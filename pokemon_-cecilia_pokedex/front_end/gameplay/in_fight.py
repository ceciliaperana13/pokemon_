import pygame, sys, math, time
from __settings__ import BATTLE_BACKGROUND, BATTLE_FLOOR, REGULAR_FONT, DARK_GREEN, LIGHT_GREEN
from front_end.menu.util_tool import UtilTool
from front_end.menu.bagmenu import BagMenu
from front_end.menu.attack_type_menu import AttackMenu
from front_end.menu.infomenu import InfoMenu
from front_end.menu.change_pokemon_infight import ChangePokemonInFight
from front_end.gameplay.healthdisplay import HealthDisplay
from back_end.models.fight import Fight
from back_end.controller import save_pokemon_to_pokedex, get_random_wild_pokemon,\
    get_bag_from_pokedex, save_bag_to_pokedex, save_wild_pokemon

class InFight():
    def __init__(self, screen, player, pokemon):
        """
        Initializes the battle scene, loads the enemy, and sets up the combat state.
        """
        self.screen = screen
        self.pokemon_enemy = get_random_wild_pokemon()

        self.background = BATTLE_BACKGROUND
      
        self.font = pygame.font.Font(None, 50)  
        self.options = ["Attack", "Bag", "Team", "Info", "Flee"]  
        self.bag_option = ["Potions", "Pokeball", "Back"]
        self.selected_index = 0  
        self.running = True  
        self.player = player.player_name
        self.pokemon = pokemon     
        self.bag = get_bag_from_pokedex(self.player)
        self.fight = Fight(self.pokemon, self.pokemon_enemy)
        self.util = UtilTool()
        self.fleeing = False
        self.healthbar = HealthDisplay()

    def display(self):
        """
        Main battle loop. Manages rendering, turn transitions, and menu navigation.
        """
        # Load environment assets
        battle_floor = self.util.load_image(BATTLE_FLOOR)
        battle_floor2 = pygame.transform.flip(battle_floor, True, False)
        pokemon_enemy_img = self.util.load_image(self.pokemon_enemy.image)
        
        # Animation and battle state variables
        time_count = 0
        var_x, var_y = 5, 5
        speed = 1.5
        win = False
        message_damage = None
        message_attack = None
        another_option = ""
        level = self.pokemon.get_level()
        name = self.pokemon.name
        winner = ""
        pokemon_hp_max = self.pokemon.get_hp_max()
        pokemon_enemy_hp_max = self.pokemon_enemy.get_hp_max()
      
        # UI Positioning
        my_pokemon_x = int(self.screen.width // 10 * 0.5)
        my_pokemon_y = int(self.screen.height // 10 )
        pokemon_enemy_x = int(self.screen.width // 10 * 7.5 )               
        pokemon_enemy_y = int(self.screen.height // 10)

        # Determine who starts based on speed stats
        player_turn = self.fight.is_player_first()

        while self.running: 
            # Load the player's Pokemon back-view sprite
            pokemon_back_img = self.util.load_image(self.pokemon.get_back_image())
            
            # --- RENDERING ---
            self.screen.update()
            
            # Idle floating animation logic
            if not win:
                time_count += speed
                x_movement = int(var_y * math.sin(time_count * 0.1))
                y_movement = int(var_x * math.sin(time_count * 0.08))
            else:
                x_movement, y_movement = 0, 0

            # Draw backgrounds and battle platforms
            self.util.display_assets_and_background_in_fight(
                self.screen, x_movement, y_movement, battle_floor, battle_floor2, pokemon_enemy_img, pokemon_back_img
            )
          
            # Draw Health Bars
            self.healthbar.draw_health_bar(my_pokemon_x, my_pokemon_y, self.pokemon, pokemon_hp_max,
                                           self.screen, (self.screen.width // 16 * 2.5, self.screen.height // 20 * 2))

            self.healthbar.draw_health_bar(pokemon_enemy_x, pokemon_enemy_y,
                                            self.pokemon_enemy, pokemon_enemy_hp_max,
                                            self.screen,
                                            (self.screen.width // 16 * 13.5, self.screen.height // 20 * 2), "enemy")
            
            self.util.draw_option_screen(self.screen)

            # Draw Action Menu
            for i, option in enumerate(self.options):
                color = LIGHT_GREEN if i == self.selected_index else DARK_GREEN
                self.util.draw_text(option, REGULAR_FONT, self.screen.width // 30, self.screen,
                                    (self.screen.width // 2 + i * 120, self.screen.height // 8 * 7), color)

            # --- POST-BATTLE SCREENS ---
            if win:
                self.options[-1] = "Exit"
                self.fleeing = False
                if winner == "enemy":
                    self.util.draw_win_bot_screen(self.screen)
                elif another_option == "Success":
                    self.util.draw_win_capture_screen(self.pokemon_enemy, self.pokemon, level, name, self.screen)
                else:
                    self.util.draw_win_player_screen(self.pokemon, self.pokemon_enemy, level, name, self.screen)

            # Display attack feedback messages (Damage/Effectiveness)
            if message_attack and message_damage and not win:
                now_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - now_time < 1000:
                    self.util.draw_info_attack_screen(self.screen, message_attack, message_damage)
                    pygame.display.update()
                message_attack, message_damage = None, None
                
            pygame.display.flip()

            # --- INPUT HANDLING ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if player_turn:
                    if event.type == pygame.KEYDOWN:
                        # Menu Navigation
                        if event.key in [pygame.K_RIGHT, pygame.K_DOWN]:
                            self.selected_index = (self.selected_index + 1) % len(self.options)
                        elif event.key in [pygame.K_LEFT, pygame.K_UP]:
                            self.selected_index = (self.selected_index - 1) % len(self.options)
                        
                        # Option Selection
                        elif event.key == pygame.K_RETURN:
                            match self.selected_index:
                                case 0: # ATTACK
                                    if win: self.selected_index = 4
                                    elif self.pokemon.get_hp() > 0:
                                        attack_type = AttackMenu(self.screen, self.pokemon, self.pokemon_enemy).display()
                                        if attack_type != "Back":
                                            self.fight.player_attack(attack_type)
                                            if self.pokemon_enemy.get_hp() > 0:
                                                message_attack = self.fight.fightinfo.set_who_attack_message(self.pokemon)
                                                message_damage = self.fight.fightinfo.get_damage_message()
                                                player_turn = False # Pass turn to enemy
                                            else:
                                                # Enemy fainted
                                                self.pokemon.update_xp(self.pokemon_enemy)
                                                winner, win = "player", True
                                                player_turn = True
                                
                                case 1: # BAG (Items)
                                    if win: self.selected_index = 4
                                    else:
                                        bag_choice = BagMenu(self.screen, self.pokemon, self.pokemon_enemy, self.bag).display()
                                        if bag_choice == "Potions":
                                            if not self.fight.use_potion(self.pokemon, self.bag):
                                                player_turn = False # Potion used, end turn
                                        elif bag_choice == "Pokeball":
                                            another_option = self.fight.use_pokeball(self.player, self.bag, self.pokemon, self.pokemon_enemy)
                                            if another_option == "Success":
                                                self.capture_message("Captured successfully!")
                                                winner, win = "player", True
                                            elif another_option == "Fail":
                                                self.capture_message(f"{self.pokemon_enemy.name} broke free!")
                                                player_turn = False
                                
                                case 2: # TEAM (Switch Pokemon)
                                    if not win:
                                        self.pokemon = ChangePokemonInFight(self.player, self.pokemon, self.pokemon_enemy, self.screen).display()
                                        self.fight.set_first_pokemon(self.pokemon)
                                        pokemon_hp_max = self.pokemon.get_hp_max()
                                        name, level = self.pokemon.name, self.pokemon.get_level()

                                case 3: # INFO (Inspect stats)
                                    InfoMenu(self.screen, self.pokemon, self.pokemon_enemy).display()
                                
                                case 4: # FLEE or EXIT
                                    if win:
                                        # Handle post-capture naming and saving
                                        if another_option == "Success":
                                            if len(self.pokemon_enemy.pet_name.split()) == 1:
                                                new_name = f"{self.pokemon_enemy.pet_name} {time.time()}"
                                                self.pokemon_enemy.set_pet_name(new_name)
                                            self.save_all_to_pokedex()
                                        else:
                                            self.save()
                                        return self.fleeing
                                    else:
                                        # Attempt to escape from wild battle
                                        self.fleeing = self.fight.run_away()
                                        if self.fleeing:
                                            self.save()
                                            self.message_pop_up(self.fight.fightinfo.flee_message)
                                            return True
                                        else:
                                            self.message_pop_up("Failed to escape!")
                                            player_turn = False

                # --- ENEMY TURN LOGIC ---
                elif not player_turn and not win:
                    pygame.time.wait(800) # Small delay for realism
                    if self.pokemon.get_hp() > 0:
                        self.fight.bot_attack()
                        message_attack = self.fight.fightinfo.set_who_attack_message(self.pokemon_enemy)
                        message_damage = self.fight.fightinfo.get_damage_message()
                        
                        if self.pokemon.get_hp() <= 0:
                            winner, win = "enemy", True
                    else:
                        winner, win = "enemy", True
                    player_turn = True

    def capture_message(self, message):
        """Displays a full-screen notification for capture events."""
        now_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - now_time < 1000:
            self.util.draw_info_capture_screen(self.screen, message)
            pygame.display.update()

    def message_pop_up(self, message):
        """Displays a temporary pop-up message (e.g., Flee attempts)."""
        now_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - now_time < 1000:
            self.util.draw_info_capture_screen(self.screen, message)
            pygame.display.update()

    def reset_hp(self):
        """Heals both participants (usually called before saving or leaving)."""
        self.pokemon.set_hp(self.pokemon.get_hp_max())
        self.pokemon_enemy.set_hp(self.pokemon_enemy.get_hp_max())

    def save_all_to_pokedex(self):
        """Saves player stats, bag, and the newly captured enemy."""
        self.reset_hp()
        save_pokemon_to_pokedex(self.player, self.pokemon)
        save_bag_to_pokedex(self.player, self.bag)
        save_pokemon_to_pokedex(self.player, self.pokemon_enemy)
    
    def save(self):
        """Standard save for player state and enemy discovery."""
        self.reset_hp()
        save_pokemon_to_pokedex(self.player, self.pokemon)
        save_bag_to_pokedex(self.player, self.bag)
        save_wild_pokemon(self.pokemon_enemy)