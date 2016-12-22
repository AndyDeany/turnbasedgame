from spec.spec_helper import *

from lib.one_image import OneImage

with description("OneImage"):
    with it("should initialise"):
        one_image = OneImage(game, "items/heart")
        expect(one_image.image_name).to(equal("items/heart"))
        expect(one_image.image).to(be(None))

    with it("should load its image"):
        one_image = OneImage(game, "items/heart")
        one_image.load_image()
        expect(one_image.image).to(be_a(game.pygame.Surface))

    with it("should unload its image"):
        one_image = OneImage(game, "items/heart")
        one_image.load_image()
        one_image.unload_image()
        expect(one_image.image).to(be(None))
