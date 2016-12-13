def mousein(x, y, width, height):
    """Determines if the mouse is in the given rectangle"""
    global error
    try:
        if (mouse_x > x and mouse_x < (x + width) and
                mouse_y > y and mouse_y < (y + height)):
            return True
        else:
            return False
    except Exception, error:
        log("".join(("Unable to determine whether mouse coordinates meet the requirements: ",
                     str(x), " < x < ", str(x + width), ", ",
                     str(y), " < y <  ", str(y + height))))
