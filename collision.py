#!/usr/bin/env python3

def is_grid_aligned(entity, cell_size, tolerance):
    """
    Check if the entity is approximately aligned with the grid.
    Entity should have x and y attributes.
    """
    if not (hasattr(entity, "x") and hasattr(entity, "y")):
        raise AttributeError("Entity must have 'x' and 'y' attributes.")
    rem_x = entity.x % cell_size
    rem_y = entity.y % cell_size
    aligned_x = rem_x <= tolerance or cell_size - rem_x <= tolerance
    aligned_y = rem_y <= tolerance or cell_size - rem_y <= tolerance
    return aligned_x and aligned_y

def get_bounding_box(entity):
    """
    Returns the bounding box of the entity as (left, top, right, bottom).
    Assumes entity has attributes: x, y, width, and height.
    """
    if not (hasattr(entity, "x") and hasattr(entity, "y") and hasattr(entity, "width") and hasattr(entity, "height")):
        raise AttributeError("Entity is missing one of the required attributes: x, y, width, height.")
    left = entity.x
    top = entity.y
    right = entity.x + entity.width
    bottom = entity.y + entity.height
    return left, top, right, bottom

def check_bounding_box_collision(entity1, entity2):
    """
    Check if the bounding boxes of two entities overlap.
    """
    left1, top1, right1, bottom1 = get_bounding_box(entity1)
    left2, top2, right2, bottom2 = get_bounding_box(entity2)
    
    if right1 <= left2 or right2 <= left1:
        return False
    if bottom1 <= top2 or bottom2 <= top1:
        return False
    return True

def detect_collision(entity1, entity2, config):
    """
    Detect collision between two entities.
    First, ensure both entities are roughly aligned on the grid.
    Then, perform a fast bounding box check.
    """
    if not (is_grid_aligned(entity1, config.CELL_SIZE, config.GRID_TOLERANCE) and 
            is_grid_aligned(entity2, config.CELL_SIZE, config.GRID_TOLERANCE)):
        return False
    return check_bounding_box_collision(entity1, entity2)

def resolve_pellet_collision(pacman, pellet, config):
    """
    Resolve collision between pacman and a pellet.
    If collision occurs and pellet is active, mark it as consumed,
    and update pacman's score.
    """
    if pellet.active and detect_collision(pacman, pellet, config):
        pellet.active = False
        pacman.score += pellet.value
        return True
    return False

def resolve_ghost_collision(pacman, ghost, config):
    """
    Resolve collision between pacman and a ghost.
    If collision occurs:
      - If ghost is vulnerable, mark ghost as eaten and update pacman's score.
      - If ghost is not vulnerable, decrement pacman's lives.
    """
    if detect_collision(pacman, ghost, config):
        if ghost.vulnerable:
            ghost.consumed = True
            pacman.score += ghost.value
            return "ghost_eaten"
        else:
            pacman.lives -= 1
            return "life_lost"
    return "no_collision"

def resolve_bonus_item_collision(pacman, bonus, config):
    """
    Resolve collision between pacman and a bonus item.
    If collision occurs and bonus item is active, mark it as consumed
    and update pacman's score.
    """
    if bonus.active and detect_collision(pacman, bonus, config):
        bonus.active = False
        pacman.score += bonus.value
        return True
    return False

def detect_wall_collision(entity, maze, config):
    """
    Detect collision between an entity and a maze wall.
    Uses the entity's center position to determine the current grid cell.
    Assumes maze has a method get_cell(row, col) that returns a cell value,
    where a value of 1 represents a wall.
    """
    if not (hasattr(entity, "x") and hasattr(entity, "y") and hasattr(entity, "width") and hasattr(entity, "height")):
        raise AttributeError("Entity is missing one of the required attributes: x, y, width, height.")
    center_x = entity.x + entity.width / 2
    center_y = entity.y + entity.height / 2
    col = int(center_x // config.CELL_SIZE)
    row = int(center_y // config.CELL_SIZE)
    if maze.get_cell(row, col) == 1:
        return True
    return False

def initialize_collision(config, maze):
    """
    Initialize collision detection system.
    Validates that the configuration and maze have the required attributes.
    Returns True if initialization is successful.
    """
    if not hasattr(config, "CELL_SIZE") or not hasattr(config, "GRID_TOLERANCE"):
        raise AttributeError("Config is missing required attributes: CELL_SIZE and GRID_TOLERANCE.")
    if not hasattr(maze, "get_cell") or not callable(maze.get_cell):
        raise AttributeError("Maze must have a callable get_cell method.")
    return True

def main():
    # Create dummy config with required attributes (using uppercase constants)
    class DummyConfig:
        CELL_SIZE = 20
        GRID_TOLERANCE = 2

    config = DummyConfig()

    # Create dummy maze for testing wall collision.
    # Maze layout: 0 = empty, 1 = wall.
    class DummyMaze:
        def __init__(self, layout):
            self.layout = layout

        def get_cell(self, row, col):
            if 0 <= row < len(self.layout) and 0 <= col < len(self.layout[0]):
                return self.layout[row][col]
            return 0

    # Maze grid (3x3): center is empty, borders are walls.
    maze_layout = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    maze = DummyMaze(maze_layout)

    # Initialize collision system
    assert initialize_collision(config, maze) is True, "Collision system initialization failed."

    # Define a base dummy game object class for testing (simulate Pac-Man, Ghost, Pellet, Bonus)
    class DummyGameObject:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

    # Define dummy PacMan
    class DummyPacMan(DummyGameObject):
        def __init__(self, x, y):
            super().__init__(x, y, 20, 20)
            self.score = 0
            self.lives = 3

    # Define dummy Pellet
    class DummyPellet(DummyGameObject):
        def __init__(self, x, y, value=10):
            super().__init__(x, y, 20, 20)
            self.active = True
            self.value = value

    # Define dummy Ghost
    class DummyGhost(DummyGameObject):
        def __init__(self, x, y, value=200):
            super().__init__(x, y, 20, 20)
            self.vulnerable = False
            self.consumed = False
            self.value = value

    # Define dummy Bonus Item
    class DummyBonus(DummyGameObject):
        def __init__(self, x, y, value=50):
            super().__init__(x, y, 20, 20)
            self.active = True
            self.value = value

    # Test 1: Pellet collision test (collision occurs)
    pacman = DummyPacMan(40, 40)
    pellet = DummyPellet(40, 40)
    result = resolve_pellet_collision(pacman, pellet, config)
    assert result is True, "Pellet collision was not resolved when it should be."
    assert pellet.active is False, "Pellet should be marked as consumed."
    assert pacman.score == 10, "PacMan score should have increased by pellet value."

    # Test 2: Pellet collision test (no collision)
    pellet = DummyPellet(80, 80)
    old_score = pacman.score
    result = resolve_pellet_collision(pacman, pellet, config)
    assert result is False, "Pellet collision incorrectly resolved when entities should not collide."
    assert pellet.active is True, "Pellet should remain active when no collision occurs."
    assert pacman.score == old_score, "PacMan score should not change when there is no collision."

    # Test 3: Ghost collision test (non-vulnerable ghost)
    pacman = DummyPacMan(40, 40)
    ghost = DummyGhost(40, 40)
    initial_lives = pacman.lives
    result = resolve_ghost_collision(pacman, ghost, config)
    assert result == "life_lost", "Ghost collision did not result in life lost for non-vulnerable ghost."
    assert pacman.lives == initial_lives - 1, "PacMan lives should decrement on collision with non-vulnerable ghost."

    # Test 4: Ghost collision test (vulnerable ghost)
    pacman = DummyPacMan(40, 40)
    ghost = DummyGhost(40, 40)
    ghost.vulnerable = True
    initial_score = pacman.score
    result = resolve_ghost_collision(pacman, ghost, config)
    assert result == "ghost_eaten", "Ghost collision did not resolve ghost eaten when ghost is vulnerable."
    assert ghost.consumed is True, "Ghost should be marked as consumed when vulnerable."
    assert pacman.score == initial_score + ghost.value, "PacMan score should increase by ghost value when ghost is eaten."

    # Test 5: Bonus item collision test (collision occurs)
    pacman = DummyPacMan(40, 40)
    bonus = DummyBonus(40, 40)
    initial_score = pacman.score
    result = resolve_bonus_item_collision(pacman, bonus, config)
    assert result is True, "Bonus collision was not resolved when it should be."
    assert bonus.active is False, "Bonus item should be marked as consumed."
    assert pacman.score == initial_score + bonus.value, "PacMan score should have increased by bonus value."

    # Test 6: Bonus item collision test (no collision)
    pacman = DummyPacMan(40, 40)
    bonus = DummyBonus(80, 80)
    initial_score = pacman.score
    result = resolve_bonus_item_collision(pacman, bonus, config)
    assert result is False, "Bonus collision incorrectly resolved when entities should not collide."
    assert bonus.active is True, "Bonus should remain active when no collision occurs."
    assert pacman.score == initial_score, "PacMan score should not change when there is no bonus collision."

    # Test 7: Wall collision test
    # Test for an entity in a wall cell (top-left corner, which is a wall according to maze_layout)
    pacman = DummyPacMan(0, 0)
    assert detect_wall_collision(pacman, maze, config) is True, "Wall collision should be detected for an entity in a wall cell."
    # Test for an entity in a non-wall cell (center cell)
    pacman = DummyPacMan(20, 20)
    assert detect_wall_collision(pacman, maze, config) is False, "Wall collision incorrectly detected for an entity in a non-wall cell."

    print("All collision tests passed successfully.")

if __name__ == "__main__":
    main()