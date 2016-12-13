class TextInput(object):
    """
    Class for holding all variables and functions to do with receiving
    text input from the user
    """

    accepting_text = False  # Showing whether the program is accepting text input from the user
    text = ""               # The input text from the user
    max_characters = 0      # The maximum amount of allowed characters in an input text
    destination = ""

    @classmethod
    def take_input(self, max_characters, destination):
        """
        Enables text input to be taken from the user and puts it in
        a variable named after the given "destination" parameter
        """
        # Maybe turn this into a function which creates a text field
        # at given coordinates or something
        self.text = ""
        self.destination = destination
        self.max_characters = max_characters
        self.accepting_text = True

    @classmethod
    def receive_single_characters(self):
        if self.accepting_text:
            if event.key == 8:
                if self.text != "":
                    self.text = self.text[:-1]
            elif event.key == 9:
                #! This (above) is the TAB key. Perhaps it should
                # make the cursor go to the next box and this
                # would be a good place to do it, since it would
                # only be applicable when inputting text.
                # The only reason this would be pointless is if
                # there are never two text boxes to fill in on
                # the same screen, which isn't that unlikely,
                # so it may actually be pointless.
                pass
            elif event.key == 13:
                # This is the enter key. It will cause the text to be accepted.
                self.accepting_text = False
                globals()[self.destination] = self.text
            elif len(self.text) < self.max_characters:
                self.text = "".join((self.text, event.unicode))

    @classmethod
    def return_key(self, n):
        """Returns the keyboard key with key n in pygame.key.get_pressed()"""
        return self.keys[n]
        # self.keys = pygame.key.get_pressed(),
        # which should be assigned before this function is called

    character_keys = (  # A list of all the keys that can produce characters when pressed
        [n for n in range(44, 58)] +
        [n for n in range(96, 123)] +
        [n for n in range(256, 272)] +
        [39, 59, 60, 61, 91, 92, 93]
        )

    @classmethod
    def receive_multiple_characters(self):
        if self.accepting_text and frame % (fps/30) == 0:
                            # This ^^^^^^^^^^^^^^^^^^^^^ means that
                            # characters are written/deleted [30]
                            # times per second when their key is held down,
                            # which feels natural.
            if backspace_held_time > fps/2:
                self.text = self.text[:-1]
            elif (len(self.text) < self.max_characters and
                  # Checking if a key has been held for half a second or longer.
                  max(space_held_time,
                      apostrophe_held_time,
                      comma_held_time,
                      minus_held_time,
                      fullstop_held_time,
                      forwardslash_held_time,
                      zero_held_time,
                      one_held_time,
                      two_held_time,
                      three_held_time,
                      four_held_time,
                      five_held_time,
                      six_held_time,
                      seven_held_time,
                      eight_held_time,
                      nine_held_time,
                      semicolon_held_time,
                      backslash_held_time,
                      equals_held_time,
                      opensquarebracket_held_time,
                      sharp_held_time,
                      closesquarebracket_held_time,
                      backtick_held_time,
                      a_held_time,
                      b_held_time,
                      c_held_time,
                      d_held_time,
                      e_held_time,
                      f_held_time,
                      g_held_time,
                      h_held_time,
                      i_held_time,
                      j_held_time,
                      k_held_time,
                      l_held_time,
                      m_held_time,
                      n_held_time,
                      o_held_time,
                      p_held_time,
                      q_held_time,
                      r_held_time,
                      s_held_time,
                      t_held_time,
                      u_held_time,
                      v_held_time,
                      w_held_time,
                      x_held_time,
                      y_held_time,
                      z_held_time,
                      numpad0_held_time,
                      numpad1_held_time,
                      numpad2_held_time,
                      numpad3_held_time,
                      numpad4_held_time,
                      numpad5_held_time,
                      numpad6_held_time,
                      numpad7_held_time,
                      numpad8_held_time,
                      numpad9_held_time,
                      numpaddivide_held_time,
                      numpadmultiply_held_time,
                      numpadminus_held_time,
                      numpadplus_held_time) > fps/2):
                self.keys = pygame.key.get_pressed()
                # Checking that only one key that provides a character input is pressed.
                if sum(map(self.return_key, self.character_keys)) == 1:
                    self.text = "".join((self.text, self.text[-1]))
