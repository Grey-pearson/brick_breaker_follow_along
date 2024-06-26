import pygame, sys, time
from settings import *
from sprites import Player, Ball, Block


# basic OOP set up with the game class


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Brick Breaker Simulator 3034")
        self.background = self.create_background()
        # group set up 4 sprites
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()

        self.player = Player(self.all_sprites)
        self.screen_setup()
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites)

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

    def screen_setup(self):
        # loop through all rows and cols of block map
        # find x and y position for all blocks
        for row_index, row in enumerate(BLOCK_MAP):
            for col_index, col in enumerate(row):
                if col != " ":
                    # to center block on Y axis
                    y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    # center blocks on X axis
                    x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    # print(f"{y} | {x}")
                    Block(col, (x, y), [self.all_sprites, self.block_sprites])

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

            # updating game
            self.all_sprites.update(dt)
            self.player.player_constraint()

            self.display_surface.blit(self.background, (0, 0))
            # this is needed to draw sprite to screen frfr
            self.all_sprites.draw(self.display_surface)
            # update window
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
