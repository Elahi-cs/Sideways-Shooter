# 13-6. Game Over: Keep track of the number of times the ship is hit and 
#   the number of times an alien is hit by the ship. Decide on an appropriate 
#   condition for ending the game, and stop the game when this situation occurs

import sys
from time import sleep

import pygame
import random

from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class SidewaysShooter:
    """Overall class to manage assets and behavior."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))

        pygame.display.set_caption("Sideways Shooter")

        #Create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

    def run_game(self):
        """The main loop of the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()

    def _check_events(self):
        """Exits the game and checks for keys pressed and unpressed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Checks key pressed and maps keys to controls."""
        if event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Checks keys unpressed."""
        if event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _create_alien(self):
        """Creates the first alien and places it outside the screen."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = self.settings.screen_width
        alien.rect.x = alien.x
        alien.y = random.randint(
            1, (self.settings.screen_height - alien_height))
        self.aliens.add(alien)

    def _create_aliens(self):
        """Creates a fleet of aliens."""
        alien = Alien(self)
        alien.width, alien.height = alien.rect.size
        number_aliens_y = random.randint(1, 3)

        for alien_number in range(number_aliens_y):
            self._create_alien()

    def _fire_bullet(self):
        """Checks if bullet can be fired and fires it."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        """Respond to alien-bullet collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        # Creates a new fleet if there are no aliens left
        if not self.aliens:
            self._create_aliens()

    def _ship_hit(self):
        """Respond to the ship colliding with an alien."""
        # Subtracts a life if there are lives left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # Cleans the sprits on screen
            self.bullets.empty()
            self.aliens.empty()

            # Creates a new fleet
            self._create_aliens()

            # Centers the ship on screen again
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_left_screen(self):
        """Checks if any aliens have reached the left of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <= screen_rect.left:
                # Treats this as if the ship got hit
                self._ship_hit()

    def _update_aliens(self):
        """Updates position of alien fleet."""
        self.aliens.update()

        # Checks for ship-alien collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Checks for aliens leaving the screen
        self._check_aliens_left_screen()

        # Deletes aliens once they have left the screen
        # for alien in self.aliens.copy():
        #     if alien.x <= 0:
        #         self.aliens.remove(alien)

    def _update_screen(self):
        """Update images on the screen, and flip the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Draw the ship to screen
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    ss = SidewaysShooter()
    ss.run_game()

# Tech debt:
# 4. Experiment with controls using forward and backward thrusts
#   and side keys to rotate ship.
# 5. Then, find out how to make the bullets always move from ship to wherever
#   the ship is looking.