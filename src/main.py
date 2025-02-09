import pygame
from player import Player
from utilities import load_level_from_csv, generate_blocks_from_map
from game_obj import blocks, players

pygame.init()

# Screen setup
screen = pygame.display.set_mode([500, 500])
clock = pygame.time.Clock()

# Load the world map and generate blocks
worldmap = load_level_from_csv('../assets/map.csv')
generate_blocks_from_map(worldmap)

# Create player
player = Player(50, 100)

#jacky is a mug

done = False
while not done:
    blocks.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    # Rendering
    screen.fill([200, 10, 205])
    blocks.draw(screen)
    players.draw(screen)
    player.update()
    player.jump()
    pygame.display.flip()

pygame.quit()
