#!/usr/bin/env python3

# collision.py

# This module provides functions and classes for detecting and handling collisions between game objects.
# Dependencies (assumed to be defined elsewhere): config.py, maze.py, game_objects.py

def is_grid_aligned(entity, cell_size, tolerance):
    """
    Check if the entity is approximately aligned with the grid.
    Entity should have x and y attributes.
    """
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
    if not (is_grid_aligned(entity1, config.cell_size, config.grid_tolerance) and 
            is_grid_aligned(entity2, config.cell_size, config.grid_tolerance)):
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
      - If ghost is vulnerable, mark ghost as eaten, update pacman's score.
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
    Uses the entity's current grid cell (based on its center) and the maze layout to determine collision.
    Assumes maze has a method get_cell(row, col) that returns a cell value,
    and that wall cells are represented with a value of 1.
    """
    # Compute the current grid cell of the entity's center
    center_x = entity.x + entity.width / 2
    center_y = entity.y + entity.height / 2
    col = int(center_x // config.cell_size)
    row = int(center_y // config.cell_size)
    # Check if maze cell is a wall (1 indicates a wall)
    if maze.get_cell(row, col) == 1:
        return True
    return False

def main():
    # Define dummy config with required attributes
    class DummyConfig:
        cell_size = 20
        grid_tolerance = 2

    config = DummyConfig()

    # Define dummy maze for testing wall collision. Maze layout: 0 = empty, 1 = wall.
    class DummyMaze:
        def __init__(self, layout):
            self.layout = layout
        
        def get_cell(self, row, col):
            if 0 <= row < len(self.layout) and 0 <= col < len(self.layout[0]):
                return self.layout[row][col]
            return 0

    # Create a simple maze layout
    # Maze grid (3x3): center is empty, borders are walls.
    maze_layout = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    maze = DummyMaze(maze_layout)

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

    # Test 1: Pellet collision test
    pacman = DummyPacMan(40, 40)
    pellet = DummyPellet(40, 40)
    result = resolve_pellet_collision(pacman, pellet, config)
    assert result is True, "Pellet collision was not resolved when it should be."
    assert pellet.active is False, "Pellet should be marked as consumed."
    assert pacman.score == 10, "PacMan score should have increased by pellet value."

    # Reset pellet for non-collision test.
    pellet = DummyPellet(100, 100)
    result = resolve_pellet_collision(pacman, pellet, config)
    assert result is False, "Pellet collision detected when there should be no collision."
    assert pellet.active is True, "Pellet should remain active when there is no collision."

    # Test 2: Ghost collision test
    ghost = DummyGhost(40, 40)
    # First test ghost in non-vulnerable state
    pacman.lives = 3
    result = resolve_ghost_collision(pacman, ghost, config)
    assert result == "life_lost", "Ghost collision (non-vulnerable) should result in life lost."
    assert pacman.lives == 2, "PacMan lives should decrement by one on collision with non-vulnerable ghost."
    # Test ghost in vulnerable state
    ghost = DummyGhost(40, 40)
    ghost.vulnerable = True
    ghost.consumed = False
    prev_score = pacman.score
    result = resolve_ghost_collision(pacman, ghost, config)
    assert result == "ghost_eaten", "Ghost collision (vulnerable) should result in ghost being eaten."
    assert ghost.consumed is True, "Ghost should be marked as consumed when vulnerable."
    assert pacman.score == prev_score + ghost.value, "PacMan score should increase by ghost value when ghost is eaten."

    # Test 3: Bonus collision test
    bonus = DummyBonus(40, 40)
    prev_score = pacman.score
    result = resolve_bonus_item_collision(pacman, bonus, config)
    assert result is True, "Bonus collision should have been detected."
    assert bonus.active is False, "Bonus item should be marked as consumed after collision."
    assert pacman.score == prev_score + bonus.value, "PacMan score should increase by bonus item value."

    # Test 4: No collision when near but not overlapping grid cells
    pacman = DummyPacMan(40, 40)
    pellet = DummyPellet(61, 61)  # Not overlapping, gap between them
    result = detect_collision(pacman, pellet, config)
    assert result is False, "Collision should not be detected when objects do not overlap."

    # Test 5: Wall collision test
    # Place an object in a cell that is a wall.
    # Using maze layout defined above: only (1,1) is non-wall.
    # Coordinates for (0,0) cell (upper-left) will be a wall.
    wall_entity = DummyGameObject(5, 5, 10, 10)  # This should be in cell (0,0)
    is_wall = detect_wall_collision(wall_entity, maze, config)
    assert is_wall is True, "Wall collision should be detected for an entity in a wall cell."
    
    # Test 6: No wall collision in empty cell.
    empty_entity = DummyGameObject(25, 25, 10, 10)  # Center of cell (1,1)
    is_wall = detect_wall_collision(empty_entity, maze, config)
    assert is_wall is False, "No wall collision should be detected for an entity in an open cell."

    print("All collision tests passed.")

if __name__ == "__main__":
    main()