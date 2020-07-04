import pygame

class Ship:
    """A movin' ship with all its movin' parts an' stuff."""

    def __init__(self, ai_game):
        """Initialize the ship and set where it starts."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.center_ship()

        # Store a decimal value for the ship's vertical position.
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """Puts the ship at the center of the screen."""
        self.rect.midleft = self.screen_rect.midleft

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's y value, not the rect. #it was converted to float
        if self.moving_up and self.rect.y >= self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)