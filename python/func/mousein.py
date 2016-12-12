def mousein(x, y, width, height):
    """Takes in coordinates for a 1920x1080 screen"""
    global error
    try:
        if (mouse_x > x*(screen_width/1920.0) and mouse_x < (x + width)*(screen_width/1920.0)
            and mouse_y > y*(screen_height/1080.0) and mouse_y < (y + height)*(screen_height/1080.0)):
            return True
        else:
            return False
    except Exception, error:
        log("".join(("Unable to determine whether mouse coordinates meet the requirements: ",
                     str(x), " < x < ", str(x + width), ", ",
                     str(y), " < y <  ", str(y + height))))
