import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    """Class and assets for the alien enemies."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (103, 69))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Get exact values for vertical and horizontal positions
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        self.drop_speed = random.uniform(0.5, 1.0)
        # Update the decimal position of the alien
        self.x -= self.drop_speed
        # Update the rect position
        self.rect.x = self.x
        self.rect.y = self.y





