import sys
from time import sleep

import pygame
import random

from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
import button as bt
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

        self._create_assets()

    def _create_assets(self):
        """Create instances of the game's assets."""
        # Create an instance to store game statistics
        self.stats = GameStats(self)

        self.aliens_killed = 0
        self.sb = Scoreboard(self)

        # Create the buttons and put them on a list
        self.play_button = bt.create_button(500, 300, 'Play', self._start_game)
        # Difficulty buttons have no callback as they'll be assigned later,
        # that way there doesn't have to be a function for each individual diff
        self.easy_button = bt.create_button(250, 400, 'Easy', 
            self._set_difficulty)
        self.normal_button = bt.create_button(500, 400, 'Normal', 
            self._set_difficulty)
        self.hard_button = bt.create_button(750, 400, 'Hard', 
            self._set_difficulty)

        self.button_list = [self.play_button, self.easy_button, 
            self.normal_button, self.hard_button]

        # Create ship and sprite assets.
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
                self.sb.check_high_score()
            self._update_screen()

    def _start_game(self):
        """Reset everything and start a new game."""
        # Reset the game statistics.
        self.settings.initialize_dynamic_settings()
        self.sb.prep_score()
        self.sb.prep_aliens_tokill()

        self.stats.reset_stats()
        self.stats.game_active = True

        self._reset_game()

    def _reset_game(self):
        """Empty the screen of assets and place them again."""
        # Render the number of ships left
        self.sb.prep_ships()

        # Clean the sprites on screen
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet
        self._create_aliens()

        # Center the ship on screen again
        self.ship.center_ship()

    def _check_events(self):
        """Exit the game and checks for keys pressed and unpressed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEMOTION:
                self._check_mouse_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_clicks(event.pos)

    def _check_keydown_events(self, event):
        """Check key pressed and maps keys to controls."""
        if event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Check keys unpressed."""
        if event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _check_mouse_clicks(self, mouse_pos):
        """Check mouse clicks."""
        for button in self.button_list:
            if button['rect'].collidepoint(mouse_pos):
                button['color'] = bt.clicked_color

        if self.play_button['rect'].collidepoint(mouse_pos):
            self.play_button['callback']()

        if self.easy_button['rect'].collidepoint(mouse_pos):
            self.easy_button['callback']('easy')
        elif self.normal_button['rect'].collidepoint(mouse_pos):
            self.normal_button['callback']('normal')
        elif self.hard_button['rect'].collidepoint(mouse_pos):
            self.hard_button['callback']('hard')

    def _set_difficulty(self, diff):
        """Sets desired difficulty."""
        if diff == 'easy':
            self.settings.speedup_scale = 1.05
            self.settings.score_scale = 1.25
        elif diff == 'normal':
            self.settings.speedup_scale = 1.1
            self.settings.score_scale = 1.5
        elif diff == 'hard':
            self.settings.speedup_scale = 1.2
            self.settings.score_scale = 1.75

    def _check_mouse_hover(self, mouse_pos):
        """
        Check if the mouse hovers over the buttons and change the color if so.
        """
        for button in self.button_list:
            if button['rect'].collidepoint(mouse_pos):
                button['color'] = bt.active_color
            else:
                button['color'] = bt.inactive_color

    def _create_alien(self):
        """Create the first alien and place it outside the screen."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = self.settings.screen_width
        alien.rect.x = alien.x
        # Spawn in random locations across the y axis, with a minimum of its own
        #height on top of screen and a limit of screen bottom
        alien.y = random.randint(
            alien_height, (self.settings.screen_height - alien_height))
        self.aliens.add(alien)

    def _create_aliens(self):
        """Create a fleet of aliens."""
        alien = Alien(self)
        alien.width, alien.height = alien.rect.size
        number_aliens_y = random.randint(1, 3)

        for alien_number in range(number_aliens_y):
            self._create_alien()

    def _fire_bullet(self):
        """Check if bullet can be fired and fire it."""
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

        # Speed up the game when threshold is reached
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.aliens_tokill -= 1 * len(aliens)
                self.aliens_killed += 1 * len(aliens)
            self.sb.prep_aliens_tokill()
            self.sb.prep_score()

            self._check_speed_up()

        # Creates a new fleet if there are no aliens left
        if not self.aliens:
            self._create_aliens()

    def _check_speed_up(self):
        """Checks if enough aliens have been killed to speed up the game."""
        if self.aliens_killed > self.settings.aliens_tokill:
            self.aliens_killed = 0
            self.settings.speed_up()
            print("Speeding up")

    def _ship_hit(self):
        """Respond to the ship colliding with an alien."""
        # Subtracts a life if there are lives left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            
            self._reset_game()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_left_screen(self):
        """
        Check if any aliens have reached the left of the screen, and subtract
        points if so. If points reach less than 0, act as if ship was hit.
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.right <= screen_rect.left:
            # Delete aliens once they have left the screen
                self.aliens.remove(alien)
                print(self.aliens)
                if self.stats.score >= 0:
                    self.stats.score -= self.settings.alien_points * 2
                else:
                    self._ship_hit()
                    self.stats.score = 0
        self.sb.prep_score()

    def _update_aliens(self):
        """Update position of alien fleet."""
        self.aliens.update()

        # Check for ship-alien collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens leaving the screen
        self._check_aliens_left_screen()

    def _update_screen(self):
        """Update images on the screen, and flip the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Draw the ship to screen
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the scoreboard to the screen
        self.sb.show_score()

        # Draw the buttons to the screen if the game isn't active
        if not self.stats.game_active:
            for button in self.button_list:
                bt.draw_button(button, self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    ss = SidewaysShooter()
    ss.run_game()

# Tech debt:
# 4. Experiment with controls using forward and backward thrusts
#   and side keys to rotate ship.
# 5. Then, make the bullets always move from ship to wherever
#   the ship is looking.