from button import Button
from hotkey import Hotkey

class Input(object):
    """
    Class for holding all variables and functions to do with receiving
    keyboard input from the user.
    """
    def __init__(self, game):
        self.game = game
        try:
            self.mouse_pos = (0, 0)

            self.accepting_text = False     # Showing whether the program is accepting text input
            self.text = ""              # The input text from the user
            self.max_characters = 0     # The maximum amount of allowed characters in an input text
            # List of dictionaries {label, text} storing output values from text inputs
            self.output = []    # See self.accept_text() for more detail
            self.output_label = ""

            # A list of all the keys that can produce characters when pressed
            self.character_keys = (
                [n for n in range(44, 58)] +
                [n for n in range(96, 123)] +
                [n for n in range(256, 272)] +
                [39, 59, 60, 61, 91, 92, 93]
                )
        except Exception as self.game.error:
            self.game.log("Failed to initialise keyboard input object")

        self.buttons = {name: Button(self.game, number) for name, number in [
            # Mouse inputs
            ("leftmouse", 1), ("middlemouse", 2), ("rightmouse", 3),

            ("backspace", 8), ("tab", 9), ("enter", 13),
            ("pausebreak", 19), ("escape", 27),
            (" ", 32), ("'", 39), (",", 44), ("-", 45), (".", 46), ("/", 47),

            # Numbers across the top)
            ("0", 48), ("1", 49), ("2", 50), ("3", 51), ("4", 52),
            ("5", 53), ("6", 54), ("7", 55), ("8", 56), ("9", 57),

            (";", 59), ("\\", 60), ("=", 61), ("[", 91),
            ("#", 92), ("]", 93), ("`", 96),

            # Alphabet keys)
            ("a", 97), ("b", 98), ("c", 99), ("d", 100), ("e", 101),
            ("f", 102), ("g", 103), ("h", 104), ("i", 105), ("j", 106),
            ("k", 107), ("l", 108), ("m", 109), ("n", 110), ("o", 111),
            ("p", 112), ("q", 113), ("r", 114), ("s", 115), ("t", 116),
            ("u", 117), ("v", 118), ("w", 119), ("x", 120), ("y", 121), ("z", 122),

            ("delete", 127),

            # Numpad)
            ("numpad0", 256), ("numpad1", 257), ("numpad2", 258),
            ("numpad3", 259), ("numpad4", 260), ("numpad5", 261),
            ("numpad6", 262), ("numpad7", 263), ("numpad8", 264),
            ("numpad9", 265), ("numpad/", 266), ("numpad*", 267),
            ("numpad-", 268), ("numpad+", 269), ("numpadenter", 270),

            # Arrow keys)
            ("up", 273), ("down", 274), ("right", 275), ("left", 276),

            ("insert", 277), ("home", 278), ("end", 279),
            ("pageup", 280), ("pagedown", 281),

            # F keys)
            ("f1", 282), ("f2", 283), ("f3", 284), ("f4", 285),
            ("f5", 286), ("f6", 287), ("f7", 288), ("f8", 289),
            ("f9", 290), ("f10", 291), ("f11", 292), ("f12", 293),

            # Key modifiers)
            ("rightshift", 303), ("leftshift", 304),
            ("rightctrl", 305), ("leftctrl", 306), ("alt", 308)
        ]}

    def reset(self):
        for button in self.buttons.values():
            button.reset()

    def buttondown(self, number):
        try:
            next((button for button in self.buttons.values() if button.number == number)).press()
        except Exception as self.game.error:
            self.game.log("Failed to process a button being pressed [event number=", number, "]")

    def buttonup(self, number):
        try:
            next((button for button in self.buttons.values() if button.number == number)).release()
        except Exception as self.game.error:
            self.game.log("Failed to process a button being released [event number=", number, "]")

    def mousein(self, x, y, width, height):
        """Determines if the mouse is in the given rectangle."""
        try:
            return (x < self.mouse_pos[0] < x + width and
                    y < self.mouse_pos[1] < y + height)
        except Exception as self.game.error:
            self.game.log("Unable to determine whether mouse position meet the requirements ",
                          x, " < x < ", x + width, ", ", y, " < y <  ", y + height)

    def take_text(self, max_characters, output_label=""):
        """
        Enables text input to be taken from the user and
        labels with the given label
        """
        # Maybe turn this into a function which creates a text field
        # at given coordinates or something
        self.text = ""
        self.output_label = output_label
        self.max_characters = max_characters
        self.accepting_text = True

    def display_text(self, font, colour, coordinates, antialias=True, background=None):
        try:
            if background is None:
                self.game.screen.blit(font.render(self.text, antialias, colour),
                                      coordinates)
            else:
                self.game.screen.blit(font.render(self.text, antialias, colour, background),
                                      coordinates)
        except Exception as self.game.error:
            self.game.log("Failed to display input text")

    def accept_text(self):
        self.accepting_text = False
        self.output.insert(0, {
            "label": self.output_label,
            "text": self.text
        })

    def most_recent_output(self, label=None):
        """Returns the most recent output (with the given label if label is given)."""
        if label is None:
            return self.output[0]["text"]
        else:
            return next((output["text"] for output in self.output if output["label"] == label))

    def all_outputs(self, label=None):
        """Returns a tuple of all outputs (with the given label if label is given)."""
        if label is None:
            return (output["text"] for output in self.output)
        else:
            return (output["text"] for output in self.output if output["label"] == label)

    def receive_single_characters(self, event):
        try:
            if (self.accepting_text and
                not (self.buttons["leftctrl"].held or
                     self.buttons["rightctrl"].held or
                     self.buttons["alt"].held)):
                if event.key == 8:
                    if self.text != "":
                        self.text = self.text[:-1]
                elif event.key == 9:
                    #! This (above) is the TAB key. Perhaps it should
                    # make the cursor go to the next box and this
                    # would be a good place to do it, since it would
                    # only be applicable when inputting text. The only
                    # reason this would be pointless is if
                    # there are never two text boxes to fill in on
                    # the same screen, or if this functionality is
                    # unneeded which isn't that unlikely,
                    # so it may actually be pointless.
                    pass
                elif event.key == 13:   # Enter key
                    self.accept_text()
                elif len(self.text) < self.max_characters:
                    self.text = "".join((self.text, event.unicode))
        except Exception as self.game.error:
            self.game.log("Failed to receive input from key press")

    def receive_multiple_characters(self):
        def return_key(n):
            return self.keys[n]
        try:
            if (self.accepting_text and
                self.game.frame % (self.game.fps/30) == 0 and
                # This (above) means that characters are written/deleted [30] times per second
                # when their key is held down, which feels natural.
                not (self.buttons["leftctrl"].held or
                     self.buttons["rightctrl"].held or
                     self.buttons["alt"].held)):
                if self.buttons["backspace"].time_held() > 0.5:
                    if self.text != "":
                        self.text = self.text[:-1]
                elif (len(self.text) < self.max_characters and
                      # Checking if a key has been held for half a second or longer.
                      max([self.buttons[key_name].time_held() for key_name in [
                        " ", "'", ",", "-", ".", "/",
                        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                        ";", "\\", "=", "[", "#", "]", "`",
                        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                        "numpad0", "numpad1", "numpad2", "numpad3", "numpad4",
                        "numpad5", "numpad6", "numpad7", "numpad8", "numpad9",
                        "numpad/", "numpad*", "numpad-", "numpad+"
                        ]]) > 0.5):
                    self.keys = self.game.pygame.key.get_pressed()
                    # Checking that only one key that provides a character input is pressed.
                    if sum(map(return_key, self.character_keys)) == 1:
                        self.text += self.text[-1]
        except Exception as self.game.error:
            self.game.log("Failed to receive text input from held keys")
