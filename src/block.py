import pygame
from game_obj import GameObj, blocks, spikes, ends, ships


class Block(GameObj):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().update()
        self.image = pygame.Surface([50, 50])
        self.image.fill([10, 20, 30])
        blocks.add(self)


class Spike(GameObj):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().update()
        self.image = pygame.Surface([50, 50])
        self.image.fill([250, 0, 0])
        spikes.add(self)


class Ship(GameObj):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().update()
        self.image = pygame.Surface([50, 50])
        self.image.fill([0, 0, 250])
        ships.add(self)


class End(GameObj):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().update()
        self.image = pygame.Surface([50, 50])
        self.image.fill([0, 255, 0])
        ends.add(self)
