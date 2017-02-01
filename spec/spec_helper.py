from expects import *

from lib.game import Game
from lib.caught_fatal_exception import CaughtFatalException

import sys
import datetime
import traceback


class TestGame(Game):
    """An altered Game class for testing purposes."""
    def __init__(self, resolution):
        super(TestGame, self).__init__(resolution)

    def log(self, *error_message, **options):
        """Altered log function which doesn't create an error popup and raises non-fatal exceptions."""
        fatal = options.get("fatal", True)  # `fatal` option defaults to True
        error_message = "".join(map(str, error_message))
        try:
            with open(self.path_to("log.txt"), "a") as error_log:
                error_log.write("%s - %s" % (datetime.datetime.utcnow(), error_message))
                error_log.write(traceback.format_exc() + "\n")
        except Exception:
            error_info = "This error occurred very early during game initialisation and could not be logged"
        else:
            error_info = "Please check log.txt for details"

        if fatal:
            text = "".join(("An error has occurred:\n\n    ",
                            error_message, ".\n\n\n",
                            error_info, "."))
            ctypes.windll.user32.MessageBoxA(0, text, "Error", 0)   # Error popup
            raise CaughtFatalException(sys.exc_info()[1])
        else:
            raise


game = TestGame((1280, 720))
