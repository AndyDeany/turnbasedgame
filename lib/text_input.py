class TextInput(object):
    instances = []
    active = False

    def __init__(self, game):
        self.game = game

        self.accepting_text = False     # Showing whether text is currently being accepted
        self.text = ""              # The input text from the user
        self.max_characters = 0     # The maximum amount of allowed characters in an input text
        self.inputs = []    # List of inputs. Most recent at index 0

        self.instances.append(self)

    def delete(self):
        self.instances.remove(self)

    def enable(self, max_characters):
        """Enables text input to be taken from the user."""
        # Maybe turn this into a function which creates a text field
        # at given coordinates or something
        self.text = ""
        self.max_characters = max_characters
        if self.active:
            for instance in self.instances:
                instance.accepting_text = False
        else:
            setattr(TextInput, "active", True)
        self.accepting_text = True

    def display(self, font, colour, coordinates, antialias=True, background=None):
        try:
            if background is None:
                self.game.screen.blit(font.render(self.text, antialias, colour),
                                      coordinates)
            else:
                self.game.screen.blit(font.render(self.text, antialias, colour, background),
                                      coordinates)
        except Exception as self.game.error:
            self.game.log("Failed to display text input")

    def disable(self):
        """Disables text input from being taken from the user."""
        self.accepting_text = False
        self.inputs.insert(0, self.text)
        setattr(TextInput, "active", False)

    def most_recent(self):
        """Returns the most recent input."""
        return self.inputs[0]

    @classmethod
    def active_instance(self):
        """Returns the instance that is currently accepting text."""
        return next((instance for instance in self.instances
                     if instance.accepting_text), None)

    @classmethod
    def receive_single_characters(self, event):
        if self.active:
            active_instance = self.active_instance()
            try:
                if not (active_instance.game.input.buttons["leftctrl"].held or
                        active_instance.game.input.buttons["rightctrl"].held or
                        active_instance.game.input.buttons["alt"].held):
                    if event.key == 8:
                        if active_instance.text != "":
                            active_instance.text = active_instance.text[:-1]
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
                    elif event.key in [13, 271]:    # Enter and numpad enter
                        active_instance.disable()
                    elif len(active_instance.text) < active_instance.max_characters:
                        active_instance.text = "".join((active_instance.text, event.unicode))
            except Exception as active_instance.game.error:
                active_instance.game.log("Failed to receive input from a key press"
                                         "[event.key = ", event.key, "]")

    character_keys = (
        [n for n in range(44, 58)]
        + [n for n in range(96, 123)]
        + [n for n in range(256, 272)]
        + [39, 59, 60, 61, 91, 92, 93]
    )

    @classmethod
    def receive_multiple_characters(self):
        def return_key(n):
            return self.keys[n]
        if self.active:
            active_instance = self.active_instance()
            try:
                if (active_instance.game.frame % (active_instance.game.fps/30) == 0 and
                    # This (above) means that characters are written/deleted [30] times per second
                    # when their key is held down, which feels natural.
                    not (active_instance.game.input.buttons["leftctrl"].held or
                         active_instance.game.input.buttons["rightctrl"].held or
                         active_instance.game.input.buttons["alt"].held)):
                    if active_instance.game.input.buttons["backspace"].time_held() > 0.5:
                        if active_instance.text != "":
                            active_instance.text = active_instance.text[:-1]
                    elif (len(active_instance.text) < active_instance.max_characters and
                          # Checking if a key has been held for half a second or longer.
                          # max((button.time_held() for button in active_instance.game.input.buttons
                          #      if button.number in character_keys)) > 0.5):
                          max((active_instance.game.input.buttons[key_name].time_held()
                               for key_name in (
                                " ", "'", ",", "-", ".", "/",
                                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                                ";", "\\", "=", "[", "#", "]", "`",
                                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                                "numpad0", "numpad1", "numpad2", "numpad3", "numpad4",
                                "numpad5", "numpad6", "numpad7", "numpad8", "numpad9",
                                "numpad.", "numpad/", "numpad*", "numpad-", "numpad+"
                            ))) > 0.5):
                        self.keys = active_instance.game.pygame.key.get_pressed()
                        # Checking that only one key that provides a character input is pressed.
                        if (sum(map(return_key, self.character_keys)) == 1 and
                                active_instance.text != ""):
                            active_instance.text += active_instance.text[-1]
            except Exception as active_instance.game.error:
                active_instance.game.log("Failed to receive text input from held keys")
