from item import Item

class Inventory(object):
    """Class for player's inventories"""
    class_assets_loaded = False

    def __init__(self, game, size=25):     #! Maybe have predetermined size
        """Size should be a multiple of 5"""
        self.game = game
        if not self.class_assets_loaded:
            self.load_class_assets()

        self.size = size
        self.items = [None for slot in range(size)]

    def load_class_assets(self):
        self.game.helper.load_class_assets(self, {
            "top_row_image": self.game.load_image("inventory_top"),
            "middle_row_image": self.game.load_image("inventory_middle"),
            "bottom_row_image": self.game.load_image("inventory_bottom"),
            "bottom_row_small_image": self.game.load_image("inventory_bottom_small"),
            "empty_slot_image": self.game.load_image("empty_inventory_slot")
        })

    def add_item(self, item):
        """item should be an Item object"""
        for index in range(self.size):
            if self.items[index] is None:
                self.items[index] = item
                break

    def remove_item(self, item_or_index):   #! add quantity? items would need a quantity attribute.
        """Can be passed an item or its index"""
        if isinstance(item_or_index, Item):
            # Add code for checking if the item is in the inventory here, and
            # Raise an error, or show a message if it's not. Or return something.
            item_or_index = self.items.index(item_or_index)
        self.items[item_or_index] = None

    def swap_items(self, index1, index2):
        """Swaps the items with the given indexes"""
        temp = self.items[index1]
        self.items[index1] = self.items[index2]
        self.items[index2] = temp

    # Class attributes used in self.display()
    inventory_padding = 15
    item_padding = 5
    item_image_side_length = 50

    screen_side_info_padding = 30   # Pixels between edge of screen and info
    # box if player has info boxes configured to show at the side of the screen

    def display(self, coordinates):
        self.game.screen.blit(self.top_row_image, coordinates)
        if self.size <= 5:
            self.game.screen.blit(self.bottom_row_small_image,
                                  (coordinates[0],
                                   coordinates[1]
                                   + self.inventory_padding
                                   + self.item_padding
                                   + self.item_image_side_length))
        else:
            number_of_extra_rows = (self.size - 1)/5
            for row in range(1, number_of_extra_rows):
                self.game.screen.blit(self.middle_row_image,
                                      (coordinates[0],
                                       coordinates[1]
                                       + self.inventory_padding
                                       + row * (self.item_padding
                                                + self.item_image_side_length)))
            self.game.screen.blit(self.bottom_row_image,
                                  (coordinates[0],
                                   coordinates[1]
                                   + self.inventory_padding
                                   + number_of_extra_rows * (self.item_padding
                                                             + self.item_image_side_length)))

        item_to_show_info_of = None
        for index in range(self.size):
            x = (coordinates[0] + self.inventory_padding +
                 (self.item_image_side_length + self.item_padding)*(index % 5))
            y = (coordinates[1] + self.inventory_padding +
                 (self.item_image_side_length + self.item_padding)*(index / 5))
            self.game.screen.blit(self.empty_slot_image, (x, y))
            if self.items[index] is not None:
                self.items[index].display((x, y))

                # Storing the item to show the info of as info needs to be displayed
                # on top of all of the items (so it needs to be blitted afterwards).
                if self.game.input.mousein(x, y, self.item_image_side_length,
                                           self.item_image_side_length):
                    item_to_show_info_of = self.items[index]
                    if self.game.options["show item info at side"]:
                        item_info_coordinates = (self.game.width
                                                 - Item.info_text_width
                                                 - self.screen_side_info_padding,
                                                 self.game.height/3)
                    else:
                        item_info_coordinates = (
                            x + self.item_image_side_length + self.item_padding, y
                            )

        if item_to_show_info_of is not None:
            item_to_show_info_of.display_info(item_info_coordinates)
