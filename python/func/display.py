def display(image, coordinates, area=None, special_flags=0):
    """Takes coordinates for a 1920x1080 window"""
    try:
        coordinates = (coordinates[0]*(screen_width/1920.0), coordinates[1]*(screen_height/1080.0))
        screen.blit(image, coordinates, area, special_flags)
    except Exception as error:
        log(" ".join(("Failed to display image at", str(coordinates))))
