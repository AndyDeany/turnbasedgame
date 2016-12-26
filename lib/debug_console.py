from text_input import TextInput
from hotkey import Hotkey

class DebugConsole(object):
    """
    Class for creating a debug console to allow code to be
    executed at runtime. Should NOT be left in the game when compiled.
    """
    def __init__(self, game):
        self.game = game
        try:
            self.text_input = TextInput(self.game)

            self.active = False
            self.toggle_active_hotkey = Hotkey(self.game, "`").pressed

            self.font = self.game.pygame.font.SysFont("consolas", 15)
            self.input_colour = (255, 255, 255)  # white

            # Placeholder
            text = "enter command"
            font = self.game.pygame.font.SysFont("consolas", 15, italic=True)
            colour = (150, 150, 150)  # grey
            self.placeholder_text = font.render(text, True, colour)

            self.output_display_time = 5    # seconds
            self.output_start_frame = -self.output_display_time * self.game.fps
            self.default_output_colour = (255, 255, 255)
            self.error_output_colour = (255, 0, 0)
            self.saved_input = ""
            self.output = self.font.render("", True, self.default_output_colour)

            # Prompt
            prompt = "> "
            self.prompt = self.font.render(prompt, True, self.input_colour)

            prompt_width = self.prompt.get_width()
            text_height = self.prompt.get_height()
            self.prompt_coordinates = (0, game.height - text_height)
            self.input_coordinates = (self.prompt_coordinates[0] + prompt_width,
                                      self.prompt_coordinates[1])
            self.output_coordinates = (0, game.height - 2*text_height)
        except Exception as self.game.error:
            self.game.log("Failed to initialise debug console object")

    def logic(self):
        if self.toggle_active_hotkey():
            if self.active:
                self.active = False
                self.saved_input = self.text_input.text[:-1]    # Stripping trailing "`" character
            else:
                self.active = True
                self.text_input.enable(200)
                self.text_input.text = self.saved_input

        if self.active and not self.text_input.accepting_text:
            command = self.text_input.most_recent()
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
            self.text_input.enable(200)

    def draw(self):
        if self.active:
            self.game.screen.blit(self.prompt, self.prompt_coordinates)
            if self.text_input.text == "":
                self.game.screen.blit(self.placeholder_text, self.input_coordinates)
            else:
                self.game.screen.blit(
                    self.font.render(self.text_input.text, True, self.input_colour),
                    self.input_coordinates
                )

        if (self.game.frame - self.output_start_frame <
                self.output_display_time * self.game.fps):
            self.game.screen.blit(self.output, self.output_coordinates)
        else:   # Resetting self.output to nothing
            self.output = self.font.render("", True, self.default_output_colour)
