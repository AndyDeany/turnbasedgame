def monitor_info():
    info = pygame.display.Info()
    return info.current_w, info.current_h

# Defining a function to change the screen settings after it has been created
def initialise_screen(resolution=(0, 0), mode="fullscreen"):
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

# Initialising screen for the first time
MONITOR_WIDTH, MONITOR_HEIGHT = monitor_info()
screen_width, screen_height = MONITOR_WIDTH, MONITOR_HEIGHT
#! Decide how the window should be when the game opens. Fullscreen? Borderless? Windowed?
# How big should it be? User's monitor dimensions? Something else?
initialise_screen((1280, 720), "windowed")

#! These could be added to initialise_screen()
pygame.display.set_caption("insertnamehere (Alpha 1.0)")
#! pygame.display.set_icon()    add the path to an image for the icon as the argument
