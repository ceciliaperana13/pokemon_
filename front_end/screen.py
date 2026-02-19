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
        self.deltatime = 0 # Time since last frame
        self.caption = pygame.display.set_caption("Pokémon")
        self.screen = pygame.display.set_icon(pygame.image.load("./assets/logo/pokeball.jpg"))
        
        # Background video variables
        self.video_capture = None
        self.is_video_background = False
        self.current_video_frame = None

    def update(self):
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.framerate) # Update screen frame rate
        self.display.fill((0, 0, 0)) # Clear screen content
        self.deltatime = self.clock.get_time()

    def get_deltatime(self):
        return self.deltatime

    def get_size(self):
        return self.display.get_size()

    def get_display(self):
        return self.display
    
    def set_background_display(self, background_path):
        # Correct the path if necessary
        if background_path.startswith('/'):
            background_path = background_path[1:]
        
        # Check if the file is a video
        if background_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # It's a video
            self.is_video_background = True
            
            # Release old video if it exists
            if self.video_capture:
                self.video_capture.release()
            
            self.video_capture = cv2.VideoCapture(background_path)
            if not self.video_capture.isOpened():
                raise FileNotFoundError(f"Could not load video '{background_path}'")
            print(f"✓ Background video loaded: {background_path}")
            
            # Display the first frame
            self._update_video_frame()
            self._draw_video_background()
        else:
            # It's an image (original behavior)
            self.is_video_background = False
            background = pygame.transform.scale(pygame.image.load(background_path), (self.width, self.height))
            background_rect = background.get_rect()
            self.display.blit(background, background_rect)

        # Add a transparent black overlay
        background_screen = pygame.Surface((self.width, self.height))
        background_rect = background_screen.get_rect(center = (self.width //2, self.height // 2))
        background_screen.set_alpha(155)
        pygame.draw.rect(background_screen, "black", background_rect)
        self.display.blit(background_screen, background_rect)

    def _update_video_frame(self):
        """Updates the current video frame"""
        if self.video_capture and self.is_video_background:
            ret, frame = self.video_capture.read()
            
            if not ret:
                # Restart video from the beginning (loop)
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video_capture.read()
            
            if ret:
                # Convert OpenCV frame (BGR) to Pygame format (RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                # Transpose for Pygame
                frame = np.rot90(frame)
                frame = np.flipud(frame)
                self.current_video_frame = pygame.surfarray.make_surface(frame)

    def _draw_video_background(self):
        """Draws the current video frame"""
        if self.current_video_frame:
            self.display.blit(self.current_video_frame, (0, 0))

    def update_video_background(self):
        """Should be called in the main loop to update the video playback"""
        if self.is_video_background:
            self._update_video_frame()
            self._draw_video_background()
            
            # Add a transparent black overlay
            background_screen = pygame.Surface((self.width, self.height))
            background_rect = background_screen.get_rect(center = (self.width //2, self.height // 2))
            background_screen.set_alpha(155)
            pygame.draw.rect(background_screen, "black", background_rect)
            self.display.blit(background_screen, background_rect)

    def set_background_without_black(self, background_path):
        # Correct the path if necessary
        if background_path.startswith('/'):
            background_path = background_path[1:]
            
        # Check if the file is a video
        if background_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # It's a video (without black overlay)
            self.is_video_background = True
            
            # Release old video if it exists
            if self.video_capture:
                self.video_capture.release()
            
            self.video_capture = cv2.VideoCapture(background_path)
            if not self.video_capture.isOpened():
                raise FileNotFoundError(f"Could not load video '{background_path}'")
            print(f"✓ Background video loaded: {background_path}")
            
            # Display the first frame
            self._update_video_frame()
            self._draw_video_background()
        else:
            # It's an image (original behavior)
            self.is_video_background = False
            background = pygame.transform.smoothscale(pygame.image.load(background_path), (self.width, self.height))
            background_rect = background.get_rect()
            self.display.blit(background, background_rect)

    def cleanup(self):
        """Releases video resources"""
        if self.video_capture:
            self.video_capture.release()