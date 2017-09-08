from lib import base
#!!! TEST - REMOVE
from debug_console import DebugConsole
#!!! TEST - REMOVE


class Game(base.Game):
    def __init__(self, resolution, mode="windowed"):
        super(Game, self).__init__(resolution, mode)

        #!!! TEST - REMOVE
        self.debug_console = DebugConsole(self)
        #!!! TEST - REMOVE

        self.options = {
            #! Add a function to make this load the player's settings from a file of
            # some sort. YAML if you don't care about hiding settings from users.
            # Inventory
            "show item info at side": False
        }

    def logic(self):
        self.check_quit()
        self.console.logic()
        #!!! TEST - REMOVE
        self.debug_console.logic()
        #!!! TEST - REMOVE

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.console.draw()
        #!!! TEST - REMOVE
        self.debug_console.draw()
        #!!! TEST - REMOVE

    def quit(self):
        #! Add code for autosaving the game here
        pygame.quit()
