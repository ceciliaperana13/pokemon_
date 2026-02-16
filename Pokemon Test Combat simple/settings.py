import pygame
import cv2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
POKE_BLUE = (53, 126, 199)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
WIDTH, HEIGHT = 800, 600

background = "asset/wallpaper/wallpaper.mp4"


class VideoBackground:
    def __init__(self, path, width, height):
        self.cap = cv2.VideoCapture(path)
        self.width = width
        self.height = height

    def get_next_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            # Si la vidéo est finie, on revient au début (loop)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        if ret:
            # OpenCV utilise le format BGR, on doit le convertir en RGB pour Pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Redimensionner l'image à la taille de l'écran
            frame = cv2.resize(frame, (self.width, self.height))
            # Transposer pour correspondre à l'orientation de Pygame
            frame = frame.swapaxes(0, 1)
            return pygame.surfarray.make_surface(frame)
        return None

    def release(self): # Fermer la vidéo
        self.cap.release()

        