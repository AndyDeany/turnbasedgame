from one_image import OneImage

class Item(OneImage):
    class_assets_loaded = False
    def __init__(self, game, name, description, image_name):   #! Add quantity?
        super(Item, self).__init__(game, "".join(("items/", image_name)))
        if not self.class_assets_loaded:
            self.load_class_assets()

        self.name = name
        self.description = self.game.helper.wrap_text(description,
                                                      self.description_font,
                                                      self.info_text_width)

    def load_class_assets(self):
        self.game.helper.load_class_assets(self, {
            "name_font": self.game.load_font("fira_sans_regular", 30),
            "description_font": self.game.load_font("chewy", 20)
        })

    def display(self, coordinates):
        self.load_image()
        self.game.screen.blit(self.image, coordinates)

    # Class attributes used in display_info()
    info_text_padding = 5
    info_text_width = 200
    info_border_colour = (102, 51, 0)
    info_background_colour = (182, 155, 76)
    info_text_colour = (0, 0, 0)

    def display_info(self, coordinates):
        """Displays the items name and description at the given coordinates"""
        info_width = 2*self.info_text_padding + self.info_text_width
        name_height = 2*self.info_text_padding + self.name_font.size(self.name)[1]
        description_line_height = self.description_font.size(self.description[-1])[1]
        description_height = (2*self.info_text_padding
                              + len(self.description) * description_line_height)

        name_rect = self.game.pygame.Rect(coordinates, (info_width, name_height))
        description_rect = self.game.pygame.Rect(
            (coordinates[0], coordinates[1] + name_height),
            (info_width, description_height)
        )

        self.game.pygame.draw.rect(screen, self.info_background_colour, name_rect)
        self.game.pygame.draw.rect(screen, self.info_border_colour, name_rect, 1)
        self.game.pygame.draw.rect(screen, self.info_background_colour, description_rect)
        self.game.pygame.draw.rect(screen, self.info_border_colour, description_rect, 1)

        self.game.screen.blit(
            self.name_font.render(self.name, True, self.info_text_colour),
            (coordinates[0] + self.info_text_padding, coordinates[1] + self.info_text_padding)
        )

        for index in range(len(self.description)):
            self.game.screen.blit(
                self.description_font.render(
                    self.description[index], True, self.info_text_colour
                    ),
                (coordinates[0] + self.info_text_padding,
                 coordinates[1] + name_height
                 + self.info_text_padding + index * description_line_height)
            )
