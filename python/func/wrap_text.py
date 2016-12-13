def wrap_text(text, font, max_width):
    """
    Returns an array of lines which can be blitted beneath each other
    in the given font in a box of the given max_width
    """
    global error
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
                    width = font.size(" ".join((line, words[0])))

            if font.size(line)[0] > max_width:
                raise ValueError("".join(("\"", line, "\"", " is too long to be wrapped.")))
            lines.append(line)

        return lines
    except Exception as error:
        log("".join(("Failed to wrap text: \"", text, "\"")))
