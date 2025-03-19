#!/usr/bin/env python3
import time
import config
import input_handler
import game_objects
import maze
import ghost_ai
import ui
import audio
import collision

# Ensure required game state constants exist in config; if not, define them locally.
if not hasattr(config, 'GAME_STATE_MAIN_MENU'):
    config.GAME_STATE_MAIN_MENU = "main_menu"
if not hasattr(config, 'GAME_STATE_GAMEPLAY'):
    config.GAME_STATE_GAMEPLAY = "gameplay"
if not hasattr(config, 'GAME_STATE_PAUSE'):
    config.GAME_STATE_PAUSE = "pause"
if not hasattr(config, 'GAME_STATE_LEVEL_TRANSITION'):
    config.GAME_STATE_LEVEL_TRANSITION = "level_transition"
if not hasattr(config, 'GAME_STATE_GAME_OVER'):
    config.GAME_STATE_GAME_OVER = "game_over"

# Local definition for GAME_STATE_STARTUP (not provided in config)
GAME_STATE_STARTUP = "startup"

# DummyScreen class to simulate a screen object for UI initialization
class DummyScreen:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height

# Note: The ui.initialize_menu function should be implemented in ui.py.
# It should initialize the main menu interface by setting up UI elements such as buttons, icons,
# and other components necessary to allow user interaction with the main menu.
# This file assumes that ui.initialize_menu is implemented and available and now takes one parameter: screen.

class StateManager:
    def __init__(self):
        self.current_state = GAME_STATE_STARTUP
        # Create a dummy screen object for UI that supports get_width() and get_height()
        self.screen = DummyScreen()
        self.initialize_state()
    
    def change_state(self, new_state):
        self.current_state = new_state
        self.initialize_state()
    
    def initialize_state(self):
        if self.current_state == GAME_STATE_STARTUP:
            print("Initializing systems for STARTUP state.")
            # Placeholder for any startup initialization.
        elif self.current_state == config.GAME_STATE_MAIN_MENU:
            print("Initializing UI and Audio for MAIN MENU.")
            ui.initialize_menu(self.screen)
            audio.initialize_menu()
        elif self.current_state == config.GAME_STATE_GAMEPLAY:
            print("Initializing Maze, Game Objects, Ghost AI, Collision, Audio and UI for GAMEPLAY.")
            maze.initialize_maze()
            game_objects.initialize_objects()
            ghost_ai.initialize_ai()
            collision.initialize_collision()
            audio.initialize_gameplay()
            ui.initialize_gameplay()
        elif self.current_state == config.GAME_STATE_PAUSE:
            print("Pausing game. Maintaining current gameplay state for resume.")
            audio.pause_audio()
            ui.show_pause_screen()
        elif self.current_state == config.GAME_STATE_LEVEL_TRANSITION:
            print("Initializing Level Transition: Preparing new level.")
            ui.initialize_level_transition()
            audio.play_level_transition()
        elif self.current_state == config.GAME_STATE_GAME_OVER:
            print("Game Over. Cleaning up and showing final screen.")
            ui.show_game_over()
            audio.play_game_over()
        else:
            print("Unknown state encountered.")
    
    def start(self):
        if self.current_state == GAME_STATE_STARTUP:
            self.change_state(config.GAME_STATE_MAIN_MENU)
        else:
            print("Start method called in wrong state.")
    
    def start_gameplay(self):
        if self.current_state == config.GAME_STATE_MAIN_MENU:
            self.change_state(config.GAME_STATE_GAMEPLAY)
        else:
            print("start_gameplay can only be called from MAIN_MENU.")
    
    def pause_game(self):
        if self.current_state == config.GAME_STATE_GAMEPLAY:
            self.change_state(config.GAME_STATE_PAUSE)
        else:
            print("pause_game can only be called from GAMEPLAY.")
    
    def resume_game(self):
        if self.current_state == config.GAME_STATE_PAUSE:
            audio.resume_audio()
            ui.hide_pause_screen()
            self.change_state(config.GAME_STATE_GAMEPLAY)
        else:
            print("resume_game can only be called from PAUSE.")
    
    def level_transition(self):
        if self.current_state == config.GAME_STATE_GAMEPLAY:
            self.change_state(config.GAME_STATE_LEVEL_TRANSITION)
            time.sleep(0.1)
            self.change_state(config.GAME_STATE_GAMEPLAY)
        else:
            print("level_transition can only be initiated from GAMEPLAY.")
    
    def game_over(self):
        self.change_state(config.GAME_STATE_GAME_OVER)
    
    def update_state(self, event):
        if event == "start_game":
            self.start_gameplay()
        elif event == "pause":
            self.pause_game()
        elif event == "resume":
            self.resume_game()
        elif event == "level_complete":
            self.level_transition()
        elif event == "game_over":
            self.game_over()
        else:
            print("Received invalid event:", event)
    
    def update(self, delta_time):
        if self.current_state == config.GAME_STATE_GAMEPLAY:
            input_handler.process_input()
            game_objects.update(delta_time)
            ghost_ai.update(delta_time)
            collision.check_collisions()
            ui.render_gameplay()
            audio.update_audio()
        elif self.current_state == config.GAME_STATE_PAUSE:
            ui.render_pause_screen()
        elif self.current_state == config.GAME_STATE_MAIN_MENU:
            ui.render_menu()
    
    def terminate(self):
        print("Terminating game and cleaning up resources.")
        audio.stop_audio()
        ui.cleanup()
        maze.cleanup()
        game_objects.cleanup()
        ghost_ai.cleanup()
        collision.cleanup()

def main():
    # Define local state variables for testing.
    startup_state = GAME_STATE_STARTUP
    main_menu_state = config.GAME_STATE_MAIN_MENU
    gameplay_state = config.GAME_STATE_GAMEPLAY
    pause_state = config.GAME_STATE_PAUSE
    level_transition_state = config.GAME_STATE_LEVEL_TRANSITION
    game_over_state = config.GAME_STATE_GAME_OVER

    # Create instance of StateManager.
    sm = StateManager()
    # Test initial state is STARTUP.
    assert sm.current_state == startup_state, "Initial state should be STARTUP."
    
    # Test start() transitions from STARTUP to MAIN_MENU.
    sm.start()
    assert sm.current_state == main_menu_state, "State should transition to MAIN_MENU after start()."
    
    # Test start_gameplay transitions from MAIN_MENU to GAMEPLAY.
    sm.start_gameplay()
    assert sm.current_state == gameplay_state, "State should transition to GAMEPLAY after start_gameplay()."
    
    # Test pause_game from GAMEPLAY to PAUSE.
    sm.update_state("pause")
    assert sm.current_state == pause_state, "State should be PAUSE after pause event."
    
    # Test resume_game transitions from PAUSE back to GAMEPLAY.
    sm.update_state("resume")
    assert sm.current_state == gameplay_state, "State should resume to GAMEPLAY after resume event."
    
    # Test level transition from GAMEPLAY.
    sm.update_state("level_complete")
    assert sm.current_state == gameplay_state, "After level transition, state should be GAMEPLAY."
    
    # Test game over transition.
    sm.update_state("game_over")
    assert sm.current_state == game_over_state, "State should be GAME_OVER after game_over event."
    
    # Test update method for MAIN_MENU.
    sm.change_state(main_menu_state)
    sm.update(0.016)  # Assuming 60 FPS frame time
    
    # Test update method for GAMEPLAY.
    sm.change_state(gameplay_state)
    sm.update(0.016)
    
    # Test update method for PAUSE.
    sm.change_state(pause_state)
    sm.update(0.016)
    
    # Test terminate/cleanup.
    sm.terminate()
    
    print("All state transitions and methods have been tested successfully.")

if __name__ == "__main__":
    main()