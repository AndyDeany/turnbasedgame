from lib.game import Game

if __name__ == "__main__":
    #! Decide how the window should be when the game opens. (fullscreen/borderless/windowed)?
    # How big should it be? User's monitor dimensions? Something else?
    game = Game((1280, 720))
    game.run()
