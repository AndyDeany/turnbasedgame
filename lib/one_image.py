class OneImage(object):
    """An abstract class for objects that have a single image"""
    def __init__(self, game, image_name):
        self.game = game
        self.image_name = image_name
        self.image = None

    def load_image(self):
        if self.image is None:
            self.image = self.game.load_image(self.image_name)

    def unload_image(self):
        self.image = None
