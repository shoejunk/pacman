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
        sprite_color = "blue" if self.state == "vulnerable" else "red"
        return f"Ghost drawn at {self.position} with color {sprite_color} and sprite width {config.SPRITE_WIDTH}"

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
        return f"Pellet drawn at {self.position}. Collected: {self.collected}"

class BonusItem:
    def __init__(self, position):
        self.position = position
        self.collected = False

    def draw(self, surface=None):
        return f"BonusItem drawn at {self.position}. Collected: {self.collected}"

def main():
    maze = Maze()

    # Test PacMan functionalities
    pacman = PacMan(position=(0, 0), direction=(1, 0), lives=3, score=0)
    init_position = pacman.position
    pacman.move()
    expected_position = (init_position[0] + config.PLAYER_SPEED, init_position[1])
    assert pacman.position == expected_position, "PacMan.move() did not update position correctly."
    draw_output = pacman.draw()
    assert "PacMan drawn" in draw_output, "PacMan.draw() output invalid."

    # Test Pellet and collision with PacMan
    pellet = Pellet(position=pacman.position)
    assert pellet.collected == False, "Pellet should initially be not collected."
    if pacman.position == pellet.position:
        pellet.collected = True
        pacman.score += 10
    assert pellet.collected == True, "Pellet was not marked as collected after collision."
    assert pacman.score == 10, "PacMan score did not update correctly after eating pellet."

    # Test BonusItem drawing
    bonus = BonusItem(position=(5, 5))
    bonus_draw = bonus.draw()
    assert "BonusItem drawn" in bonus_draw, "BonusItem.draw() output invalid."

    # Test Ghosts movements and drawing
    blinky = Blinky(position=(10, 10))
    pinky = Pinky(position=(20, 20))
    inky = Inky(position=(30, 30))
    clyde = Clyde(position=(40, 40))

    pos_before = blinky.position
    blinky.move()
    expected_pos_blinky = (pos_before[0] + config.GHOST_SPEED, pos_before[1])
    assert blinky.position == expected_pos_blinky, "Blinky.move() did not update position correctly."

    pos_before = pinky.position
    pinky.move()
    expected_pos_pinky = (pos_before[0], pos_before[1] + config.GHOST_SPEED)
    assert pinky.position == expected_pos_pinky, "Pinky.move() did not update position correctly."

    pos_before = inky.position
    inky.move()
    expected_pos_inky = (pos_before[0] + config.GHOST_SPEED, pos_before[1] + config.GHOST_SPEED)
    assert inky.position == expected_pos_inky, "Inky.move() did not update position correctly."

    pos_before = clyde.position
    clyde.move()
    expected_pos_clyde = (pos_before[0] - config.GHOST_SPEED, pos_before[1])
    assert clyde.position == expected_pos_clyde, "Clyde.move() did not update position correctly."

    # Test Ghost vulnerable drawing state
    for ghost in [blinky, pinky, inky, clyde]:
        ghost.state = "vulnerable"
        draw_str = ghost.draw()
        assert "blue" in draw_str, "Ghost.draw() did not reflect vulnerable state correctly."

    # Test Ghost update function
    prev_position = blinky.position
    blinky.update(maze)
    expected_position = (prev_position[0] + config.GHOST_SPEED, prev_position[1])
    assert blinky.position == expected_position, "Ghost.update() did not update position correctly."

    print("All tests passed successfully.")

if __name__ == "__main__":
    main()