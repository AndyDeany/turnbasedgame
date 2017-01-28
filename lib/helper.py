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
        except Exception:
            self.game.log("Failed to load ", calling_class.__name__, " class assets")
        setattr(calling_class, "class_assets_loaded", True)

    def wrap_text(self, text, font, max_width):
        """
        Returns an array of lines which can be blitted beneath each other
        in the given font in a box of the given maximum width.
        """
        def wrap_paragraph(paragraph):
            """Wraps text that doesn't contain newlines."""
            def too_long(string):
                return font.size(string)[0] > max_width

            def raise_word_too_long_error(word):
                raise ValueError("\"%s\" is too long to be wrapped." % word)

            lines = []
            words = paragraph.split()

            line = words.pop(0)
            if too_long(line):
                raise_word_too_long_error(line)

            for word in words:
                if too_long(word):
                    raise_word_too_long_error(word)

                if too_long(" ".join((line, word))):
                    lines.append(line)
                    line = word
                else:
                    line = " ".join((line, word))

            lines.append(line)
            return lines

        try:
            paragraphs = text.split("\n")
            return sum(map(wrap_paragraph, paragraphs), [])
        except Exception:
            self.game.log("Failed to wrap text: \"", text, "\"")
