class Settings:
    """Sets the tings."""

    def __init__(self):
        """Initialize the setting of tings."""
        # Screen size
        self.screen_width = 1200
        self.screen_height = 800
        # Draws the screen
        self.bg_color = (200, 200, 200)

        # Ship settings
        self.ship_limit = 2

        # Bullet settings
        self.bullet_color = (0, 0, 0)

        # Level scaling settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.2

        self.bullet_speed = 2.0
        self.bullets_allowed = 3

        self.alien_speed = 0.7
        # Number of aliens you need to kill for the game to speed up.
        self.aliens_tokill = 5

        self.alien_points = 50

    def speed_up(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # Increase the number of aliens needed till next speedup by 5 and
        # multiply by speedup scale
        self.aliens_tokill = int(self.aliens_tokill + 5 * self.speedup_scale)

        self.bullets_allowed += 1

        self.alien_points = int(self.alien_points * self.score_scale)



