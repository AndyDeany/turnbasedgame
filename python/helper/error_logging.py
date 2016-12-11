# Defining the error logging function
def log(error_message):
    def write_to_log_file(raised_error="Details Unknown"):
        error_log.write("".join((
            str(datetime.datetime.utcnow())[0:19], " - ",
            error_message, ": ", str(raised_error), "\n"
            )))

    def error_popup(error_info):
        ctypes.windll.user32.MessageBoxA(
            0,
            "".join(("An error has occurred:\n\n    ",
                     error_message,
                     ".\n\n\n",
                     error_info, ".")),
            "Error",
            1
            )

    try:
        error_log = open("".join((file_directory, "log.txt")), "a")
        try:
            write_to_log_file(error)
        except:
            write_to_log_file()
        error_log.close()
    except:    # Likely only when file_directory has not yet been defined
        error_popup("This error occurred very early during"
                    "game initialisation and could not be logged")
        raise
    #! Add some code here to show a message in game instead of
    # force quitting the game unless the error is sufficiently bad.
    # fatal_error (below) should depend on this code,
    # or it can be passed in to log() as a parameter.
    fatal_error = True
    if fatal_error:
        error_popup("Please check log.txt for details")
        raise
