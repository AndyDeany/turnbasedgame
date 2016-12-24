class DebugConsole(object):
    """
    Class for creating a debug console to allow code to be
    executed at runtime. Should NOT be left in the game when compiled.
    """
    def __init__(self, game):
        self.game = game
        try:
            self.font = self.game.pygame.font.SysFont("consolas", 15)
            self.text_colour = (255, 255, 255)  # white

            self.output_display_time = 5    # seconds
            self.output_start_frame = -self.output_display_time * self.game.fps
            self.default_output_colour = (255, 255, 255)
            self.error_output_colour = (255, 0, 0)
            self.output = self.font.render("", True, self.default_output_colour)

            text_height = self.font.size("")[1]
            self.input_coordinates = (0, game.height - text_height)
            self.output_coordinates = (0, game.height - 2*text_height)

            self.game.input.take_text(200, "debug console")
        except Exception as self.game.error:
            self.game.log("Failed to initialise debug console object")

    def logic(self):
        if not self.game.input.accepting_text:
            command = self.game.input.most_recent_output("debug console")
            try:
                self.output = self.font.render(str(eval(command)), True,
                                               self.default_output_colour)
            except:
                try:
                    exec(command)
                except Exception as error:
                    self.output = self.font.render(str(error), True,
                                                   self.error_output_colour)

            self.output_start_frame = self.game.frame
            self.game.input.take_text(200, "debug console")

    def draw(self):
        if self.game.input.output_label == "debug console":
            self.game.screen.blit(
                self.font.render(self.game.input.text, True, self.text_colour),
                self.input_coordinates
            )

        if (self.game.frame - self.output_start_frame <
                self.output_display_time * self.game.fps):
            self.game.screen.blit(self.output, self.output_coordinates)
        else:   # Resetting self.output to nothing
            self.output = self.font.render("", True, self.default_output_colour)
