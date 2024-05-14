import pygame, sys, time
from settings import *


# basic OOP set up with the game class


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Brick Breaker Simulator 3034")
        self.background = self.create_background()

    # add background
    def create_background(self):
        background_original = pygame.image.load("graphics/other/bg.png").convert()
        new_background_ratio = WINDOW_HEIGHT / background_original.get_height()
        print(new_background_ratio)
        scaled_width = background_original.get_width() * new_background_ratio
        scaled_height = background_original.get_height() * new_background_ratio
        scaled_background = pygame.transform.scale(
            background_original,
            (scaled_width, scaled_height),
        )
        return scaled_background

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.blit(self.background, (0, 0))

            # update window
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
