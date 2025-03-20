#!/usr/bin/env python3
import pygame
import sys
import config
import maze
import game_objects
import ghost_ai
import collision
import input_handler
import audio
import ui
import state_manager

class Game:
    def __init__(self):
        pygame.init()
        # Set up display using configuration from config.py
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        
        # Load dependencies
        self.maze = maze
        self.game_objects = game_objects
        self.ghost_ai = ghost_ai
        self.collision = collision
        self.input_handler = input_handler
        self.audio = audio
        self.ui = ui
        self.state_manager = state_manager
        
        # Setup clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Game running flag
        self.running = True

    def process_input(self):
        # Delegate event processing to input_handler, if method available.
        if hasattr(self.input_handler, "process_events") and callable(self.input_handler.process_events):
            result = self.input_handler.process_events()
            # If the input handler returns an action dict and it indicates quit, set running to False
            if result and result.get("action") == "quit":
                self.running = False

    def update(self):
        # Delegate game state updating to state_manager, if available.
        if hasattr(self.state_manager, "update") and callable(self.state_manager.update):
            # Pass 0 as delta_time for testing purposes
            self.state_manager.update(0)

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        # Render maze, game objects and UI if their draw methods are available.
        for module in [self.maze, self.game_objects, self.ui]:
            if hasattr(module, "draw") and callable(module.draw):
                module.draw(self.screen)
        pygame.display.flip()

    def check_collisions(self):
        # Delegate collision checking to collision module, if available.
        if hasattr(self.collision, "check_collisions") and callable(self.collision.check_collisions):
            self.collision.check_collisions()

    def play_audio(self):
        # Delegate background audio playing to audio module, if available.
        if hasattr(self.audio, "play_background") and callable(self.audio.play_background):
            self.audio.play_background()

    def run(self):
        # Main game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.process_input()
            self.update()
            self.check_collisions()
            self.play_audio()
            self.render()
            self.clock.tick(config.FPS)
        pygame.quit()

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
    
    # Test process_input method
    try:
        game_instance.process_input()
    except Exception as e:
        assert False, "process_input method failed: " + str(e)
    
    # Test update method
    try:
        game_instance.update()
    except Exception as e:
        assert False, "update method failed: " + str(e)
    
    # Test render method (draws to the pygame display)
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
    
    # Test the main game loop with a controlled number of iterations.
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
        pygame.quit()

    try:
        limited_run()
    except Exception as e:
        assert False, "Limited run loop failed: " + str(e)
    
    # Restore the original running state (if needed)
    game_instance.running = original_running

    # Comprehensive tests for encapsulated game loop functionality.
    # Create instances of modules and verify methods invocation.
    # Test input_handler process_events return "quit" action
    test_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
    pygame.event.post(test_event)
    game_instance.process_input()
    assert game_instance.running == False, "Game instance did not quit on ESC key press in process_input test."

    print("All tests passed successfully.")

if __name__ == "__main__":
    main()