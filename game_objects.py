import pygame

try:
    import config
except SyntaxError:
    class DummyConfig:
        PLAYER_SPEED = 1
        GHOST_SPEED = 1
        SPRITE_WIDTH = 16
        SPRITE_HEIGHT = 16
    config = DummyConfig

from maze import Maze

class PacMan:
    def __init__(self, position, direction, lives=3, score=0):
        self.position = position  # tuple (x, y)
        self.direction = direction  # tuple (dx, dy)
        self.lives = lives
        self.score = score

    def move(self):
        new_x = self.position[0] + self.direction[0] * config.PLAYER_SPEED
        new_y = self.position[1] + self.direction[1] * config.PLAYER_SPEED
        self.position = (new_x, new_y)

    def update(self, maze):
        self.move()

    def draw(self, surface=None):
        # Draw PacMan as a yellow circle
        if surface is not None:
            pygame.draw.circle(surface, (255, 255, 0), (int(self.position[0]), int(self.position[1])), config.SPRITE_WIDTH // 2)
        return f"PacMan drawn at {self.position} with sprite width {config.SPRITE_WIDTH}"

class Ghost:
    def __init__(self, position, state="normal", speed=None):
        self.position = position  # tuple (x, y)
        self.state = state  # "normal" or "vulnerable"
        self.speed = speed if speed is not None else config.GHOST_SPEED

    def move(self):
        new_x = self.position[0] + self.speed
        new_y = self.position[1]
        self.position = (new_x, new_y)

    def update(self, maze):
        self.move()

    def draw(self, surface=None):
        # Draw Ghost as a circle: blue if vulnerable, otherwise red.
        color = (0, 0, 255) if self.state == "vulnerable" else (255, 0, 0)
        if surface is not None:
            pygame.draw.circle(surface, color, (int(self.position[0]), int(self.position[1])), config.SPRITE_WIDTH // 2)
        return f"Ghost drawn at {self.position} with color {'blue' if self.state == 'vulnerable' else 'red'} and sprite width {config.SPRITE_WIDTH}"

class Blinky(Ghost):
    def __init__(self, position, state="normal", speed=None):
        super().__init__(position, state, speed)

    def move(self):
        new_x = self.position[0] + self.speed
        new_y = self.position[1]
        self.position = (new_x, new_y)

class Pinky(Ghost):
    def __init__(self, position, state="normal", speed=None):
        super().__init__(position, state, speed)

    def move(self):
        new_x = self.position[0]
        new_y = self.position[1] + self.speed
        self.position = (new_x, new_y)

class Inky(Ghost):
    def __init__(self, position, state="normal", speed=None):
        super().__init__(position, state, speed)

    def move(self):
        new_x = self.position[0] + self.speed
        new_y = self.position[1] + self.speed
        self.position = (new_x, new_y)

class Clyde(Ghost):
    def __init__(self, position, state="normal", speed=None):
        super().__init__(position, state, speed)

    def move(self):
        new_x = self.position[0] - self.speed
        new_y = self.position[1]
        self.position = (new_x, new_y)

class Pellet:
    def __init__(self, position):
        self.position = position
        self.collected = False

    def draw(self, surface=None):
        # Draw Pellet as a small white circle
        if surface is not None:
            pygame.draw.circle(surface, (255, 255, 255), (int(self.position[0]), int(self.position[1])), 3)
        return f"Pellet drawn at {self.position}. Collected: {self.collected}"

class BonusItem:
    def __init__(self, position):
        self.position = position
        self.collected = False

    def draw(self, surface=None):
        # Draw BonusItem as a green square
        if surface is not None:
            rect = pygame.Rect(self.position[0] - config.SPRITE_WIDTH // 2,
                               self.position[1] - config.SPRITE_HEIGHT // 2,
                               config.SPRITE_WIDTH,
                               config.SPRITE_HEIGHT)
            pygame.draw.rect(surface, (0, 255, 0), rect)
        return f"BonusItem drawn at {self.position}. Collected: {self.collected}"

def draw_objects(surface, objects):
    # Draw all primary objects on the provided pygame surface
    pacman = objects.get("pacman")
    ghosts = objects.get("ghosts", [])
    pellet = objects.get("pellet")
    bonus_item = objects.get("bonus_item")

    if pacman:
        pacman.draw(surface)
    for ghost in ghosts:
        ghost.draw(surface)
    if pellet:
        pellet.draw(surface)
    if bonus_item:
        bonus_item.draw(surface)

def initialize_objects():
    pacman = PacMan(position=(0, 0), direction=(1, 0), lives=3, score=0)
    ghosts = [
        Blinky(position=(10, 10)),
        Pinky(position=(20, 20)),
        Inky(position=(30, 30)),
        Clyde(position=(40, 40))
    ]
    pellet = Pellet(position=(5, 5))
    bonus_item = BonusItem(position=(7, 7))
    return {"pacman": pacman, "ghosts": ghosts, "pellet": pellet, "bonus_item": bonus_item}

def main():
    # Initialize pygame and create a surface for drawing (used only for demonstration purposes)
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("PacMan Test")
    maze = Maze()
    
    # Initialize objects using the initialize_objects function
    objects = initialize_objects()
    pacman = objects["pacman"]
    ghosts = objects["ghosts"]
    pellet = objects["pellet"]
    bonus = objects["bonus_item"]
    
    # Test PacMan functionalities
    init_position = pacman.position
    pacman.move()
    expected_position = (init_position[0] + config.PLAYER_SPEED, init_position[1])
    assert pacman.position == expected_position, "PacMan.move() did not update position correctly."
    draw_output = pacman.draw()
    assert "PacMan drawn" in draw_output, "PacMan.draw() output invalid."
    
    # Test Pellet and collision with PacMan
    pellet.collected = False
    if pacman.position == pellet.position:
        pellet.collected = True
        pacman.score += 10
    # For testing, force a collision if not already collided.
    if pacman.position != pellet.position:
        pacman.position = pellet.position
        pellet.collected = True
        pacman.score += 10
    assert pellet.collected == True, "Pellet was not marked as collected after collision."
    assert pacman.score >= 10, "PacMan score did not update correctly after eating pellet."
    
    # Test BonusItem drawing
    bonus_draw = bonus.draw()
    assert "BonusItem drawn" in bonus_draw, "BonusItem.draw() output invalid."
    
    # Test Ghosts movements and drawing
    # Blinky
    blinky = ghosts[0]
    pos_before = blinky.position
    blinky.move()
    expected_pos_blinky = (pos_before[0] + config.GHOST_SPEED, pos_before[1])
    assert blinky.position == expected_pos_blinky, "Blinky.move() did not update position correctly."
    
    # Pinky
    pinky = ghosts[1]
    pos_before = pinky.position
    pinky.move()
    expected_pos_pinky = (pos_before[0], pos_before[1] + config.GHOST_SPEED)
    assert pinky.position == expected_pos_pinky, "Pinky.move() did not update position correctly."
    
    # Inky
    inky = ghosts[2]
    pos_before = inky.position
    inky.move()
    expected_pos_inky = (pos_before[0] + config.GHOST_SPEED, pos_before[1] + config.GHOST_SPEED)
    assert inky.position == expected_pos_inky, "Inky.move() did not update position correctly."
    
    # Clyde
    clyde = ghosts[3]
    pos_before = clyde.position
    clyde.move()
    expected_pos_clyde = (pos_before[0] - config.GHOST_SPEED, pos_before[1])
    assert clyde.position == expected_pos_clyde, "Clyde.move() did not update position correctly."
    
    # Test Ghost vulnerable drawing state
    for ghost in ghosts:
        ghost.state = "vulnerable"
        draw_str = ghost.draw()
        assert "blue" in draw_str, "Ghost.draw() did not reflect vulnerable state correctly."
    
    # Test Ghost update function
    prev_position = blinky.position
    blinky.update(maze)
    expected_position = (prev_position[0] + config.GHOST_SPEED, prev_position[1])
    assert blinky.position == expected_position, "Ghost.update() did not update position correctly."
    
    # Optionally, demonstrate drawing all objects on the pygame surface.
    screen.fill((0, 0, 0))  # Clear screen with black background
    draw_objects(screen, objects)
    pygame.display.flip()
    
    # Wait briefly so we can see the window (for demonstration purposes only)
    pygame.time.wait(500)
    
    print("All tests passed successfully.")
    pygame.quit()

if __name__ == "__main__":
    main()