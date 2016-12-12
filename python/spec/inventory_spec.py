execfile("spec/spec_helper.py")

with description("Inventory"):
    with it("should initialise with a default value for size"):
        inventory = Inventory()
        expect(inventory.size).to(equal(25))
        expect(inventory.items).to(equal([None for slot in range(25)]))

    with it("should initialise with a given value for size"):
        inventory = Inventory(20)
        expect(inventory.size).to(equal(20))
        expect(inventory.items).to(equal([None for slot in range(20)]))

    with it("should allow us to add an item"):
        inventory = Inventory()
        heart = Item(
            "Heart",
            "A lovely heart.",
            "heart"
            )
        inventory.add_item(heart)
        expect(inventory.items[0]).to(be(heart))
        expect(inventory.items[1:]).to(equal([None for slot in range(24)]))

    with it("should allow us to remove a given item"):
        inventory = Inventory()
        heart = Item(
            "Heart",
            "A lovely heart.",
            "heart"
            )
        inventory.add_item(heart)
        inventory.remove_item(heart)
        expect(inventory.items).to(equal([None for slot in range(25)]))

    with it("should allow us to remove an item by index"):
        inventory = Inventory()
        heart = Item(
            "Heart",
            "A lovely heart.",
            "heart"
            )
        inventory.add_item(heart)
        inventory.remove_item(0)
        expect(inventory.items).to(equal([None for slot in range(25)]))

    with it("should allow us to swap two items' places"):
        inventory = Inventory()
        heart = Item(
            "Heart",
            "A lovely heart.",
            "heart"
            )
        teddy_bear = Item(
            "Teddy Bear",
            "A cute little teddy bear who loves lollipops... "
            "and hugs.",
            "teddy_bear"
            )
        inventory.add_item(heart)
        inventory.add_item(teddy_bear)
        inventory.swap_items(0, 1)
        expect(inventory.items[0]).to(be(teddy_bear))
        expect(inventory.items[1]).to(be(heart))
