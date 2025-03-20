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
            ghost_type = ghost.__class__.__name__
            if ghost_type == "Blinky":
                blinky_chase(ghost, pacman.position)
            elif ghost_type == "Pinky":
                pinky_ambush(ghost, pacman.position, pacman.direction)
            elif ghost_type == "Inky":
                inky_unpredictable(ghost, pacman.position)
            elif ghost_type == "Clyde":
                clyde_dual_behavior(ghost, pacman.position)

def initialize_ai():
    """
    Initialize any AI-specific timers or settings.
    """
    # For now, no initialization is needed.
    pass

def main():
    # Create test instances for PacMan and ghosts using game_objects.initialize_objects
    objects = game_objects.initialize_objects()
    pacman = objects["pacman"]
    ghosts = objects["ghosts"]

    # Ensure pacman has a clear direction for testing purposes
    pacman.position = (10, 10)
    pacman.direction = (1, 0)

    # Testing Blinky's AI strategy
    blinky = ghosts[0]  # Should be an instance of Blinky from game_objects
    blinky.position = (5, 5)
    blinky_chase(blinky, pacman.position)
    assert blinky.target == pacman.position, "Blinky target not set correctly by blinky_chase."
    assert blinky.speed == config.BLINKY_SPEED, "Blinky speed not set correctly by blinky_chase."

    # Testing Pinky's AI strategy
    pinky = ghosts[1]  # Should be an instance of Pinky
    pinky.position = (5, 5)
    pinky_ambush(pinky, pacman.position, pacman.direction)
    expected_pinky_target = (pacman.position[0] + 4 * pacman.direction[0],
                             pacman.position[1] + 4 * pacman.direction[1])
    assert pinky.target == expected_pinky_target, "Pinky target not set correctly by pinky_ambush."
    assert pinky.speed == config.PINKY_SPEED, "Pinky speed not set correctly by pinky_ambush."

    # Testing Inky's AI strategy
    inky = ghosts[2]  # Should be an instance of Inky
    inky.position = (0, 0)
    inky_unpredictable(inky, pacman.position)
    # Check that the target is within 4 units offset from pacman.position
    offset_x = inky.target[0] - pacman.position[0]
    offset_y = inky.target[1] - pacman.position[1]
    assert -4 <= offset_x <= 4, "Inky unpredictable target offset_x out of range."
    assert -4 <= offset_y <= 4, "Inky unpredictable target offset_y out of range."
    assert inky.speed == config.INKY_SPEED, "Inky speed not set correctly by inky_unpredictable."

    # Testing Clyde's AI strategy
    clyde = ghosts[3]  # Should be an instance of Clyde
    # First case: distance less than threshold, should scatter
    clyde.position = (pacman.position[0] + 1, pacman.position[1] + 1)
    clyde_dual_behavior(clyde, pacman.position)
    assert clyde.target == config.CLYDE_SCATTER_POSITION, "Clyde target not set correctly when scattering."
    assert clyde.speed == config.CLYDE_SPEED * 0.5, "Clyde speed not set correctly when scattering."

    # Second case: distance greater than or equal to threshold, should chase
    clyde.position = (pacman.position[0] + config.CLYDE_BEHAVIOR_DISTANCE + 1, pacman.position[1])
    clyde_dual_behavior(clyde, pacman.position)
    assert clyde.target == pacman.position, "Clyde target not set correctly when chasing."
    assert clyde.speed == config.CLYDE_SPEED, "Clyde speed not set correctly when chasing."

    # Testing update_ghosts without power pellet (normal state)
    # Reset positions for testing
    blinky.position = (0, 0)
    pinky.position = (0, 0)
    inky.position = (0, 0)
    clyde.position = (0, 0)
    pacman.position = (10, 10)
    pacman.direction = (0, 1)
    update_ghosts(ghosts, pacman, power_pellet_active=False)
    # Check based on ghost type
    # For Blinky, target should equal pacman.position.
    assert blinky.target == pacman.position, "update_ghosts failed for Blinky in normal state."
    # For Pinky, target should be pacman.position offset by 4 in pacman's direction.
    expected_pinky_target = (pacman.position[0] + pacman.direction[0] * 4, pacman.position[1] + pacman.direction[1] * 4)
    assert pinky.target == expected_pinky_target, "update_ghosts failed for Pinky in normal state."
    # For Inky, we check that the target is within acceptable offset range.
    offset_x = inky.target[0] - pacman.position[0]
    offset_y = inky.target[1] - pacman.position[1]
    assert -4 <= offset_x <= 4, "update_ghosts failed for Inky (offset_x out of range)."
    assert -4 <= offset_y <= 4, "update_ghosts failed for Inky (offset_y out of range)."
    # For Clyde, depends on distance, and here distance is math.dist((0,0),(10,10)) which is > CLYDE_BEHAVIOR_DISTANCE
    assert clyde.target == pacman.position, "update_ghosts failed for Clyde in normal state."

    # Testing update_ghosts with power pellet active.
    # Set ghosts to known positions.
    blinky.position = (5, 5)
    pinky.position = (6, 6)
    inky.position = (7, 7)
    clyde.position = (8, 8)
    pacman.position = (10, 10)
    update_ghosts(ghosts, pacman, power_pellet_active=True)
    for ghost in ghosts:
        # Expect ghost speed to be set to vulnerable speed.
        assert ghost.speed == config.VULNERABLE_SPEED, "update_ghosts failed to set vulnerable speed."
        # Expect ghost.target to be calculated based on vector from pacman to ghost.
        dx = ghost.position[0] - pacman.position[0]
        dy = ghost.position[1] - pacman.position[1]
        expected_target = (ghost.position[0] + dx, ghost.position[1] + dy)
        assert ghost.target == expected_target, "update_ghosts failed to set vulnerable target correctly."

    # Test initialize_ai function
    try:
        initialize_ai()
    except Exception as e:
        assert False, "initialize_ai function raised an exception: " + str(e)

    print("All tests passed successfully.")

if __name__ == "__main__":
    main()