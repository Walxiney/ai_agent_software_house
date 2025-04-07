import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FPS = 15
PELLET_SCORE = 10
GHOST_SCORE = 50
NUM_LIVES = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game States
RUNNING = 0
GAME_OVER = 1

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PacMan(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score = 0
        self.lives = NUM_LIVES

    def move(self, direction):
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x, self.y = new_x, new_y

class Ghost(Entity):
    def move(self, pacman_position):
        # Simple AI to chase Pac-Man
        if pacman_position[0] > self.x:
            self.x += 1
        elif pacman_position[0] < self.x:
            self.x -= 1
        if pacman_position[1] > self.y:
            self.y += 1
        elif pacman_position[1] < self.y:
            self.y -= 1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pac-Man')
        self.clock = pygame.time.Clock()
        self.state = RUNNING
        self.pacman = PacMan(GRID_SIZE // 2, GRID_SIZE // 2)
        self.ghosts = [Ghost(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)) for _ in range(3)]
        self.pellets = [(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)) for _ in range(20)]

    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

    def draw_entities(self):
        # Draw Pac-Man
        pacman_rect = pygame.Rect(self.pacman.x * CELL_SIZE, self.pacman.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, YELLOW, pacman_rect)

        # Draw Ghosts
        for ghost in self.ghosts:
            ghost_rect = pygame.Rect(ghost.x * CELL_SIZE, ghost.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, RED, ghost_rect)

        # Draw Pellets
        for pellet in self.pellets:
            pellet_rect = pygame.Rect(pellet[0] * CELL_SIZE + CELL_SIZE // 4, pellet[1] * CELL_SIZE + CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2)
            pygame.draw.circle(self.screen, BLUE, pellet_rect.topleft, CELL_SIZE // 4)

    def check_collisions(self):
        # Check pellet collection
        if (self.pacman.x, self.pacman.y) in self.pellets:
            self.pellets.remove((self.pacman.x, self.pacman.y))
            self.pacman.score += PELLET_SCORE

        # Check ghost collisions
        for ghost in self.ghosts:
            if self.pacman.x == ghost.x and self.pacman.y == ghost.y:
                self.pacman.lives -= 1
                if self.pacman.lives <= 0:
                    self.state = GAME_OVER

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.pacman.score} Lives: {self.pacman.lives}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.pacman.move(UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.move(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.move(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.move(RIGHT)

            if self.state == RUNNING:
                self.screen.fill(BLACK)
                self.draw_grid()
                self.check_collisions()
                self.display_score()

                for ghost in self.ghosts:
                    ghost.move((self.pacman.x, self.pacman.y))

                self.draw_entities()
            else:
                # Game over state
                font = pygame.font.Font(None, 74)
                game_over_text = font.render('Game Over', True, WHITE)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    Game().run()