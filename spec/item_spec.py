from spec.spec_helper import *

from lib.inventory import Inventory
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
        expect(heart.description).to(equal(["A lovely heart."]))
        expect(heart.image_name).to(equal("items/heart"))
