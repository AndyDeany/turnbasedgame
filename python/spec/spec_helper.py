from expects import *

import os
import ctypes
import datetime

import pygame
pygame.init()

file_directory = "".join((os.path.dirname(os.getcwd()), "\\"))

execfile("spec/support/error_logging.py")   # Altered log function
execfile("helper/asset_loading.py")
execfile("helper/initialise_screen.py")

for python_file in os.listdir("func"):
    execfile("".join(("func\\", python_file)))

execfile("helper/abstract_classes.py")
for python_file in os.listdir("lib"):
    execfile("".join(("lib\\", python_file)))
