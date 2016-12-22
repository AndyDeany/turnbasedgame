class Helper(object):
    """Class holding helper functions."""
    def __init__(self, game):
        self.game = game

    def load_class_assets(self, calling_object, assets_dict):
        """Loads class assets. Should only be calling if self.class_assets_loaded is False."""
        try:
            for attribute_name in assets_dict:
                calling_class = calling_object.__class__
                setattr(calling_class, attribute_name, assets_dict[attribute_name])
        except Exception as self.game.error:
            self.game.log("Failed to load ", calling_class.__name__, " class assets")
        setattr(calling_class, "class_assets_loaded", True)

    def wrap_text(self, text, font, max_width):
        """
        Returns an array of lines which can be blitted beneath each other
        in the given font in a box of the given maximum width.
        """
        try:
            lines = []
            words = text.split(" ")

            while words:
                line = words.pop(0)
                if words:
                    width = font.size(" ".join((line, words[0])))[0]
                    while width < max_width:
                        if words[0] == "\n":
                            del words[0]
                            break
                        line = " ".join((line, words.pop(0)))
                        if not words:
                            break
                        width = font.size(" ".join((line, words[0])))[0]

                if font.size(line)[0] > max_width:
                    raise ValueError("".join(("\"", line, "\"", " is too long to be wrapped.")))
                lines.append(line)

            return lines
        except Exception as self.game.error:
            self.game.log("Failed to wrap text: \"", text, "\"")
