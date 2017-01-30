from text_input import TextInput
from hotkey import Hotkey

class DebugConsole(object):
    """
    Class for creating a debug console to allow code to be
    executed at runtime. Should NOT be left in the game when compiled.
    """
    def __init__(self, game,
                 max_command_length=200,
                 font_name="consolas",
                 font_size=15,
                 input_colour=(255, 255, 255),  # white
                 placeholder_text="enter command",
                 placeholder_colour=(150, 150, 150),    # grey
                 output_display_time=5,     # seconds
                 default_output_colour=(255, 255, 255),     # white
                 error_output_colour=(255, 0, 0),  # red
                 prompt="> "):
        self.game = game
        try:
            self.text_input = TextInput(self.game)

            self.max_command_length = max_command_length
            # Maybe remove this and make it so commands just can't go off the screen

            self.active = False     # Whether the console is open
            self.toggle_active_hotkey = Hotkey(self.game, "`").pressed

            self.font = self.game.pygame.font.SysFont(font_name, font_size)
            self.input_colour = input_colour    # white

            # Placeholder
            font = self.game.pygame.font.SysFont(font_name, font_size, italic=True)
            self.placeholder_text = font.render(placeholder_text, True, placeholder_colour)

            self.output_display_time = output_display_time
            self.output_start_frame = -self.output_display_time * self.game.fps
            self.default_output_colour = default_output_colour
            self.error_output_colour = error_output_colour
            self.saved_input = ""
            self.default_output = self.font.render("", True, self.default_output_colour)
            self.output = self.default_output

            # Prompt
            self.prompt = self.font.render(prompt, True, self.input_colour)

            prompt_width = self.prompt.get_width()
            text_height = self.prompt.get_height()
            self.prompt_coordinates = (0, game.height - text_height)
            self.input_coordinates = (self.prompt_coordinates[0] + prompt_width,
                                      self.prompt_coordinates[1])
            self.output_coordinates = (0, game.height - 2*text_height)

            # Previous commands
            self.current_command = ""
            self.using_previous_commands = False
            self.command_index = 0
            self.previous_hotkey = Hotkey(self.game, "up").pressed
            self.next_hotkey = Hotkey(self.game, "down").pressed
        except Exception:
            self.game.log("Failed to initialise debug console object")

    def activate(self):
        """Marks console as active."""
        self.active = True
        self.focused = True
        self.text_input.enable(self.max_command_length)
        self.text_input.text = self.saved_input

    def deactivate(self):
        """Saves current input and marks console as inactive."""
        self.active = False
        self.saved_input = self.text_input.text
        self.text_input.disable(submit=False)

    def set_command_index(self, command_index):
        self.command_index = command_index
        self.text_input.update_with(previous_input_index=command_index)

    def logic(self):
        # Using previously executed commands
        if self.previous_hotkey():
            if not self.using_previous_commands and self.text_input.inputs:
                self.using_previous_commands = True
                self.current_command = self.text_input.text
                self.set_command_index(0)
            elif self.command_index < len(self.text_input.inputs) - 1:
                self.set_command_index(self.command_index + 1)

        if self.using_previous_commands and self.next_hotkey():
            if self.command_index == 0:
                self.using_previous_commands = False
                self.text_input.update_with(self.current_command)
            else:
                self.set_command_index(self.command_index - 1)

        # Executing commands
        if self.active and not self.text_input.accepting_text:
            command = self.text_input.most_recent()
            try:
                self.output = self.font.render(str(eval(command)), True,
                                               self.default_output_colour)
            except SyntaxError:
                try:
                    exec(command)
                except Exception as error:
                    self.output = self.font.render(str(error), True,
                                                   self.error_output_colour)

            self.output_start_frame = self.game.frame
            self.text_input.enable(self.max_command_length)
            self.using_previous_commands = False

        # Toggling active state
        if self.toggle_active_hotkey():
            if self.active:
                if self.text_input.text[-1] == self.toggle_active_hotkey.im_self.button_name:
                    # Stripping trailing character if there is one
                    # (created by pressing the hotkey to close the console)
                    self.text_input.text = self.text_input.text[:-1]
                self.deactivate()
            else:
                self.activate()

        # Toggling focus state
        if self.active:
            self.text_input.check_focused(
                self.prompt_coordinates[0], self.prompt_coordinates[1],
                self.game.width, self.game.height - self.prompt_coordinates[1]
            )
            if not self.text_input.focused:
                # Hiding the console when it is put out of focus
                self.deactivate()

    def draw(self):
        if self.active:
            self.game.screen.blit(self.prompt, self.prompt_coordinates)
            if not self.text_input.text:
                self.game.screen.blit(self.placeholder_text, self.input_coordinates)
            else:
                self.text_input.display(self.font, self.input_colour, self.input_coordinates)

        if (self.game.frame - self.output_start_frame <
                self.output_display_time * self.game.fps):
            self.game.screen.blit(self.output, self.output_coordinates)
        else:   # Resetting self.output to its default value
            self.output = self.default_output
