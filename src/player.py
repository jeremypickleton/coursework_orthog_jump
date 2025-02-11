import pygame
from game_obj import GameObj, blocks, players, spikes, ends
from utilities import load_level_from_csv, generate_blocks_from_map

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([45, 45])
        self.image.fill([150, 125, 90])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.falling = True
        self.dx = 0
        self.dy = 0
        self.blockmove = False
        self.finished = False
        self.level = 0

        players.add(self)
   
    def jump(self):
        if self.falling:
            self.dy += 0.5
            if self.dy > 10:
                self.dy = 10
        else:
            self.dy = 0

        keys = pygame.key.get_pressed()
 
        if keys[pygame.K_RIGHT]:
            self.dx += 2 
        elif keys[pygame.K_LEFT]:
            self.dx -= 2

        if keys[pygame.K_UP] and not self.falling:
            self.dy -= 10
            self.falling = True
            
        if keys[pygame.K_LEFT]:
            self.blockmove = True
        else:
            self.blockmove = False
        self.dx = self.dx * 0.7

        self.rect.x += int(self.dx)
        touched = pygame.sprite.spritecollide(self, blocks, False)
        
        if touched:
            block = touched[0]
            if self.rect.right > block.rect.left and self.rect.left < block.rect.left:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += int(self.dy)
        touched = pygame.sprite.spritecollide(self, blocks, False)
        if touched:
            block = touched[0]
            if self.rect.bottom > block.rect.top and self.rect.top < block.rect.top:
                self.rect.bottom = block.rect.top
                self.falling = False
            else:
                self.rect.top = block.rect.bottom
                self.dy = 0
        else:
            self.falling = True   

        crashed = pygame.sprite.spritecollide(self, spikes, False) 
        if crashed:
            self.crash()
        finished = pygame.sprite.spritecollide(self, ends, False)
        if finished:
            self.finished = True
           
    def crash(self):
        print("You crashed into a spike!")
        blocks.empty()  
        spikes.empty()
        ends.empty()
        self.rect.x = 50
        self.rect.y = 100
        map_file = './assets/map' + str(self.level) + '.csv'
        print("map")
        print(map_file)
        worldmap = load_level_from_csv(map_file)
        generate_blocks_from_map(worldmap)


        
    


     




