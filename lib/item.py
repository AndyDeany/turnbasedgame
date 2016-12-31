from one_image import OneImage

class Item(OneImage):
    class_assets_loaded = False

    def __init__(self, game, name, description, image_name):   #! Add quantity?
        super(Item, self).__init__(game, "".join(("items/", image_name)))
        if not self.class_assets_loaded:
            self.load_class_assets()

        self.name = name
        self.info = self.create_info_surface(description)

    def load_class_assets(self):
        self.game.helper.load_class_assets(self, {
            "name_font": self.game.load_font("fira_sans_regular", 30),
            "description_font": self.game.load_font("chewy", 20)
        })

    # Class attributes used in create_description_surface()
    info_text_padding = 5
    info_text_width = 200
    info_border_width = 1
    info_border_colour = (102, 51, 0)
    info_background_colour = (182, 155, 76)
    info_text_colour = (0, 0, 0)

    def create_info_surface(self, description):
        """Creates a surface showing the name and description of the item."""
        def with_padding(dimension):
            """Adds text padding to a width or height measurement."""
            return 2*self.info_text_padding + dimension

        def draw_border_rect(Rect):
            self.game.pygame.draw.rect(surface, self.info_border_colour,
                                       Rect, self.info_border_width)

        description = self.game.helper.wrap_text(description,
                                                 self.description_font,
                                                 self.info_text_width)

        surface_width = with_padding(self.info_text_width)
        name_height = with_padding(self.name_font.size(self.name)[1])
        description_line_height = self.description_font.size("")[1]
        description_height = with_padding(len(description) * description_line_height)
        surface_height = name_height + description_height

        surface = self.game.pygame.Surface((surface_width, surface_height))

        name_rect = self.game.pygame.Rect((0, 0), (surface_width, name_height))
        description_rect = self.game.pygame.Rect((0, name_height),
                                                 (surface_width, description_height))
        surface.fill(self.info_background_colour)
        draw_border_rect(name_rect)
        draw_border_rect(description_rect)

        surface.blit(self.name_font.render(self.name, True, self.info_text_colour),
                     (self.info_text_padding, self.info_text_padding))

        for index in range(len(description)):
            surface.blit(
                self.description_font.render(description[index], True,
                                             self.info_text_colour),
                (self.info_text_padding,
                 name_height
                 + self.info_text_padding
                 + index * description_line_height)
            )

        return surface

    def display(self, coordinates):
        self.load_image()
        self.game.screen.blit(self.image, coordinates)

    def display_info(self, coordinates):
        """Displays the item's name and description at the given coordinates."""
        self.game.screen.blit(self.info, coordinates)
