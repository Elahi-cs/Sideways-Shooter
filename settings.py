import random

class Settings:
    """Sets the tings."""

    def __init__(self):
        """Initialize the setting of tings."""
        # Screen size
        self.screen_width = 1200
        self.screen_height = 800
        # Draws the screen (check out how it can be done with an image)
        self.bg_color = (200, 200, 200)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 7

        # Alien settings in Alien class
        
