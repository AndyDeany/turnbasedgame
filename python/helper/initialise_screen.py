screen = pygame.display.set_mode(
        (0, 0),     # (0, 0) resolution defaults to the user's screen size
        pygame.HWSURFACE | pygame.DOUBLEBUF     #!|pygame.FULLSCREEN)
        )
#! Decide how the window should be when the game opens. Fullscreen? Borderless? Windowed?
screen_width = screen.get_width()
screen_height = screen.get_height()
MONITOR_WIDTH = screen_width
MONITOR_HEIGHT = screen_height

# Defining a function to change the screen settings after it has been created
def reinitialise_screen(resolution=(screen_width, screen_height), mode="fullscreen"):
    global error
    try:
        global screen, screen_width, screen_height
        screen_width = resolution[0]
        screen_height = resolution[1]
        if mode == "fullscreen":
            screen = pygame.display.set_mode(
                resolution,
                pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN
                )
        elif mode == "windowed":
            # Positioning the window in the centre of the screen
            os.environ['SDL_VIDEO_WINDOW_POS'] = "".join((
                str((MONITOR_WIDTH - screen_width)/2), ",",
                str((MONITOR_HEIGHT - screen_height)/2)
                ))
            screen = pygame.display.set_mode(
                resolution,
                pygame.HWSURFACE | pygame.DOUBLEBUF
                )
        elif mode == "borderless":
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
            screen = pygame.display.set_mode(
                resolution,
                pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME
                )
        else:
            raise Exception("".join(("Unknown mode for reinitialise_screen(): \"", mode, "\" "
                                     "[syntax error].")))
    except Exception as error:
        log("".join(("Failed to reinitialise screen in ", mode, " mode "
                     "at ", str(screen_width), "x", str(screen_height), " resolution")))

#! This (below) could all be removed, along with reinitialise_screen,
# if you decide to have a fixed resolution.
# resolutions = [_list of tuples of available resolutions_]
# if (MONITOR_WIDTH, MONITOR_HEIGHT) not in resolutions:
#      screen_width = 0
#      screen_height = 0
#      for resolution in resolutions:
#          if resolution[0] <= MONITOR_WIDTH:
#              if screen_width < resolution[0]:
#                  screen_width = resolution[0]
#                  screen_height = resolution[1]
#              elif (screen_width == resolution[0] and
#                    resolution[1] <= MONITOR_HEIGHT and
#                    screen_height < resolution[1]):
#                  screen_height = resolution[1]
#
#      reinitialise_screen(screen_width, screen_height)

pygame.display.set_caption("insertnamehere (Alpha 1.0)")
#! pygame.display.set_icon()    add the path to an image for the icon as the argument
