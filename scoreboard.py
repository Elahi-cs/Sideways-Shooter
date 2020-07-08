import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ss_game):
        """Initialize scoreboard."""
        self.ss_game = ss_game
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ss_game.settings
        self.stats = ss_game.stats

        # Font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 42)

        # Prepare initial score, high score, number of lives and alien indicator
        self.prep_score()
        self.prep_high_score()
        self.prep_aliens_tokill()
        self.prep_ships()

    def prep_score(self):
        """Render the scoreboard."""
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.screen)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        self.rounded_hisc = round(self.stats.high_score, -1)
        self.hisc_str = f'{self.rounded_hisc:,}'
        self.hisc_image = self.font.render(self.hisc_str, True,
            self.text_color, self.screen)

        # Display the high score at the top of the screen
        self.hisc_rect = self.hisc_image.get_rect()
        self.hisc_rect.right = self.score_rect.right
        self.hisc_rect.top = self.score_rect.bottom + 10

    def prep_aliens_tokill(self):
        """Turn the number of aliens left to kill into a rendered image."""
        self.aliens_tokill = (self.settings.aliens_tokill - 
            self.ss_game.aliens_killed + 1)
        self.tokill_str = f'Aliens until speedup: {self.aliens_tokill}'
        self.tokill_image = self.font.render(self.tokill_str, True,
            self.text_color, self.screen)

        # Display how many aliens are left at the top of the screen
        self.tokill_rect = self.tokill_image.get_rect()
        self.tokill_rect.centerx = self.screen_rect.centerx
        self.tokill_rect.top = self.screen_rect.top

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ss_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        with open("highscore.txt", 'r+') as hisc:
            hi = hisc.read()
            self.stats.high_score = int(hi)
            if not hi:
                hi = '0'
            if self.stats.score > int(hi):
                hisc.seek(0)
                hisc.write(str(self.stats.score))
                hisc.truncate()

        self.prep_high_score()

    def show_score(self):
        """Draw scores, aliens left till speedup, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hisc_image, self.hisc_rect)
        self.screen.blit(self.tokill_image, self.tokill_rect)
        self.ships.draw(self.screen)

