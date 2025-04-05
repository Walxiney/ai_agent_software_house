import pygame
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE = 30
ROWS = SCREEN_HEIGHT // TILE_SIZE
COLS = SCREEN_WIDTH // TILE_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game state
class GameState:
    def __init__(self):
        self.pacman = PacMan()  # Change to PacMan instance
        self.score = 0
        self.lives = 3
        self.pellets = []
        self.power_pellets = []
        self.ghosts = []
        self.game_over = False
        self.level = 1
        self.initialize_maze()

    def initialize_maze(self):
        self.maze_template = [
            "##############################",
            "#........#........#.........#",
            "#.####.#.###.###.#######.#.#.#",
            "#......#.....#........#.#...#",
            "#.#######.#.#.#.####.###.###.#",
            "#.......#.#.#.#.........#....#",
            "######.###.###.#.##.########.#",
            "#..........#.......#..........#",
            "##############################",
        ]

        for r, row in enumerate(self.maze_template):
            for c, char in enumerate(row):
                if char == '.':
                    self.pellets.append((r, c))
                elif char == '#':
                    pass  # Wall

        self.power_pellets = [(1, 1), (1, COLS - 2), (ROWS - 2, 1), (ROWS - 2, COLS - 2)]
        self.ghosts = [Ghost("Blinky", 1, 0), Ghost("Pinky", 0, -1), Ghost("Inky", 1, 1), Ghost("Clyde", -1, 1)]

class PacMan:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.state = "normal"  # Other states: "power", "dead"

    def move(self, direction, maze_template):
        if direction == "UP" and maze_template[self.y - 1][self.x] != '#':
            self.y -= 1
        elif direction == "DOWN" and maze_template[self.y + 1][self.x] != '#':
            self.y += 1
        elif direction == "LEFT" and maze_template[self.y][self.x - 1] != '#':
            self.x -= 1
        elif direction == "RIGHT" and maze_template[self.y][self.x + 1] != '#':
            self.x += 1

class Ghost:
    def __init__(self, name, move_x, move_y):
        self.name = name
        self.x = random.randint(1, COLS - 2)
        self.y = random.randint(1, ROWS - 2)
        self.move_x = move_x
        self.move_y = move_y
        self.state = "chase"  # Other states: "scatter", "frightened"
        self.scatter_timer = 0
        self.frightened_timer = 0
        self.eaten_count = 0  # Track the number of ghosts eaten

    def move(self, game_state):
        # Ghost movement logic
        if self.state == "chase":
            if self.x < game_state.pacman.x:
                self.x += 1
            elif self.x > game_state.pacman.x:
                self.x -= 1

            if self.y < game_state.pacman.y:
                self.y += 1
            elif self.y > game_state.pacman.y:
                self.y -= 1

        # Implement scatter mode behavior
        if self.state == "scatter":
            self.move_to_corner()

        # Handle frightened mode
        if self.state == "frightened":
            self.frightened_timer += 1
            if self.frightened_timer > 50:  # Example timer for switching back
                self.state = "chase"
                self.frightened_timer = 0

    def move_to_corner(self):
        # Implement behavior for scattering to corners (example logic)
        corners = [(1, 1), (1, COLS - 2), (ROWS - 2, 1), (ROWS - 2, COLS - 2)]
        target = (self.x, self.y)  # Start at current position
        if (self.x, self.y) not in corners:
            corner = min(corners, key=lambda c: ((self.x-c[0]) ** 2 + (self.y-c[1]) ** 2) ** 0.5)  # Nearest corner
            if self.x < corner[1]:
                self.x += 1
            elif self.x > corner[1]:
                self.x -= 1
            elif self.y < corner[0]:
                self.y += 1
            elif self.y > corner[0]:
                self.y -= 1

def draw_game(screen, game_state):
    screen.fill(BLACK)
    for pellet in game_state.pellets:
        pygame.draw.circle(screen, WHITE, (pellet[1] * TILE_SIZE + TILE_SIZE // 2, pellet[0] * TILE_SIZE + TILE_SIZE // 2), 5)
    for power_pellet in game_state.power_pellets:
        pygame.draw.circle(screen, YELLOW, (power_pellet[1] * TILE_SIZE + TILE_SIZE // 2, power_pellet[0] * TILE_SIZE + TILE_SIZE // 2), 10)
    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW, (game_state.pacman.x * TILE_SIZE + TILE_SIZE // 2, game_state.pacman.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)
    # Draw Ghosts
    for ghost in game_state.ghosts:
        color = BLUE if ghost.state == "frightened" else RED
        pygame.draw.rect(screen, color, (ghost.x * TILE_SIZE, ghost.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def check_collision(game_state):
    # Check collision with walls
    pacman = game_state.pacman

    # Check collision with pellets
    if (pacman.y, pacman.x) in game_state.pellets:
        game_state.pellets.remove((pacman.y, pacman.x))
        game_state.score += 10

    # Check collision with power pellets
    if (pacman.y, pacman.x) in game_state.power_pellets:
        game_state.power_pellets.remove((pacman.y, pacman.x))
        game_state.score += 50
        pacman.state = "power"

    # Check collision with ghosts
    for ghost in game_state.ghosts:
        if ghost.x == pacman.x and ghost.y == pacman.y:
            if pacman.state == "power":
                ghost.state = "frightened"  # Pac-Man can eat the ghost
                ghost.eaten_count += 1
                if ghost.eaten_count > 4:
                    ghost.eaten_count = 4
                game_state.score += 200 * (2 ** ghost.eaten_count)  # Points for eating a ghost
            else:
                game_state.lives -= 1  # Lose a life
                if game_state.lives == 0:
                    game_state.game_over = True

    # Check for level progression
    if not game_state.pellets and not game_state.power_pellets:
        game_state.level += 1
        game_state.pellets = [(r, c) for r in range(ROWS) for c in range(COLS) if game_state.maze_template[r][c] == '.']
        game_state.power_pellets = [(1, 1), (1, COLS - 2), (ROWS - 2, 1), (ROWS - 2, COLS - 2)]
        for ghost in game_state.ghosts:
            ghost.move_x += 1 if ghost.move_x > 0 else -1  # Increase speed of ghosts

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    game_state = GameState()

    while not game_state.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game_state.pacman.move("UP", game_state.maze_template)
        elif keys[pygame.K_DOWN]:
            game_state.pacman.move("DOWN", game_state.maze_template)
        elif keys[pygame.K_LEFT]:
            game_state.pacman.move("LEFT", game_state.maze_template)
        elif keys[pygame.K_RIGHT]:
            game_state.pacman.move("RIGHT", game_state.maze_template)

        for ghost in game_state.ghosts:
            ghost.move(game_state)

        check_collision(game_state)  # Check for collisions after moving Pac-Man
        draw_game(screen, game_state)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()