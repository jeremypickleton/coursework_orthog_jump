import pygame
from game_obj import GameObj, blocks, players, spikes, ends, ships, balls
from utilities import (
    load_level_from_csv,
    generate_blocks_from_map,
    write_to_csv,
    get_last_attempt_num,
)


class Particle:
    def __init__(self, x, y):
        self.size = 5
        self.x = x
        self.y = y
        self.color = (255, 165, 0)
        self.dx = -2
        self.dy = 0
        self.lifespan = 30

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.size -= 0.1
        self.lifespan -= 1

    def is_alive(self):
        return self.lifespan > 0 and self.size > 0

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), int(self.size)
        )


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("./assets/player_texture.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.dx, self.dy = 0, 0
        self.falling = True
        self.blockmove = False
        self.finished = False
        self.level = 0
        self.flight_mode = False
        self.gravity = True
        self.gravity_up = False

        self.particles = []

        players.add(self)

    def jump(self):
        keys = pygame.key.get_pressed()

        if self.flight_mode:
            self.handle_flight(keys)
        else:
            self.handle_normal_jump(keys)

        self.handle_gravity(keys)

        self.handle_block_collision()
        self.handle_ship_collision()
        self.handle_gravity_switch()
        self.handle_falling_collision()
        self.handle_spike_collision()
        self.handle_finish_collision()

        # Update particles
        self.update_particles()

    def handle_flight(self, keys):
        if keys[pygame.K_UP]:
            self.dy -= 0.535
        elif keys[pygame.K_DOWN]:
            self.dy = 5
        else:
            self.dy += 0.3

        if keys[pygame.K_RIGHT]:
            self.dx += 2
        elif keys[pygame.K_LEFT]:
            self.dx -= 2

        self.blockmove = keys[pygame.K_LEFT]
        self.dx *= 0.7
        self.rect.x += int(self.dx)

        # Generate particles behind the player
        self.generate_particles()

    def handle_normal_jump(self, keys):
        if self.falling:
            self.dy = min(self.dy + 0.5, 10)
        else:
            self.dy = 0

        if self.gravity_up:
            self.dy = min(self.dy - 1.5, 0.5)

        if keys[pygame.K_RIGHT]:
            self.dx += 2
        elif keys[pygame.K_LEFT]:
            self.dx -= 2

        if keys[pygame.K_UP] and not self.falling:
            self.dy -= 10
            self.falling = True

        self.blockmove = keys[pygame.K_LEFT]
        self.dx *= 0.7
        self.rect.x += int(self.dx)

    def handle_gravity(self, keys):
        if not self.gravity:

            if keys[pygame.K_UP]:
                # print("Gravity disabled", self.dy)
                self.dy += 5
                self.gravity_up = True
            self.dy -= 0.5

    def handle_block_collision(self):
        touched_blocks = pygame.sprite.spritecollide(self, blocks, False)
        if touched_blocks:
            block = touched_blocks[0]
            if self.rect.right > block.rect.left and self.rect.left < block.rect.left:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

    def handle_ship_collision(self):
        if pygame.sprite.spritecollide(self, ships, False):
            self.flight_mode = True

    def handle_gravity_switch(self):
        if pygame.sprite.spritecollide(self, balls, False):
            self.gravity = False

    def handle_falling_collision(self):
        self.rect.y += int(self.dy)
        touched_blocks = pygame.sprite.spritecollide(self, blocks, False)
        if touched_blocks:
            block = touched_blocks[0]
            if self.rect.bottom > block.rect.top and self.rect.top < block.rect.top:
                self.rect.bottom = block.rect.top
                self.falling = False
            else:
                self.rect.top = block.rect.bottom
                self.dy = 0
        else:
            self.falling = True

    def handle_spike_collision(self):
        if pygame.sprite.spritecollide(self, spikes, False):
            self.crash()

    def handle_finish_collision(self):
        if pygame.sprite.spritecollide(self, ends, False):
            self.finished = True
            attempt = int(get_last_attempt_num()[1]) + 1
            data = ["Felix", str(attempt), str(self.level)]

            if attempt <= 7:
                write_to_csv("./assets/leaderboard.csv", data)

    def crash(self):
        blocks.empty()
        spikes.empty()
        ends.empty()
        balls.empty()
        ships.empty()

        self.rect.x, self.rect.y = 50, 100
        self.gravity = True
        self.gravity_up = False
        map_file = f"./assets/map{self.level}.csv"
        print(map_file)
        worldmap = load_level_from_csv(map_file)
        generate_blocks_from_map(worldmap)

    def generate_particles(self):
        print("Generating particles")
        # Generate particles behind the player when in flight mode
        particle_x = self.rect.x + self.rect.width // 2
        particle_y = self.rect.y + self.rect.height
        self.particles.append(Particle(particle_x, particle_y))

    def update_particles(self):
        # Update and draw particles
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, screen):
        # Draw player
        screen.blit(self.image, self.rect)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
