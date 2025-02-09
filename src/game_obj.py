import pygame

# Group to hold all the blocks and players
blocks = pygame.sprite.Group()
players = pygame.sprite.Group()


class GameObj(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill([10, 230, 210])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.dx = 1
        self.rect.y = y

    def update(self):
        self.rect.x -= self.dx
        
class Block(GameObj):
    def __init__(self, x, y):
        super().__init__(x, y)
        super().update()
        self.image = pygame.Surface([50, 50])
        self.image.fill([10, 20, 30])
        blocks.add(self)
