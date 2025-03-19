# Technical Document

## Project Overview

This document outlines the technical implementation of the project based on the design document. It includes a list of all files needed, their dependencies, and what each file should do.

## Table of Contents

1. [File Structure](#file-structure)
2. [Dependency Graph](#dependency-graph)
3. [File Details](#file-details)

## File Structure

The project consists of the following files:

- `game.py`
- `state_manager.py`
- `ui.py`
- `audio.py`
- `input_handler.py`
- `collision.py`
- `ghost_ai.py`
- `game_objects.py`
- `maze.py`
- `config.py`

## Dependency Graph

The following diagram shows the dependencies between files:

```
game (no dependencies)
state_manager (no dependencies)
ui (no dependencies)
audio (no dependencies)
input_handler (no dependencies)
collision (no dependencies)
ghost_ai (no dependencies)
game_objects (no dependencies)
maze (no dependencies)
config (no dependencies)
```

## File Details

### game.py

• Purpose: Serves as the main entry point and game loop controller for the Pac-Man game.
• Key Classes/Functions:
– The main() function which initializes Pygame, loads all required modules, and sets up the game window.
– The main game loop that continuously processes input (via input_handler.py), updates game logic (using state_manager.py), renders graphics (maze.py, game_objects.py, ui.py), handles collisions (collision.py), and plays audio (audio.py).
• Interaction:
– Aggregates all other modules (config.py, maze.py, game_objects.py, ghost_ai.py, collision.py, input_handler.py, audio.py, ui.py, and state_manager.py).
– Serves as the tying point where all event handling and state management converge.
• Implementation Details:
– Ensure proper initialization and graceful shutdown (including Pygame quit routines).
– Maintain fixed time steps or frame rate control (using config.py FPS settings) to ensure smooth game performance.
DEPENDECIES: config.py, maze.py, game_objects.py, ghost_ai.py, collision.py, input_handler.py, audio.py, ui.py, state_manager.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Run game.py and verify that the startup splash screen loads, then the main menu appears and user input transitions correctly between states. – Step 2: During gameplay, test that movements, collisions, ghost behaviors, power-up effects, UI updates, and audio feedback occur as expected. – Step 3: Simulate edge cases (e.g., rapid state changes, no input, window focus loss) to ensure the game handles them without crashing and maintains game state integrity.

### state_manager.py

• Purpose: Manages the overall flow and state transitions of the game including startup, main menu, gameplay, pause, level transitions, and game over.
• Key Classes/Functions:
– StateManager class that holds the current game state and handles transitions between them.
– Functions for starting, pausing, updating, and terminating game states.
– Methods to initialize the appropriate modules (UI, audio, maze, etc.) based on state changes.
• Interaction:
– Combines input from input_handler.py, gameplay updates from game_objects.py and ghost_ai.py, UI rendering from ui.py, and audio cues from audio.py.
– Uses config.py for game state constants.
• Implementation Details:
– Clear separation of state-specific logic to avoid intermingling menus and gameplay code.
– Establish timed transitions (e.g., power pellet effects, ghost vulnerability duration, level transitions) and ensure they reset properly on state exit.
DEPENDECIES: config.py, input_handler.py, game_objects.py, maze.py, ghost_ai.py, ui.py, audio.py, collision.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Launch the game and simulate transitions between states (e.g., main menu → gameplay → pause → resume) verifying that state changes occur smoothly. – Step 2: Trigger events (e.g., life loss, level completion) and confirm that the state manager correctly initiates transitions such as Game Over or Level Transition screens. – Step 3: Intentionally input invalid state changes (simulate rapid state toggle) to test for robustness and correct handling of edge cases.
------------------------------------------------------------------

### ui.py

• Purpose: Manages all aspects of the user interface including HUD elements, score display, lives counter, level indicator, and menus (main, pause, and game over).
• Key Classes/Functions:
– UIManager class that renders HUD elements based on game state (score, lives, level).
– Functions/classes to create and handle menu selections (start, options, high scores, pause, restart, quit).
– Functions for drawing popups such as level transition screens and game-over screens.
• Interaction:
– Uses configuration settings (fonts, colors, positions) from config.py.
– Invoked by state_manager.py to display the appropriate UI based on the current game state.
• Implementation Details:
– Ensure UI elements are clear and continuously updated.
– Use layered rendering to draw UI components on top of gameplay without obstructing essential visuals.
DEPENDECIES: config.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Render each HUD element on a blank canvas and verify correct positioning and styling. – Step 2: Simulate menu navigation to check that selections are highlighted and input events are handled correctly. – Step 3: Change game state (e.g., from GAMEPLAY to PAUSE) and verify that the appropriate UI elements appear.
------------------------------------------------------------------

### audio.py

• Purpose: Handles loading, managing, and playing sound effects and background music.
• Key Classes/Functions:
– AudioManager class to load sound assets (e.g., pellet consumption, ghost encounter sounds, power-up activation, life loss, etc.).
– Functions to play, pause, and loop background music as well as play one-off sounds based on game events.
• Interaction:
– Invoked by state_manager.py and game_objects.py when specific events occur (e.g., Pac-Man consuming a pellet, ghost eaten, game over).
– Uses configuration constants from config.py for asset file paths and volume settings.
• Implementation Details:
– Preload assets during initialization for faster playback during gameplay.
– Use Pygame’s mixer module or a similar library to manage audio streams.
DEPENDECIES: config.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Initialize AudioManager in isolation and trigger playback for each sound, confirming that the correct audio file is played. – Step 2: Verify that background music loops seamlessly without noticeable gaps. – Step 3: Adjust volume settings from config.py and check that changes are reflected in playback.
------------------------------------------------------------------

### input_handler.py

• Purpose: Manages and processes keyboard input for controlling Pac-Man and navigating menus.
• Key Classes/Functions:
– InputHandler class that encapsulates input polling using Pygame’s event system.
– Functions/methods to map arrow key presses to direction changes for Pac-Man and menu selections.
• Interaction:
– Used by state_manager.py and game.py during the main loop to react to user input.
– Relies on configuration settings from config.py (e.g., key mapping constants).
• Implementation Details:
– Ensure that input is processed continuously and responsively.
– Debounce or buffer inputs when required to avoid multiple rapid transitions.
DEPENDECIES: config.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Run a test harness that prints the detected key presses and verifies correct mapping (e.g., arrow keys yielding the appropriate direction). – Step 2: Check the behavior during rapid sequential key presses to ensure the inputs are handled correctly. – Step 3: Test input during different game states (gameplay vs. menu) to verify context-sensitive behavior.
------------------------------------------------------------------

### collision.py

• Purpose: Provides functions and classes for detecting and handling collisions between game objects (Pac-Man, Ghosts, Pellets, Bonus Items, and Maze walls).
• Key Classes/Functions:
– Functions to detect grid-based collisions based on object positions and maze cell values.
– Collision resolution functions to handle outcome (e.g., losing a life, consuming a pellet, or eating a ghost).
• Interaction:
– Utilizes position information from game_objects.py and the maze layout from maze.py.
– Calls configuration values from config.py to determine cell sizes and tolerances for collision detection.
• Implementation Details:
– Perform collision checks only when entities are approximately aligned with the grid.
– Use efficient algorithms (e.g., bounding box checks) to keep processing fast during game loops.
DEPENDECIES: config.py, maze.py, game_objects.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Simulate a collision scenario where Pac-Man’s position overlaps a pellet position and verify that the pellet is marked as consumed and the score updates. – Step 2: Test collisions between Pac-Man and a ghost in both normal and vulnerable states to ensure proper event triggering. – Step 3: Check that no collision is detected when entities are near but not overlapping grid cells, ensuring precision.
------------------------------------------------------------------

### ghost_ai.py

• Purpose: Implements the artificial intelligence strategies for the ghost characters.
• Key Classes/Functions:
– AI strategy functions for each ghost (for example, chase strategy for Blinky, ambush strategy for Pinky, unpredictable movement for Inky, and dual-behavior for Clyde).
– A function to update ghost movements based on the current game state (normal or vulnerable).
• Interaction:
– Works directly with the Ghost classes from game_objects.py by updating their target positions and speed adjustments.
– Uses configuration constants (e.g., speeds, timers) from config.py.
• Implementation Details:
– Encapsulate AI logic in separate functions or strategies that can be easily modified or extended.
– Incorporate timer-based events to switch states (e.g., switching ghost behavior after PacMan eats a power pellet).
DEPENDECIES: config.py, game_objects.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Set up a controlled scenario with PacMan in a fixed position and verify ghost target calculation (e.g., Blinky directly chasing PacMan). – Step 2: Trigger power pellet state and check that ghost speeds and target behaviors switch. – Step 3: Simulate movement over several game ticks and log positions to verify that AI movement changes are as expected.
------------------------------------------------------------------

### game_objects.py

• Purpose: Defines all the primary in-game entities such as Pac-Man, Ghosts, Pellets, and Bonus Items.
• Key Classes/Functions:
– PacMan class (attributes: position, direction, lives, score; methods: move, draw, update).
– Ghost base class with subclasses for Blinky, Pinky, Inky, and Clyde (attributes: position, state, speed; methods: move, update, draw).
– Pellet class and BonusItem class, each with attributes for position and collected state and methods for drawing.
• Interaction:
– Imports config.py for speed and sprite sizes.
– Maze from maze.py is referenced during collision detection and pellet consumption.
– Ghost AI behavior (typically managed in ghost_ai.py) can be integrated as methods or injected strategies.
• Implementation Details:
– Use inheritance for ghosts to encapsulate common behavior and override for individual strategies.
– Ensure that drawing functions are optimized for the 2D rendering context.
DEPENDECIES: config.py, maze.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Instantiate PacMan and ghost objects; update their positions using simulated input and verify movement. – Step 2: Place pellets in the maze and simulate PacMan passing over them to confirm proper state changes and score updates. – Step 3: Test ghost objects by toggling between normal and vulnerable states and checking that drawing functions change the sprite color.
------------------------------------------------------------------

### maze.py

• Purpose: Defines the maze structure including wall placements, pellet positions, and special tunnels (wrap-around areas).
• Key Contents:
– Maze class that loads a fixed 2D grid layout from a text file or hard-coded array.
– Methods to query cell content (wall, pellet, empty space, tunnel) and modify pellet existence during gameplay.
– Functions to render the maze layout onto the screen using the provided configuration.
• Interaction:
– Uses configuration constants from config.py to determine grid size and drawing parameters.
– Its API is used by state_manager.py and game_objects.py (e.g., for collision detection).
• Implementation Details:
– Maintain an internal 2D list or matrix representing the maze.
– Include helper functions for coordinate transformations between grid positions and screen positions.
DEPENDECIES: config.py

**Dependencies:** None

**Testing Steps:**

– Step 1: Create an instance of Maze and call its function to print a textual or graphical representation of the layout. – Step 2: Verify correct pellet count before and after consumption. – Step 3: Test wrap-around functionality by querying tunnel cells.
------------------------------------------------------------------

### config.py

• Purpose: Stores all global constants and configuration settings used across the game.
• Key Contents:
– Variables for screen dimensions, FPS, grid size, colors, sprite sizes, asset file paths, and gameplay constants (e.g., speed values, ghost behavior timings).
– Enumerations for game states (STARTUP, MAIN_MENU, GAMEPLAY, PAUSE, GAME_OVER, LEVEL_TRANSITION).
• Interaction:
– All other modules import config.py to access shared settings.
• Implementation Details:
– Centralized location for tweaking game parameters without changing code across multiple files.
– Use Python constants (and possibly Enum classes for state management) to organize settings.
DEPENDECIES: none

**Dependencies:** None

**Testing Steps:**

– Step 1: Import config.py in an interactive shell and print key constants such as SCREEN_WIDTH, SCREEN_HEIGHT. – Step 2: Change a constant value and verify that modules using it reflect the modification. – Step 3: Use assertions in config.py to verify value ranges (e.g., positive screen dimensions).
------------------------------------------------------------------

