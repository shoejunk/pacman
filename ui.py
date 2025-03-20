#!/usr/bin/env python3
import pygame

try:
    from config import TILE_SIZE, MAZE_OFFSET, HUD_FONT, HUD_FONT_SIZE, HUD_COLOR, SCORE_POS, LIVES_POS, LEVEL_POS, MENU_POS
except Exception:
    TILE_SIZE = 20
    MAZE_OFFSET = (0, 0)
    HUD_FONT = None  # Use default system font if not provided
    HUD_FONT_SIZE = 24
    HUD_COLOR = (255, 255, 255)  # White color for HUD text
    SCORE_POS = (10, 10)
    LIVES_POS = (10, 40)
    LEVEL_POS = (10, 70)
    MENU_POS = (200, 200)

class Maze:
    def __init__(self):
        self.initialize_maze()

    def initialize_maze(self):
        # Hard-coded maze layout where:
        # 'W' represents a wall,
        # 'P' represents a pellet,
        # ' ' represents an empty space,
        # 'T' represents a tunnel (wrap-around cell).
        self.layout = [
            list("WWWWWWWWWW"),
            list("T P    P T"),
            list("W WWWW W W"),
            list("W        W"),
            list("WPWWWWWWPW"),
            list("W        W"),
            list("W WWWW W W"),
            list("T P    P T"),
            list("WWWWWWWWWW")
        ]
        self.rows = len(self.layout)
        self.cols = len(self.layout[0])

    def get_cell(self, row, col):
        """Return the content of the cell at the given row and column."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.layout[row][col]
        return None

    def is_wall(self, row, col):
        """Return True if the cell is a wall."""
        return self.get_cell(row, col) == 'W'

    def is_pellet(self, row, col):
        """Return True if the cell is a pellet."""
        return self.get_cell(row, col) == 'P'

    def is_tunnel(self, row, col):
        """Return True if the cell is a tunnel."""
        return self.get_cell(row, col) == 'T'

    def consume_pellet(self, row, col):
        """If the cell contains a pellet, remove it (set to empty) and return True.
           Otherwise, return False."""
        if self.is_pellet(row, col):
            self.layout[row][col] = ' '
            return True
        return False

    def pellet_count(self):
        """Return the total number of pellets remaining in the maze."""
        count = 0
        for row in self.layout:
            count += row.count('P')
        return count

    def grid_to_screen(self, row, col):
        """Convert a grid coordinate (row, col) to screen coordinate (x, y).
           Assumes TILE_SIZE is the size of a cell in pixels and MAZE_OFFSET is a tuple (offset_x, offset_y)."""
        offset_x, offset_y = MAZE_OFFSET
        screen_x = offset_x + col * TILE_SIZE
        screen_y = offset_y + row * TILE_SIZE
        return (screen_x, screen_y)
    
    def draw(self, screen):
        """Draw the maze layout on the given screen (pygame surface)."""
        wall_color = (0, 0, 255)       # Blue walls
        pellet_color = (255, 255, 0)   # Yellow pellets
        tunnel_color = (192, 192, 192) # Gray tunnels
        for row_idx, row in enumerate(self.layout):
            for col_idx, cell in enumerate(row):
                x, y = self.grid_to_screen(row_idx, col_idx)
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                if cell == 'W':
                    pygame.draw.rect(screen, wall_color, rect)
                elif cell == 'P':
                    center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    radius = TILE_SIZE // 6
                    pygame.draw.circle(screen, pellet_color, center, radius)
                elif cell == 'T':
                    pygame.draw.rect(screen, tunnel_color, rect)

    def render(self):
        """Renders the maze layout onto the screen.
           For this implementation, it prints a textual representation to the console."""
        for row in self.layout:
            print("".join(row))

class UIManager:
    def __init__(self, score=0, lives=3, level=1, menu_text=""):
        self.score = score
        self.lives = lives
        self.level = level
        self.menu_text = menu_text
        # Initialize the font module and set up the font
        pygame.font.init()
        if HUD_FONT:
            self.font = pygame.font.Font(HUD_FONT, HUD_FONT_SIZE)
        else:
            self.font = pygame.font.SysFont(None, HUD_FONT_SIZE)

    def draw(self, screen):
        """Draw all user interface components (HUD elements, score, lives counter, level indicator, and menus)
           on the given screen. These elements are layered on top of the gameplay graphics."""
        score_text = f"Score: {self.score}"
        lives_text = f"Lives: {self.lives}"
        level_text = f"Level: {self.level}"

        score_surface = self.font.render(score_text, True, HUD_COLOR)
        lives_surface = self.font.render(lives_text, True, HUD_COLOR)
        level_surface = self.font.render(level_text, True, HUD_COLOR)

        screen.blit(score_surface, SCORE_POS)
        screen.blit(lives_surface, LIVES_POS)
        screen.blit(level_surface, LEVEL_POS)

        if self.menu_text:
            menu_surface = self.font.render(self.menu_text, True, HUD_COLOR)
            screen.blit(menu_surface, MENU_POS)

def initialize_maze():
    """Initialize and return a Maze instance."""
    return Maze()

def main():
    # Create a Maze instance using initialize_maze
    maze = initialize_maze()
    
    # Test get_cell for valid coordinates.
    assert maze.get_cell(0, 0) == 'W', "Top-left cell should be a wall."
    assert maze.get_cell(1, 2) == 'P', "Cell (1,2) should be a pellet."
    assert maze.get_cell(1, 0) == 'T', "Cell (1,0) should be a tunnel."
    
    # Test get_cell for coordinates outside the maze.
    assert maze.get_cell(-1, 0) is None, "Out-of-bound row should return None."
    assert maze.get_cell(0, 10) is None, "Out-of-bound column should return None."
    
    # Expected pellet positions:
    # Row 1: at columns 2 and 7 => 2 pellets.
    # Row 4: at columns 1 and 8 => 2 pellets.
    # Row 7: at columns 2 and 7 => 2 pellets.
    # Total expected pellets = 6.
    expected_initial_pellet_count = 6
    initial_count = maze.pellet_count()
    assert initial_count == expected_initial_pellet_count, "Initial pellet count mismatch."
    
    # Render the initial maze layout.
    print("Initial Maze Layout:")
    maze.render()
    
    # Test consuming a pellet.
    consumed = maze.consume_pellet(1, 2)
    assert consumed, "Pellet consumption failed when it should have succeeded."
    assert not maze.is_pellet(1, 2), "Pellet was not removed properly."
    new_count = maze.pellet_count()
    assert new_count == expected_initial_pellet_count - 1, "Pellet count did not decrease correctly after consumption."
    
    # Test wall detection.
    assert maze.is_wall(0, 0), "Cell (0,0) should be a wall."
    assert not maze.is_wall(3, 3), "Cell (3,3) should not be a wall."
    
    # Test tunnel detection.
    tunnel_positions = [(1, 0), (1, 9), (7, 0), (7, 9)]
    for row, col in tunnel_positions:
        assert maze.is_tunnel(row, col), f"Cell at ({row}, {col}) should be a tunnel."
    
    # Test grid_to_screen coordinate transformation.
    screen_coord = maze.grid_to_screen(0, 0)
    assert screen_coord == MAZE_OFFSET, "Grid to screen conversion failed for cell (0, 0)."
    expected_coord = (MAZE_OFFSET[0] + 3 * TILE_SIZE, MAZE_OFFSET[1] + 2 * TILE_SIZE)
    screen_coord = maze.grid_to_screen(2, 3)
    assert screen_coord == expected_coord, "Grid to screen conversion failed for cell (2, 3)."
    
    print("\nMaze Layout after consuming one pellet at (1,2):")
    maze.render()
    
    # Initialize pygame and set up the display.
    pygame.init()
    screen_width = MAZE_OFFSET[0] * 2 + maze.cols * TILE_SIZE
    screen_height = MAZE_OFFSET[1] * 2 + maze.rows * TILE_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Drawing and UI Test")
    
    clock = pygame.time.Clock()
    ui_manager = UIManager(score=100, lives=3, level=1, menu_text="Press ESC to exit")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        # Fill the background.
        screen.fill((0, 0, 0))
        
        # Draw the maze (gameplay graphics).
        maze.draw(screen)
        
        # Draw the UI elements on top.
        ui_manager.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()