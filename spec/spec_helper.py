from expects import *

from lib.game import Game
from lib.caught_fatal_exception import CaughtFatalException

import datetime


class TestGame(Game):
    """An altered Game class for testing purposes."""
    def __init__(self, resolution):
        super(TestGame, self).__init__(resolution)

    def log(self, *error_message):
        """Altered log function which just raises errors."""
        raise CaughtFatalException


game = TestGame((1280, 720))
