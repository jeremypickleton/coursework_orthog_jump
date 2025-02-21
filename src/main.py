import pygame
import sys
from player import Player
from utilities import load_level_from_csv, generate_blocks_from_map
from game_obj import blocks, players, spikes, ends, ships

pygame.init()
print("test")
screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption("Orthogonal Jump")

TEXT_COLOUR = (255, 255, 255)
BUTTON_COLOUR = (200, 150, 255)

font = pygame.font.SysFont("Papyrus", 48)


class Button:
    def __init__(self, text, x, y, width, height, action=None, params=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.params = params or []

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOUR, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOUR)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def is_pressed(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action(*self.params)


def start_game(level):
    print("level")
    print(level)
    blocks.empty()
    spikes.empty()
    ships.empty()
    players.empty()
    ends.empty()

    if level == 1:
        worldmap = load_level_from_csv("./assets/map1.csv")
    elif level == 2:
        worldmap = load_level_from_csv("./assets/map2.csv")
    generate_blocks_from_map(worldmap)

    player = Player(50, 50)
    player.level = level

    game_loop(player)


def game_loop(player):
    clock = pygame.time.Clock()

    done = False
    while not done:

        if player.finished:
            finish_screen()

        blocks.update()
        spikes.update()
        ships.update()
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
        ships.draw(screen)
        players.draw(screen)
        ends.draw(screen)
        player.update()
        player.jump()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def menu_screen():
    start_button = Button("Start Game", 120, 200, 300, 90, start_game, params=[1])
    level2 = Button("Level 2", 120, 300, 300, 90, start_game, params=[2])

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.rect.collidepoint(event.pos):
                        start_button.is_pressed(event.pos)
                    if level2.rect.collidepoint(event.pos):
                        level2.is_pressed(event.pos)

        screen.fill([10, 75, 200])
        start_button.draw(screen)
        level2.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def finish_screen():
    blocks.empty()
    spikes.empty()
    ships.empty()
    players.empty()
    ends.empty()
    start_button = Button("Game finished!", 120, 200, 300, 90, menu_screen)

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
