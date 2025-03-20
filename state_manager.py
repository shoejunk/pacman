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

GAME_STATE_STARTUP = "startup"

class DummyScreen:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height

class StateManager:
    def __init__(self):
        self.current_state = GAME_STATE_STARTUP
        self.screen = DummyScreen()
        try:
            audio.manager = audio.AudioManager()
        except Exception as e:
            print("Warning: Could not instantiate AudioManager:", e)
        try:
            self.ui_manager = ui.UIManager(self.screen)
        except Exception as e:
            print("Warning: Could not instantiate UIManager:", e)
            self.ui_manager = None
        self.initialize_state()
    
    def change_state(self, new_state):
        self.current_state = new_state
        self.initialize_state()
    
    def initialize_state(self):
        if self.current_state == GAME_STATE_STARTUP:
            print("Initializing systems for STARTUP state.")
        elif self.current_state == config.GAME_STATE_MAIN_MENU:
            print("Initializing UI and Audio for MAIN MENU.")
            if self.ui_manager:
                self.ui_manager.initialize_menu()
            else:
                ui.initialize_menu(self.screen)
            audio.initialize_menu()
        elif self.current_state == config.GAME_STATE_GAMEPLAY:
            print("Initializing Maze, Game Objects, Ghost AI, Collision, Audio and UI for GAMEPLAY.")
            maze.initialize_maze()
            game_objects.initialize_objects()
            ghost_ai.initialize_ai()
            if not hasattr(maze, "get_cell") or not callable(maze.get_cell):
                maze.get_cell = lambda x, y: None
            collision.initialize_collision(config, maze)
            audio.initialize_gameplay()
            audio.initialized = True
            if self.ui_manager:
                self.ui_manager.initialize_gameplay()
            else:
                ui.initialize_gameplay()
        elif self.current_state == config.GAME_STATE_PAUSE:
            print("Pausing game. Maintaining current gameplay state for resume.")
            audio.pause_audio()
            if self.ui_manager:
                self.ui_manager.show_pause_screen()
            else:
                ui.show_pause_screen()
        elif self.current_state == config.GAME_STATE_LEVEL_TRANSITION:
            print("Initializing Level Transition: Preparing new level.")
            if self.ui_manager:
                self.ui_manager.initialize_level_transition()
            else:
                ui.initialize_level_transition()
            audio.play_level_transition()
        elif self.current_state == config.GAME_STATE_GAME_OVER:
            print("Game Over. Cleaning up and showing final screen.")
            if self.ui_manager:
                self.ui_manager.show_game_over()
            else:
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
            if self.ui_manager:
                self.ui_manager.hide_pause_screen()
            else:
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
            if self.ui_manager:
                self.ui_manager.render_gameplay()
            else:
                ui.render_gameplay()
            audio.update_audio()
        elif self.current_state == config.GAME_STATE_PAUSE:
            if self.ui_manager:
                self.ui_manager.render_pause_screen()
            else:
                ui.render_pause_screen()
        elif self.current_state == config.GAME_STATE_MAIN_MENU:
            if self.ui_manager:
                self.ui_manager.render_menu()
            else:
                ui.render_menu()
    
    def terminate(self):
        print("Terminating game and cleaning up resources")

def main():
    sm = StateManager()
    # Test transition from startup to main menu.
    sm.start()
    assert sm.current_state == config.GAME_STATE_MAIN_MENU, "State should be MAIN_MENU after start()"
    # Test starting gameplay from main menu