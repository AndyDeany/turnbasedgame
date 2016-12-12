execfile("spec/spec_helper.py")

with description("OneImage"):
    with it("should initialise"):
        one_image = OneImage("heart")
        expect(one_image.image_name).to(equal("heart"))
        expect(one_image.image).to(be(None))

    with it("should load its image"):
        one_image = OneImage("heart")
        one_image.load_image()
        expect(one_image.image).to(be_a(pygame.Surface))

    with it("should unload its image"):
        one_image = OneImage("heart")
        one_image.load_image()
        one_image.unload_image()
        expect(one_image.image).to(be(None))
