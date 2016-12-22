class Helper(object):
    """Class holding helper functions."""
    def __init__(self, game):
        self.game = game

    def load_class_assets(self, calling_object, assets_dict):
        for attribute_name in assets_dict:
            calling_class = calling_object.__class__
            setattr(calling_class, attribute_name, assets_dict[attribute_name])

    def mousein(self, x, y, width, height):
        """Determines if the mouse is in the given rectangle."""
        try:
            return (x < self.game.mouse[0] < x + width and
                    y < self.game.mouse[1] < y + height)
        except Exception as self.game.error:
            self.game.log("Unable to determine whether mouse position meet the requirements ",
                         x, " < x < ", x + width, ", ", y, " < y <  ", y + height)

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
