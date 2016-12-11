# Importing modules that are required for the error logging function to work
import os
import ctypes
import datetime

# Obtaining the location of the game files
file_directory = "".join((os.path.dirname(os.getcwd()), "\\"))
#! This (above) might be unneccessary with relative paths. Might be more robust though.

# Defining functions for logging errors
execfile("helper\\error_logging.py")

# Defining functions for loading assets such as images, videos, sounds etc.
execfile("helper\\asset_loading.py")

### ---------- IMPORTING MODULES - START ---------- ###
try:    # Importing and initialising pygame
    import pygame
    try:
        import pygame._view     # sometimes necessary. If it isn't this will cause an error
        #! UPDATE: this might only be necessary for py2exe to work, so if you can
        # compile without it, then there's no need to import pygame_view whatsoever
    except Exception:
        pass
    pygame.init()
except Exception as error:
    log("Failed to initialise pygame")

try:    # Importing other modules
    import sys
    import time
    import math
    import random
except Exception as error:
    log("Failed to import modules")
### ---------- IMPORTING MODULES - END ---------- ###


### ---------- INITIALISING GLOBAL VARIABLES - START ---------- ###
try:    # Initialising game screen
    execfile("helper\\initialise_screen.py")
except Exception as error:
    log("Failed to initialise game screen")

# Initialising other global variables
current = "main menu"   # The part of the game the screen is showing
fps = 60
frame = 1   # The current frame the game is on (since the game was opened)
# Creating variables for keyboard and mouse inputs
execfile("helper\\reset_inputs.py")
execfile("helper\\input_attributes.py")
### ---------- INITIALISING GLOBAL VARIABLES - END ---------- ###

### ---------- FUNCTION DEFINITIONS - START ---------- ###
for python_file in os.listdir("func"):
    try:
        execfile("".join(("func\\", python_file)))
    except Exception as error:
        log("".join(("Failed to load file: func\\", python_file)))
### ---------- FUNCTION DEFINITIONS - END ---------- ###

### ---------- CLASS DEFINITIONS - START ---------- ###
for python_file in os.listdir("lib"):
    try:
        execfile("".join(("lib\\", python_file)))
    except Exception as error:
        log("".join(("Failed to load file: lib\\", python_file)))
### ---------- CLASS DEFINITIONS - END ---------- ###

### ---------- PROGRAM DISPLAY - START ---------- ###
# Initialising essential display variables
ongoing = True
try:
    clock = pygame.time.Clock()
    start_time = time.time()
except Exception as error:
    log("Failed to initialise essential display variables")
#!!! TEST - REMOVE
TextInput.take_input(50, "test")
#!!! TEST - REMOVE
## Game window while loop
while ongoing:
    try:
        current_time = time.time() - start_time
    except Exception as error:
        log("Failed to update game run time")

    try:
        execfile("helper\\reset_inputs.py")
    except Exception as error:
        log("Failed to reset user input values")

    try:
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
    except Exception as error:
        log("Failed to determine mouse position")

    try:
        execfile("helper\\input_timer.py")
    except Exception as error:
        log("Failed to calculate key held duration")
    #!!! TEST - REMOVE
    screen.fill((0, 0, 0))
    screen.blit(pygame.font.SysFont(
        "Arial Black", 40, False, False
        ).render(TextInput.text, True, (255, 255, 255)), (0, 0))
    #!!! TEST - REMOVE

    try:    # Receiving user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # When the user exits the game manually
                ongoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: left_held = 1
                elif event.button == 2: middle_held = 1
                elif event.button == 3: right_held = 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left = 1
                    left_held = 0
                elif event.button == 2:
                    middle = 1
                    middle_held = 0
                elif event.button == 3:
                    right = 1
                    right_held = 0
            elif event.type == pygame.KEYDOWN:
                execfile("helper\\keydown.py")
                if alt_held and f4_held and f4_held_time < alt_held_time:
                    ongoing = False     # Quits the game. Add an "are you sure" prompt if you want
                TextInput.receive_single_characters()
            elif event.type == pygame.KEYUP:
                execfile("helper\\keyup.py")
    except Exception as error:
        log("Failed to receive user inputs correctly")

    try:
        TextInput.receive_multiple_characters()
    except Exception as error:
        log("Failed to receive multiple characters for text input correctly")

    frame += 1
    try:
        pygame.display.flip()   # Updating the screen
        clock.tick(fps)         # [fps] times per second
    except Exception as error:
        log("Failed to update screen")
### ---------- PROGRAM DISPLAY - END ---------- ###

#! Add code for autosaving the game

pygame.quit()
