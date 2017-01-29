# Built-in modules
# Base
import os
import ctypes
import datetime
import time
# Main
# import [module]

# Pygame
import pygame
try:
    import pygame._view     # sometimes necessary. If it isn't this will cause an error
    #! UPDATE: this might only be necessary for py2exe to work, so if you can
    # compile without it, then there's no need to import pygame_view whatsoever
except ImportError:
    pass

# User defined modules
# Base
from system import System
from console import Console
from userinput import Input
from hotkey import Hotkey
from text_input import TextInput
# Main
from helper import Helper


class Game(object):
    def __init__(self, resolution, mode="windowed"):
        # Base setup
        self.directory = os.getcwd()

        try:
            pygame.init()
            self.pygame = pygame
        except Exception:
            self.log("Failed to initialise pygame")
        self.system = System(self)
        self.width = self.system.MONITOR_WIDTH
        self.height = self.system.MONITOR_HEIGHT
        self.initialise_screen(resolution, mode)
        pygame.display.set_caption("insertnamehere (Alpha 1.0)")
        #! pygame.display.set_icon(self.load_image("icon_name.ico"))

        self.current = "main menu"
        self.fps = 60
        self.frame = 0  # The current frame the game is on (since the game was opened)

        self.console = Console(self)
        self.input = Input(self)

        self.quit_condition = Hotkey(self, "f4", alt=True).pressed

        # Main setup
        self.helper = Helper(self)
        #!!! TEST - REMOVE
        self.text_input = TextInput(self)
        #!!! TEST - REMOVE

        self.options = {
            #! Add a function to make this load the player's settings from a file of
            # some sort. YAML if you don't care about hiding settings from users.
            # Inventory
            "show item info at side": False
        }
        #!!! TEST - REMOVE
        self.text_input.enable(100)
        #!!! TEST - REMOVE

    # Main functions
    def logic(self):
        self.check_quit()
        self.console.logic()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.console.draw()
        #!!! TEST - REMOVE
        self.text_input.display(pygame.font.SysFont("Arial Black", 40, False, False),
                                (255, 255, 255), (0, 0))
        #!!! TEST - REMOVE

    def quit(self):
        #! Add code for autosaving the game here
        pygame.quit()

    # Base functions
    def path_to(self, *path):
        """Returns the complete absolute path of the path given."""
        return os.path.join(self.directory, *"/".join(path).split("/"))

    def log(self, *error_message):
        """Takes 1 or more variables and concatenates them to create the error message."""
        def error_popup(error_info):
            text = "".join(("An error has occurred:\n\n    ",
                            error_message, ".\n\n\n",
                            error_info, "."))
            ctypes.windll.user32.MessageBoxA(0, text, "Error", 0)

        try:
            error_message = "".join(map(str, error_message))
            with open(self.path_to("log.txt"), "a") as error_log:
                error_log.write("".join((
                    str(datetime.datetime.utcnow())[0:19], " - ", error_message, ".\n",
                    traceback.format_exc(), "\n"
                    )))
        except:    # Likely only when self.file_directory has not yet been defined
            error_popup("This error occurred very early during "
                        "game initialisation and could not be logged")
            raise
        #! Add some code here to show a message in game instead of
        # force quitting the game unless the error is sufficiently bad.
        # fatal_error (below) should depend on this code,
        # or it can be passed in to log() as a argument.
        fatal_error = True
        if fatal_error:
            error_popup("Please check log.txt for details")
            raise

    def initialise_screen(self, resolution=None, mode="fullscreen"):
        """(Re)initialises the screen using the given arguments."""
        try:
            if resolution is None:
                resolution = (self.width, self.height)
            flags = pygame.HWSURFACE | pygame.DOUBLEBUF
            if mode == "fullscreen":
                flags = flags | pygame.FULLSCREEN
            elif mode == "windowed":
                # Positioning the window in the centre of the screen
                os.environ['SDL_VIDEO_WINDOW_POS'] = "".join((
                    str((self.system.MONITOR_WIDTH - resolution[0])/2), ",",
                    str((self.system.MONITOR_HEIGHT - resolution[1])/2)
                    ))
            elif mode == "borderless":
                os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                flags = flags | pygame.NOFRAME
            else:
                raise ValueError("".join((
                    "Unknown mode for reinitialise_screen(): \"", mode, "\""
                    )))

            self.screen = pygame.display.set_mode(resolution, flags)
            self.width, self.height = resolution
        except Exception:
            self.log("Failed to reinitialise screen in ", mode, " mode "
                     "at ", self.width, "x", self.height, " resolution")

    # Asset loading
    def load_image(self, image_name, fade_enabled=False):
        """fade_enabled should be True if you want images to be able to fade"""
        try:
            #! Add stuff for loading images of the correct resolution
            # depending on the player's resolution settings
            if not fade_enabled:
                return pygame.image.load(
                    self.path_to("assets/images", image_name + ".png")
                    ).convert_alpha()   # Fixes per pixel alphas permanently
            else:
                return pygame.image.load(
                    self.path_to("assets/images", image_name + ".png")
                    ).convert()
        except Exception:
            self.log("Failed to load image: ", image_name, ".png")

    def load_font(self, font_name, font_size):
        try:
            return pygame.font.Font(
                self.path_to("assets/fonts", font_name + ".ttf"), font_size
                )
        except Exception:
            self.log("Failed to load font: ", font_name, ".ttf")

    def display(self, image, coordinates, area=None, special_flags=0):
        """Takes coordinates and area for a 1920x1080 window"""
        try:
            x_scale = self.width/1920.0
            y_scale = self.height/1080.0
            coordinates = (coordinates[0]*x_scale, coordinates[1]*y_scale)
            if area is not None:
                area = (area[0]*x_scale, area[1]*y_scale,
                        area[2]*x_scale, area[3]*y_scale)
            self.screen.blit(image, coordinates, area, special_flags)
        except Exception:
            self.log("Failed to display image at ", coordinates)

    def inputs(self):
        self.input.reset()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.input.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input.buttondown(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.input.buttonup(event.button)
            elif event.type == pygame.KEYDOWN:
                self.input.buttondown(event)
                TextInput.receive_single_characters(event)
            elif event.type == pygame.KEYUP:
                self.input.buttonup(event.key)
        TextInput.receive_multiple_characters()

    def update(self):
        self.frame += 1
        try:
            pygame.display.flip()   # Updating the screen
            self.clock.tick(self.fps)    # [fps] times per second
        except Exception:
            self.log("Failed to update screen")

    def runtime(self):
        try:
            return time.time() - self.start_time
        except Exception:
            self.log("Failed to calculate and return game run time")

    def check_quit(self):
        if self.quit_condition():
            self.running = False

    def run(self):
        self.running = True
        try:
            self.clock = pygame.time.Clock()
            self.start_time = time.time()
        except Exception:
            self.log("Failed to initialise essential time related display variables")

        while self.running:
            self.inputs()
            self.logic()
            self.draw()
            self.update()

        self.quit()
