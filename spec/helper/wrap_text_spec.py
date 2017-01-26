execfile("spec/spec_helper.py")

with description("wrap_text()"):
    with before.all:
        global font
        font = game.load_font("chewy", 20)

    with it("should wrap valid text correctly"):
        text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Aliquam faucibus magna arcu, nec finibus lectus gravida "
                "ultrices. Nam non nibh tellus. Pellentesque molestie "
                "sagittis mi eget interdum. Vivamus semper metus vestibulum "
                "metus interdum porttitor. Phasellus suscipit enim at "
                "sollicitudin luctus. Nam ultrices quis leo a faucibus. "
                "Mauris porta nibh ultrices quam bibendum, sed cursus velit "
                "elementum. Etiam ultrices molestie sem vitae accumsan. "
                "Maecenas dictum gravida nulla non blandit.")
        lines = game.helper.wrap_text(text, font, 200)
        for index in range(len(lines)):
            line = lines[index]
            expect(font.size(line)[0]).to(be_below_or_equal(200))   # Line not too long
            if not index + 1 == len(lines):
                next_word = lines[index+1].split()[0]
                expect(font.size(" ".join((line, next_word)))).to(be_above(200))    # Line not too short

    with it("should create a forced newline wherever \\n is present in the text"):
        text = "Lorem\nipsum\ndolor\nsit\namet."
        lines = game.helper.wrap_text(text, font, 200)
        expect(lines).to(equal(["Lorem", "ipsum", "dolor", "sit", "amet."]))

    with it("should raise an error if the first word is too long to wrap"):
        text = "Supercalifragilisticexpialidocious."

        def use_invalid_text():
            game.helper.wrap_text(text, font, 200)
        expect(use_invalid_text).to(raise_error(ValueError))

    with it("should raise an error if a word in the middle is too long to wrap"):
        text = "I am feeling supercalifragilisticexpialidocious today!"

        def use_invalid_text():
            game.helper.wrap_text(text, font, 200)
        expect(use_invalid_text).to(raise_error(ValueError))
