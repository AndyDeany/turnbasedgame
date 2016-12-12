class Item(OneImage):
    def __init__(self, name, description, image_name):   #! Add quantity?
        super(Item, self).__init__(image_name)
        self.name = name
        self.description = description

    def display(self, coordinates):
        self.load_image()
        screen.blit(self.image, coordinates)
