import pygame, sys, time
from settings import *

player_width = WINDOW_WIDTH // 10
player_height = WINDOW_HEIGHT // 20


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # set up
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill("teal")

        # position
        self.rect = self.image.get_rect(
            midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)
        )
        # for input
        self.direction = pygame.math.Vector2()
        # for update
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT or pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT or pygame.K_a]:
            self.direction.x = -1
        # idk if this else is nessesary
        else:
            self.direction.x = 0

    def player_constraint(self):
        # left to right
        if self.pos.x <= -(player_width):
            self.pos.x += WINDOW_WIDTH + (player_width)
        # right to left
        if self.pos.x >= WINDOW_WIDTH:
            self.pos.x = -(player_width)

    def update(self, dt):
        self.input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        # print(self.pos.x) # only needed for testing
