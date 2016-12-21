class Hotkey(object):
    def __init__(self, game, button_name, ctrl=False, shift=False, alt=False):
        self.game = game
        try:
            self.button_name = button_name
            self.ctrl = ctrl
            self.shift = shift
            self.alt = alt
        except Exception as self.game.error:
            self.game.log("Failed to initialise hotkey object")

    def pressed(self):
        """Returns True if the hotkey was just pressed."""
        return (self.button_pressed() and
                self.ctrl_satisfied() and
                self.shift_satisfied() and
                self.alt_satisfied())

    def held(self):
        """Returns True if the hotkey is held."""
        return (self.button_held() and
                self.ctrl_satisfied() and
                self.shift_satisfied() and
                self.alt_satisfied())

    def released(self):
        """Returns True if the hotkey was just released."""
        return (self.button_released() and
                self.ctrl_satisfied() and
                self.shift_satisfied() and
                self.alt_satisfied())

    def button_pressed(self):
        return self.game.input.buttons[self.button_name].pressed

    def button_held(self):
        return self.game.input.buttons[self.button_name].held

    def button_released(self):
        return self.game.input.buttons[self.button_name].released

    def ctrl_satisfied(self):
        return self.ctrl == (
            (self.game.input.buttons["leftctrl"].held and
             self.game.input.buttons["leftctrl"].time_held() >
             self.game.input.buttons[self.button_name].time_held()) or
            (self.game.input.buttons["rightctrl"].held and
             self.game.input.buttons["rightctrl"].time_held() >
             self.game.input.buttons[self.button_name].time_held())
        )

    def shift_satisfied(self):
        return self.shift == (
            (self.game.input.buttons["leftshift"].held and
             self.game.input.buttons["leftshift"].time_held() >
             self.game.input.buttons[self.button_name].time_held()) or
            (self.game.input.buttons["rightshift"].held and
             self.game.input.buttons["rightshift"].time_held() >
             self.game.input.buttons[self.button_name].time_held())
        )

    def alt_satisfied(self):
        return self.alt == (
            self.game.input.buttons["alt"].held and
            self.game.input.buttons["alt"].time_held() >
            self.game.input.buttons[self.button_name].time_held()
        )
