class GameStats:
    """Collects statistics about the game."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        """Initialize what happens when ships run out."""
        self.ships_left = self.settings.ship_limit

