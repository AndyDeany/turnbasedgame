class Inventory(object):
    """Class for player's inventories"""
    def __init__(self, size=25):     #! Maybe have predetermined size
        """Size should be a multiple of 5"""
        self.size = size
        self.items = [None for slot in range(size)]

    def add_item(self, item):
        """item should be an Item object"""
        for index in range(self.size):
            if self.items[index] is None:
                self.items[index] = item
                break

    def remove_item(self, item_or_index):   #! add quantity? items would need a quantity attribute.
        """Can be passed an item or its index"""
        if isinstance(item_or_index, Item):
            item_or_index = self.items.index(item_or_index)
        self.items[item_or_index] = None

    def swap_items(self, index1, index2):
        """Swaps the items with the given indexes"""
        temp = self.items[index1]
        self.items[index1] = self.items[index2]
        self.items[index2] = temp

    def display(self, coordinates):
        inventory_padding = 10
        item_padding = 5
        item_image_side_length = 50
        for index in range(size):
            x = (coordinates[0] + inventory_padding +
                 (item_image_side_length + item_padding)*(index % 5))
            y = (coordinates[1] + inventory_padding +
                 (item_image_side_length + item_padding)*(index / 5))
            self.items[index].display((x, y))
