import datetime
import traceback

from lib.game import Game
from lib.base.caught_fatal_exception import CaughtFatalException

if __name__ == "__main__":
    #! Decide how the window should be when the game opens. (fullscreen/borderless/windowed)?
    # How big should it be? User's monitor dimensions? Something else?
    try:
        game = Game((1280, 720))
    except Exception:
        with open("log.txt", "a") as error_log:
            error_log.write("%s - UNCAUGHT FATAL EXCEPTION (INITIALISATION)\n" % datetime.datetime.utcnow())
            error_log.write(traceback.format_exc() + "\n")
    else:
        try:
            game.run()
        except CaughtFatalException:
            pass
        except Exception:   # Catches all exceptions that weren't caught in the rest of the code
            game.log("UNCAUGHT FATAL EXCEPTION")
