from expects import *

from lib.game import Game

import datetime


class TestGame(Game):
    """An altered Game class for testing purposes."""
    def __init__(self, resolution):
        super(TestGame, self).__init__(resolution)

    def log(self, *error_message):
        """Altered log function which doesn't show error popups."""
        try:
            error_message = "".join(map(str, error_message))
            with open(self.path_to("log.txt"), "a") as error_log:
                error_log.write("".join((
                    str(datetime.datetime.utcnow())[0:19], " - ",
                    error_message, ": ",
                    str(self.error), " (", self.error.__class__.__name__, ")\n"
                    )))
            self.error = "Details unknown"  # Resetting to default value
        except:    # Likely only when file_directory has not yet been defined
            raise
        #! Add some code here to show a message in game instead of
        # force quitting the game unless the error is sufficiently bad.
        # fatal_error (below) should depend on this code,
        # or it can be passed in to log() as a argument.
        fatal_error = True
        if fatal_error:
            raise


game = TestGame((1280, 720))
