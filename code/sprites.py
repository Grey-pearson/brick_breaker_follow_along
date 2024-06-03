import pygame, sys, time
from random import choice
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
        self.old_rect = self.rect.copy()

        # for input
        self.direction = pygame.math.Vector2()
        # for update
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        # idk if this else is nessesary
        else:
            self.direction.x = 0

    def player_constraint(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    # makes player wrap around the screen, its cool but i prefer full stop
    def player_wrap(self):
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


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, player, blocks):
        super().__init__(groups)
        # ball will need to be active or passive

        # for collisions
        self.player = player
        self.blocks = blocks

        # graphics set up
        self.image = pygame.image.load("graphics/other/ball.png").convert_alpha()
        # position
        self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2((choice((1, -1)), -1))
        self.speed = 400

        # making ball active
        self.active = False

    # space to launch ball
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_SPACE]:
            self.active = True

    def window_collision(self, direction):
        if direction == "horizontal":
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1

            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1
        if direction == "vertical":
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1

            if self.rect.bottom > WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1
                # this is for if i want it to bounce off the bottom, would be useful for screen saver
                # self.rect.bottom = WINDOW_HEIGHT
                # self.pos.y = self.rect.y
                # self.direction.y *= -1

    def collision(self, direction):
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)
        # right and left
        if overlap_sprites:
            if direction == "horizontal":
                for sprite in overlap_sprites:
                    # right of self
                    if (
                        self.rect.right >= sprite.rect.left
                        and self.old_rect.right <= sprite.old_rect.left
                    ):
                        self.rect.right = sprite.rect.left - 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                    # left of self
                    if (
                        self.rect.left <= sprite.rect.right
                        and self.old_rect.left >= sprite.old_rect.right
                    ):
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.y *= -1

                    if getattr(sprite, "health", None):
                        sprite.get_damage(1)

            if direction == "vertical":
                for sprite in overlap_sprites:
                    # top of self
                    if (
                        self.rect.top <= sprite.rect.bottom
                        and self.old_rect.top >= sprite.old_rect.bottom
                    ):
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                    # bottom of self
                    if (
                        self.rect.bottom >= sprite.rect.top
                        and self.old_rect.bottom <= sprite.old_rect.top
                    ):
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

                    if getattr(sprite, "health", None):
                        sprite.get_damage(1)

    def update(self, dt):
        self.input()
        if self.active:
            # normalize direction, make ball go same speed no matter angle
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # create old rect
            self.old_rect = self.rect.copy()

            # horizontal collision
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.pos.x)
            self.collision("horizontal")
            self.window_collision("horizontal")
            self.collision("horizontal")
            # vertiacal collision
            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.pos.y)
            self.collision("vertical")
            self.window_collision("vertical")
            self.collision("vertical")
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)
        # print(self.pos)


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        # damage info
        self.health = int(block_type)

    def get_damage(self, amount):
        self.health -= amount

        if self.health > 0:
            pass
        else:
            self.kill()
