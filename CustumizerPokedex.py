import pygame
from pokedex import *

class CustumizerPokedex :
    def __init__(self,pokedex):
        self.pokedex=pokedex

    def dessiner (self,pokedex):
        

    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)
        return self.survole
    
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)    