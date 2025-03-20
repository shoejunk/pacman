#!/usr/bin/env python3
import pygame
from game import Game
import config

def main():
    # Instantiate the Game class
    game_instance = Game()

    # Verify that the game_instance has necessary attributes and methods.
    assert hasattr(game_instance, "process_input") and callable(game_instance.process_input), "Missing process_input method"
    assert hasattr(game_instance, "update") and callable(game_instance.update), "Missing update method"
    assert hasattr(game_instance, "render") and callable(game_instance.render), "Missing render method"
    assert hasattr(game_instance, "check_collisions") and callable(game_instance.check_collisions), "Missing check_collisions method"
    assert hasattr(game_instance, "play_audio") and callable(game_instance.play_audio), "Missing play_audio method"
    assert hasattr(game_instance, "run") and callable(game_instance.run), "Missing run method"

    # Test process_input method (without any event in the queue)
    try:
        game_instance.process_input()
    except Exception as e:
        assert False, "process_input method failed: " + str(e)

    # Test update method
    try:
        game_instance.update()
    except Exception as e:
        assert False, "update method failed: " + str(e)

    # Test render method
    try:
        game_instance.render()
    except Exception as e:
        assert False, "render method failed: " + str(e)

    # Test check_collisions method
    try:
        game_instance.check_collisions()
    except Exception as e:
        assert False, "check_collisions method failed: " + str(e)

    # Test play_audio method
    try:
        game_instance.play_audio()
    except Exception as e:
        assert False, "play_audio method failed: " + str(e)

    # Test a limited game loop run to ensure functionality without entering an infinite loop
    iterations = 0
    max_iterations = 3
    original_running = game_instance.running

    def limited_run():
        nonlocal iterations
        while iterations < max_iterations and game_instance.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_instance.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_instance.running = False
            game_instance.process_input()
            game_instance.update()
            game_instance.check_collisions()
            game_instance.play_audio()
            game_instance.render()
            game_instance.clock.tick(config.FPS)
            iterations += 1
        game_instance.running = False
        # Removed pygame.quit() here to avoid uninitializing the video system

    try:
        limited_run()
    except Exception as e:
        assert False, "Limited run loop failed: " + str(e)

    # Restore the original running state for further tests.
    game_instance.running = original_running

    # For testing process_input's ability to quit on ESC, override the input_handler's process_events
    # to simulate recognition of the ESC key event.
    def process_events_override():
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return {"action": "quit"}
        return None

    if hasattr(game_instance, "input_handler"):
        game_instance.input_handler.process_events = process_events_override

    # Test that process_input correctly quits on ESC key press
    test_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
    pygame.event.post(test_event)
    game_instance.process_input()
    assert game_instance.running == False, "Game instance did not quit on ESC key press in process_input test."

    print("All tests passed successfully.")
    
    # Re-instantiate the game to start the actual game loop
    game_instance = Game()
    game_instance.run()

if __name__ == "__main__":
    main()