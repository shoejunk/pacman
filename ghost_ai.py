import random
import math
import config
import game_objects

def blinky_chase(ghost, pacman_position):
    """
    AI strategy for Blinky: directly chase PacMan.
    """
    ghost.target = pacman_position
    ghost.speed = config.BLINKY_SPEED

def pinky_ambush(ghost, pacman_position, pacman_direction):
    """
    AI strategy for Pinky: ambush by targeting a position several tiles ahead of PacMan.
    """
    offset = 4  # number of tiles ahead
    target = (pacman_position[0] + pacman_direction[0] * offset,
              pacman_position[1] + pacman_direction[1] * offset)
    ghost.target = target
    ghost.speed = config.PINKY_SPEED

def inky_unpredictable(ghost, pacman_position):
    """
    AI strategy for Inky: move unpredictably by adding a random offset to PacMan's position.
    """
    offset_x = random.randint(-4, 4)
    offset_y = random.randint(-4, 4)
    target = (pacman_position[0] + offset_x, pacman_position[1] + offset_y)
    ghost.target = target
    ghost.speed = config.INKY_SPEED

def clyde_dual_behavior(ghost, pacman_position):
    """
    AI strategy for Clyde: if close to PacMan, scatter; otherwise, chase.
    """
    distance = math.dist(ghost.position, pacman_position)
    if distance < config.CLYDE_BEHAVIOR_DISTANCE:
        ghost.target = config.CLYDE_SCATTER_POSITION
        ghost.speed = config.CLYDE_SPEED * 0.5  # slower speed when scattering
    else:
        ghost.target = pacman_position
        ghost.speed = config.CLYDE_SPEED

def update_ghosts(ghosts, pacman, power_pellet_active=False):
    """
    Update AI behavior for each ghost based on the current game state.
    
    If power_pellet_active is True, ghosts become vulnerable, their speed is adjusted,
    and they target positions away from PacMan.
    Otherwise, each ghost uses its own strategy.
    """
    for ghost in ghosts:
        if power_pellet_active:
            ghost.speed = config.VULNERABLE_SPEED
            dx = ghost.position[0] - pacman.position[0]
            dy = ghost.position[1] - pacman.position[1]
            ghost.target = (ghost.position[0] + dx, ghost.position[1] + dy)
        else:
            if ghost.name == "Blinky":
                blinky_chase(ghost, pacman.position)
            elif ghost.name == "Pinky":
                pinky_ambush(ghost, pacman.position, pacman.direction)
            elif ghost.name == "Inky":
                inky_unpredictable(ghost, pacman.position)
            elif ghost.name == "Clyde":
                clyde_dual_behavior(ghost, pacman.position)
            else:
                ghost.target = pacman.position
                ghost.speed = 1

def main():
    # Dummy classes to simulate game_objects' Ghost classes and PacMan.
    class DummyGhost:
        def __init__(self, name, position):
            self.name = name
            self.position = position
            self.target = None
            self.speed = 0

        def __repr__(self):
            return f"{self.name}: pos={self.position}, target={self.target}, speed={self.speed}"

    class DummyPacman:
        def __init__(self, position, direction):
            self.position = position
            self.direction = direction

    # In case config does not have the expected attributes, define defaults.
    try:
        _ = config.BLINKY_SPEED
    except AttributeError:
        class Config:
            BLINKY_SPEED = 2
            PINKY_SPEED = 2.5
            INKY_SPEED = 2.2
            CLYDE_SPEED = 1.8
            VULNERABLE_SPEED = 1
            CLYDE_BEHAVIOR_DISTANCE = 5
            CLYDE_SCATTER_POSITION = (0, 0)
        config.__dict__.update({k: v for k, v in Config.__dict__.items() if not k.startswith("__")})
    
    # Create dummy ghost instances.
    blinky = DummyGhost("Blinky", (10, 10))
    pinky = DummyGhost("Pinky", (12, 10))
    inky = DummyGhost("Inky", (8, 8))
    clyde = DummyGhost("Clyde", (5, 5))
    ghosts = [blinky, pinky, inky, clyde]

    # Create a dummy PacMan instance.
    pacman = DummyPacman((15, 15), (1, 0))

    # Test AI strategies in normal state.
    update_ghosts(ghosts, pacman, power_pellet_active=False)

    # Test Blinky: target should be PacMan's position and speed should be config.BLINKY_SPEED.
    assert blinky.target == pacman.position, "Blinky target incorrect in chase strategy."
    assert blinky.speed == config.BLINKY_SPEED, "Blinky speed incorrect in normal state."

    # Test Pinky: target should be PacMan's position offset by 4 tiles in the direction.
    expected_pinky_target = (pacman.position[0] + 4 * pacman.direction[0],
                             pacman.position[1] + 4 * pacman.direction[1])
    assert pinky.target == expected_pinky_target, "Pinky target incorrect in ambush strategy."
    assert pinky.speed == config.PINKY_SPEED, "Pinky speed incorrect in normal state."

    # Test Inky: target should be around PacMan's position with a random offset.
    inky_target = inky.target
    assert pacman.position[0] - 4 <= inky_target[0] <= pacman.position[0] + 4, "Inky target x-coordinate out of expected range."
    assert pacman.position[1] - 4 <= inky_target[1] <= pacman.position[1] + 4, "Inky target y-coordinate out of expected range."
    assert inky.speed == config.INKY_SPEED, "Inky speed incorrect in normal state."

    # Test Clyde: if close, should scatter; otherwise, chase PacMan.
    distance = math.dist(clyde.position, pacman.position)
    if distance < config.CLYDE_BEHAVIOR_DISTANCE:
        expected_clyde_target = config.CLYDE_SCATTER_POSITION
        expected_clyde_speed = config.CLYDE_SPEED * 0.5
    else:
        expected_clyde_target = pacman.position
        expected_clyde_speed = config.CLYDE_SPEED
    assert clyde.target == expected_clyde_target, "Clyde target incorrect in dual behavior."
    assert clyde.speed == expected_clyde_speed, "Clyde speed incorrect in dual behavior."

    # Test AI strategies in power pellet active (vulnerable) state.
    update_ghosts(ghosts, pacman, power_pellet_active=True)
    for ghost in ghosts:
        assert ghost.speed == config.VULNERABLE_SPEED, f"{ghost.name} speed incorrect when vulnerable."
        dx = ghost.position[0] - pacman.position[0]
        dy = ghost.position[1] - pacman.position[1]
        expected_target = (ghost.position[0] + dx, ghost.position[1] + dy)
        assert ghost.target == expected_target, f"{ghost.name} target incorrect when vulnerable."

    # Simulate movement over several game ticks and log positions.
    # For simulation, assume ghost.position moves towards ghost.target by a fraction of the distance.
    def simulate_tick(ghost, fraction=0.2):
        x, y = ghost.position
        tx, ty = ghost.target
        new_x = x + (tx - x) * fraction
        new_y = y + (ty - y) * fraction
        ghost.position = (new_x, new_y)
    
    # Reset ghosts to initial positions.
    blinky.position = (10, 10)
    pinky.position = (12, 10)
    inky.position = (8, 8)
    clyde.position = (5, 5)
    
    # Run simulation for 5 ticks with normal behavior.
    for _ in range(5):
        update_ghosts(ghosts, pacman, power_pellet_active=False)
        for ghost in ghosts:
            simulate_tick(ghost)
    
    # After simulation, ensure that positions have moved and are not equal to initial positions.
    for ghost in ghosts:
        if ghost.name == "Blinky":
            assert ghost.position != (10, 10), f"{ghost.name} did not move during simulation."
        elif ghost.name == "Pinky":
            assert ghost.position != (12, 10), f"{ghost.name} did not move during simulation."
        elif ghost.name == "Inky":
            assert ghost.position != (8, 8), f"{ghost.name} did not move during simulation."
        elif ghost.name == "Clyde":
            assert ghost.position != (5, 5), f"{ghost.name} did not move during simulation."

    print("All tests passed successfully.")
    for ghost in ghosts:
        print(ghost)

if __name__ == "__main__":
    main()