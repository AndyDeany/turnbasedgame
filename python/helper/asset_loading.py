# Defining a function to load images
def load_image(image_name, fade_enabled=False):
    """fade_enabled should be True if you want images to be able to fade"""
    global error
    try:
        #! Add stuff for loading images of the correct resolution
        # depending on the player's resolution settings
        if not fade_enabled:
            return pygame.image.load("".join((
                file_directory, "assets\\images\\",
                image_name, ".png"
                ))).convert_alpha()   # Fixes per pixel alphas permanently
        else:
            return pygame.image.load("".join((
                file_directory, "assets\\images\\",
                image_name, ".png"
                ))).convert()
    except Exception as error:
        log("".join(("Failed to load image: ", image_name, ".png")))

def load_font(font_name, font_size):
    global error
    try:
        return pygame.font.Font("".join((
            file_directory, "assets\\fonts\\",
            font_name, ".ttf"
            )), font_size)
    except Exception as error:
        log("".join(("Failed to load font: ", font_name, ".ttf")))
