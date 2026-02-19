import pygame, sys
from __settings__ import POKEMON_CENTER, REGULAR_FONT, POKEBALL
from .util_tool import UtilTool
from .display_pokemon_stat import PokemonStat
from back_end.controller import get_starter_pokemons, create_player

class SelectPokemon():
    def __init__(self, player_name, screen, pokemon_list=[]):
        self.player_name = player_name
        self.screen = screen
        self.background = POKEMON_CENTER
        self.image_background = pygame.transform.scale(pygame.image.load(self.background), (self.screen.width, self.screen.height))
        self.image_rect = self.image_background.get_rect(center = (self.screen.width // 2, self.screen.height //2))
        self.util = UtilTool()
        self.font = pygame.font.Font(None, 50)
        
        if not pokemon_list:
            self.pokemons = get_starter_pokemons()
        else:
            self.pokemons = pokemon_list

        self.options = []
        self.options_rect = []
        my_x = 0.5
        for pokemon in self.pokemons:
            option = self.load_image(pokemon.get_image(), (self.screen.width // 6, self.screen.width // 6))
            option_rect = option.get_rect(center = (self.screen.width // 3 * my_x, self.screen.height // 5*2.5))
            my_x += 1
            self.options.append(option)
            self.options_rect.append(option_rect)

        self.selected_index = 0
        self.running = True

    def load_image(self, path, scaling):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (scaling))
        return img

    def capturePokemon(self, pokemon, pokemon_rect, pokemons, pokemons_rect):
        """Animation for capturing the chosen starter"""
        pokeball_img = pygame.transform.scale(pygame.image.load(POKEBALL), (60,60))
        pokeball_rect = pokeball_img.get_rect(center=(self.screen.width // 2, self.screen.height - 100))
        target_pos = pokemon_rect.center
        
        speed = 15 # Internal variable updated to English
        captured = False

        while not captured:
            self.screen.display.fill((173, 216, 230))
            self.screen.display.blit(self.image_background, (0, 0))

            for index, p in enumerate(pokemons):
                self.screen.display.blit(p, pokemons_rect[index].topleft)

            if pokeball_rect.colliderect(pokemon_rect):
                captured = True
                return

            else:
                dx = target_pos[0] - pokeball_rect.centerx
                dy = target_pos[1] - pokeball_rect.centery
                dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                pokeball_rect.x += int(speed * dx / dist)
                pokeball_rect.y += int(speed * dy / dist)

            self.screen.display.blit(pokeball_img, pokeball_rect.topleft)
            pygame.display.flip()
            pygame.time.delay(30)
    
    def display(self):
        while self.running:
            self.screen.update()
            self.screen.display.blit(self.image_background, self.image_rect)
            
            for i, option in enumerate(self.options):
                font_size = self.screen.height // 15
                if i == self.selected_index:
                    option = pygame.transform.smoothscale(pygame.image.load(self.pokemons[i].get_image()), (self.screen.width // 4, self.screen.width // 4))
                    self.screen.display.blit(option, self.options_rect[i])
                    self.util.draw_text(self.pokemons[i].name, REGULAR_FONT, font_size, self.screen, (self.screen.width // 2, self.screen.height // 5*1.5), "white")
                else:
                    option = pygame.transform.smoothscale(pygame.image.load(self.pokemons[i].get_image()), (self.screen.width // 6, self.screen.width // 6))
                    self.screen.display.blit(option, self.options_rect[i])

            # Display instructions (Translated to English)
            instructions = "Arrows: Choose | ENTER: Confirm Starter"
            self.util.draw_text(instructions, REGULAR_FONT, self.screen.height // 35, self.screen, (self.screen.width // 2, self.screen.height - 50), "yellow")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.options)

                    elif event.key == pygame.K_RETURN:
                        # MODIFIED: ENTER directly starts the game
                        create_player(self.player_name, self.pokemons[self.selected_index])
                        
                        self.capturePokemon(
                            self.options[self.selected_index], 
                            self.options_rect[self.selected_index], 
                            self.options, 
                            self.options_rect
                        )
                        
                        return self.pokemons[self.selected_index]