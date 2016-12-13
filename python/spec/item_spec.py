execfile("spec/spec_helper.py")

with description("Item"):
    with it("should initialise"):
        heart = Item(
            "Heart",
            "A lovely heart.",
            "heart"
            )
        expect(heart.name).to(equal("Heart"))
        expect(heart.description).to(equal(["A lovely heart."]))
        expect(heart.image_name).to(equal("items/heart"))
