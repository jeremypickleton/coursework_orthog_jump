import pygame
import sys
from player import Player
from utilities import load_level_from_csv, generate_blocks_from_map
from game_obj import blocks, players, spikes, ends, ships, balls
from background import Background

background = Background()

pygame.init()
screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption("Orthogonal Jump")

TEXT_COLOUR = (255, 255, 255)
BUTTON_COLOUR = (200, 150, 255)

font = pygame.font.SysFont("Papyrus", 35)


class FlashingBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.color1 = (0, 0, 255)  # Blue
        self.color2 = (255, 0, 0)  # Red
        self.flash_interval = 500  # Interval in milliseconds
        self.last_flash_time = 0  # Time when the color was last changed

    def update(self):
        current_time = pygame.time.get_ticks()
        # Change color every 'flash_interval' milliseconds
        if current_time - self.last_flash_time > self.flash_interval:
            # Toggle between color1 and color2
            if self.surface.get_at((0, 0)) == pygame.Color(
                self.color1[0], self.color1[1], self.color1[2]
            ):
                self.surface.fill(self.color2)
            else:
                self.surface.fill(self.color1)
            self.last_flash_time = current_time  # Update the last flash time

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))


class Button:
    def __init__(self, text, x, y, width, height, action=None, params=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.params = params or []

    def draw(self, surface, size):
        pygame.draw.rect(surface, BUTTON_COLOUR, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOUR)
        if size == "L":
            surface.blit(text_surf, (self.rect.x + 60, self.rect.y + 20))
        else:
            surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def is_pressed(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action(*self.params)


def start_game(level):
    # Reset all game objects for a fresh start
    blocks.empty()
    spikes.empty()
    ships.empty()
    players.empty()
    balls.empty()
    ends.empty()

    # Load the level map
    if level == 1:
        worldmap = load_level_from_csv("./assets/map1.csv")
    elif level == 2:
        worldmap = load_level_from_csv("./assets/map2.csv")
    generate_blocks_from_map(worldmap)

    # Create a player and set the current level
    player = Player(50, 50)
    player.level = level

    game_loop(player)


def game_loop(player):
    clock = pygame.time.Clock()
    background = FlashingBackground(screen.get_width(), screen.get_height())

    done = False
    while not done:
        dt = clock.tick(60)  # Get delta time in milliseconds
        dt = dt / 1000.0  # Convert to seconds

        background.update()  # Update the background with delta time

        if player.finished:
            finish_screen()

        blocks.update()
        spikes.update()
        ships.update()
        ends.update()
        balls.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        background.draw(screen)  # Draw the dynamic background

        # Draw the rest of the game objects
        blocks.draw(screen)
        spikes.draw(screen)
        ships.draw(screen)
        players.draw(screen)
        ends.draw(screen)
        balls.draw(screen)

        player.update()
        player.jump()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def menu_screen():
    # Main menu setup
    start_button = Button("Start Game", 120, 200, 300, 90, level_menu)
    leaderboard_menu = Button("Leaderboard", 170, 300, 220, 70, leaderboard_menu_screen)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.rect.collidepoint(event.pos):
                        start_button.is_pressed(event.pos)
                    if leaderboard_menu.rect.collidepoint(event.pos):
                        leaderboard_menu.is_pressed(event.pos)

        screen.fill([10, 75, 200])
        start_button.draw(screen, "L")
        leaderboard_menu.draw(screen, "S")

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def level_menu():
    # Level selection menu setup
    level1 = Button("Level 1", 120, 200, 300, 90, start_game, params=[1])
    level2 = Button("Level 2", 120, 300, 300, 90, start_game, params=[2])

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if level1.rect.collidepoint(event.pos):
                        level1.is_pressed(event.pos)
                    if level2.rect.collidepoint(event.pos):
                        level2.is_pressed(event.pos)

        screen.fill([10, 75, 200])
        level1.draw(screen, "L")
        level2.draw(screen, "L")

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def leaderboard_menu_screen():
    # Leaderboard screen setup
    blocks.empty()
    spikes.empty()
    ships.empty()
    balls.empty()
    players.empty()
    ends.empty()
    menu_button = Button("Main Menu", 170, 50, 200, 70, menu_screen)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_button.rect.collidepoint(event.pos):
                        menu_button.is_pressed(event.pos)

        screen.fill([10, 75, 200])
        menu_button.draw(screen, "S")

        data = load_level_from_csv("./assets/leaderboard.csv")
        cell_width = 100
        cell_height = 40
        padding = 5
        font = pygame.font.Font(None, 20)
        for row_index, row in enumerate(data):
            for col_index, cell in enumerate(row):
                text_surface = font.render(cell, True, (0, 0, 0))
                x = 120 + col_index * cell_width + padding
                y = 170 + row_index * cell_height + padding
                screen.blit(text_surface, (x, y))

                pygame.draw.rect(
                    screen,
                    (250, 0, 0),
                    (x - padding, y - padding, cell_width, cell_height),
                    2,
                )
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def finish_screen():
    # Display the finish screen when the game ends
    blocks.empty()
    spikes.empty()
    ships.empty()
    players.empty()
    balls.empty()
    ends.empty()
    start_button = Button("Game finished!", 120, 50, 300, 90, menu_screen)

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
        start_button.draw(screen, "L")

        data = load_level_from_csv("./assets/leaderboard.csv")
        cell_width = 100
        cell_height = 40
        padding = 5
        font = pygame.font.Font(None, 20)
        for row_index, row in enumerate(data):
            for col_index, cell in enumerate(row):
                text_surface = font.render(cell, True, (0, 0, 0))
                x = 120 + col_index * cell_width + padding
                y = 170 + row_index * cell_height + padding
                screen.blit(text_surface, (x, y))

                pygame.draw.rect(
                    screen,
                    (250, 0, 0),
                    (x - padding, y - padding, cell_width, cell_height),
                    2,
                )
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    menu_screen()
