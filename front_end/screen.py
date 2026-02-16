import pygame
import cv2
import numpy as np

class Screen:
    def __init__(self, width=1200, height=720):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokémon")
        self.clock = pygame.time.Clock()
        self.framerate = 144
        self.deltatime = 0 # refresh screen window
        self.caption = pygame.display.set_caption("Pokémon")
        self.screen = pygame.display.set_icon(pygame.image.load("./assets/logo/pokeball.jpg"))
        
        # Variables pour la vidéo background
        self.video_capture = None
        self.is_video_background = False
        self.current_video_frame = None

    def update(self):
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.framerate) #r refresh screen
        self.display.fill((0, 0, 0)) # erase screen content
        self.deltatime = self.clock.get_time()

    def get_deltatime(self):
        return self.deltatime

    def get_size(self):
        return self.display.get_size()

    def get_display(self):
        return self.display
    
    def set_background_display(self, background_path):
        # Corriger le chemin si nécessaire
        if background_path.startswith('/'):
            background_path = background_path[1:]
        
        # Vérifier si c'est une vidéo
        if background_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # C'est une vidéo
            self.is_video_background = True
            
            # Libérer l'ancienne vidéo si elle existe
            if self.video_capture:
                self.video_capture.release()
            
            self.video_capture = cv2.VideoCapture(background_path)
            if not self.video_capture.isOpened():
                raise FileNotFoundError(f"Impossible de charger la vidéo '{background_path}'")
            print(f"✓ Vidéo background chargée : {background_path}")
            
            # Afficher la première frame
            self._update_video_frame()
            self._draw_video_background()
        else:
            # C'est une image (comportement original)
            self.is_video_background = False
            background = pygame.transform.scale(pygame.image.load(background_path), (self.width, self.height))
            background_rect = background.get_rect()
            self.display.blit(background, background_rect)

        # Ajouter l'overlay noir transparent
        background_screen = pygame.Surface((self.width, self.height))
        background_rect = background_screen.get_rect(center = (self.width //2, self.height // 2))
        background_screen.set_alpha(155)
        pygame.draw.rect(background_screen, "black", background_rect)
        self.display.blit(background_screen, background_rect)

    def _update_video_frame(self):
        """Met à jour la frame vidéo courante"""
        if self.video_capture and self.is_video_background:
            ret, frame = self.video_capture.read()
            
            if not ret:
                # Recommencer la vidéo depuis le début (loop)
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video_capture.read()
            
            if ret:
                # Convertir la frame OpenCV (BGR) en format Pygame (RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                # Transposer pour Pygame
                frame = np.rot90(frame)
                frame = np.flipud(frame)
                self.current_video_frame = pygame.surfarray.make_surface(frame)

    def _draw_video_background(self):
        """Dessine la frame vidéo courante"""
        if self.current_video_frame:
            self.display.blit(self.current_video_frame, (0, 0))

    def update_video_background(self):
        """À appeler dans la boucle principale pour mettre à jour la vidéo"""
        if self.is_video_background:
            self._update_video_frame()
            self._draw_video_background()
            
            # Ajouter l'overlay noir transparent
            background_screen = pygame.Surface((self.width, self.height))
            background_rect = background_screen.get_rect(center = (self.width //2, self.height // 2))
            background_screen.set_alpha(155)
            pygame.draw.rect(background_screen, "black", background_rect)
            self.display.blit(background_screen, background_rect)

    def set_background_without_black(self, background_path):
        # Corriger le chemin si nécessaire
        if background_path.startswith('/'):
            background_path = background_path[1:]
            
        # Vérifier si c'est une vidéo
        if background_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # C'est une vidéo (sans overlay noir)
            self.is_video_background = True
            
            # Libérer l'ancienne vidéo si elle existe
            if self.video_capture:
                self.video_capture.release()
            
            self.video_capture = cv2.VideoCapture(background_path)
            if not self.video_capture.isOpened():
                raise FileNotFoundError(f"Impossible de charger la vidéo '{background_path}'")
            print(f"✓ Vidéo background chargée : {background_path}")
            
            # Afficher la première frame
            self._update_video_frame()
            self._draw_video_background()
        else:
            # C'est une image (comportement original)
            self.is_video_background = False
            background = pygame.transform.smoothscale(pygame.image.load(background_path), (self.width, self.height))
            background_rect = background.get_rect()
            self.display.blit(background, background_rect)

    def cleanup(self):
        """Libère les ressources vidéo"""
        if self.video_capture:
            self.video_capture.release()