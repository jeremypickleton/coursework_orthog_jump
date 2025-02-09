import pygame
import sys
from player import Player
from utilities import load_level_from_csv, generate_blocks_from_map
from game_obj import blocks, players, spikes, ends

pygame.init()

screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption('Orthogonal Jump')

TEXT_COLOUR = (255, 255, 255)
BUTTON_COLOUR = (200, 150, 255)

font = pygame.font.SysFont("Papyrus", 48)

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
    
    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOUR, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOUR)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))
    
    def is_pressed(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()


def start_game():
    blocks.empty()  
    spikes.empty()
    players.empty()  

    worldmap = load_level_from_csv('../assets/map.csv')
    generate_blocks_from_map(worldmap)

    player = Player(50, 100)

    game_loop(player)


def game_loop(player):
    clock = pygame.time.Clock()

    done = False
    while not done:

        if player.finished: 
            finish_screen()
            
        blocks.update()
        spikes.update()
        ends.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill([200, 100, 235])
        blocks.draw(screen)
        spikes.draw(screen)
        players.draw(screen)
        ends.draw(screen)
        player.update()
        player.jump()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def menu_screen():
    start_button = Button("Start Game", 120, 200, 300, 90, start_game)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if start_button.rect.collidepoint(event.pos):
                        start_button.is_pressed(event.pos)

        screen.fill([10, 75, 200])  
        start_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def finish_screen():
    start_button = Button("game finished!", 120, 200, 300, 90, None)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if start_button.rect.collidepoint(event.pos):
                        start_button.is_pressed(event.pos)

        screen.fill([10, 75, 200])  
        start_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu_screen()
