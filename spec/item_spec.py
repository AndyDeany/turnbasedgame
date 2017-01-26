from spec.spec_helper import *

from lib.item import Item

with description("Item"):
    with it("should initialise"):
        heart = Item(
            game,
            "Heart",
            "A lovely heart.",
            "heart"
            )
        expect(heart.name).to(equal("Heart"))
        expect(heart.info).to(be_a(game.pygame.Surface))
        expect(heart.image_name).to(equal("items/heart"))
