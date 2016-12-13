execfile("spec/spec_helper.py")

with description("wrap_text()"):
    with it("should wrap text correctly"):
        font = load_font("chewy", 20)
        text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Aliquam faucibus magna arcu, nec finibus lectus gravida "
                "ultrices. Nam non nibh tellus. Pellentesque molestie "
                "sagittis mi eget interdum. Vivamus semper metus vestibulum "
                "metus interdum porttitor. Phasellus suscipit enim at "
                "sollicitudin luctus. Nam ultrices quis leo a faucibus. "
                "Mauris porta nibh ultrices quam bibendum, sed cursus velit "
                "elementum. Etiam ultrices molestie sem vitae accumsan. "
                "Maecenas dictum gravida nulla non blandit.")
        lines = wrap_text(text, font, 200)

        for line in lines:
            expect(font.size(line)[0]).to(be_below_or_equal(200))

        expect(" ".join(lines)).to(equal(text))

    with it("should create a forced newline wherever \\n is present in the text"):
        font = load_font("chewy", 20)
        text = ("Lorem \n ipsum \n dolor \n sit \n amet.")
        lines = wrap_text(text, font, 200)
        expect(lines).to(equal(["Lorem", "ipsum", "dolor", "sit", "amet."]))

    with it("should raise an error if a word is too long to wrap"):
        font = load_font("chewy", 20)
        text = ("Supercalifragilisticexpialidocious.")
        def give_invalid_text():
            wrap_text(text, font, 200)
        expect(give_invalid_text).to(raise_error(ValueError))
