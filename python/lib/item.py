class Item(OneImage):
    def __init__(self, name, description, image_name):   #! Add quantity?
        super(Item, self).__init__("".join(("items/", image_name)))
        self.name = name
        self.description = description

    def display(self, coordinates):
        self.load_image()
        screen.blit(self.image, coordinates)

    # Class attributes used in display_info()
    name_font = load_font("fira_sans_regular", 30)
    description_font = load_font("chewy", 20)
    info_text_padding = 5
    info_text_width = 200
    info_border_colour = (102, 51, 0)
    info_background_colour = (182, 155, 76)
    info_text_colour = (0, 0, 0)

    def display_info(self, coordinates):
        description_lines = wrap_text(self.description,
                                      self.description_font,
                                      self.info_text_width)

        description_line_height = self.description_font.size(description_lines[-1])[1]
        info_width = 2*self.info_text_padding + self.info_text_width
        name_height = 2*self.info_text_padding + self.name_font.size(self.name)[1]
        description_height = (2*self.info_text_padding
                              + len(description_lines) * description_line_height)

        name_rect = pygame.Rect(coordinates, (info_width, name_height))
        description_rect = pygame.Rect((coordinates[0], coordinates[1] + name_height),
                                       (info_width, description_height))

        pygame.draw.rect(screen, self.info_background_colour, name_rect)
        pygame.draw.rect(screen, self.info_border_colour, name_rect, 1)
        pygame.draw.rect(screen, self.info_background_colour, description_rect)
        pygame.draw.rect(screen, self.info_border_colour, description_rect, 1)

        screen.blit(self.name_font.render(self.name, True, self.info_text_colour),
                    (coordinates[0] + self.info_text_padding,
                     coordinates[1] + self.info_text_padding))

        for index in range(len(description_lines)):
            screen.blit(self.description_font.render(description_lines[index],
                                                     True,
                                                     self.info_text_colour),
                        (coordinates[0] + self.info_text_padding,
                         coordinates[1]
                         + name_height
                         + self.info_text_padding
                         + index * description_line_height))
