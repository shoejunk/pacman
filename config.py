#!/usr/bin/env python3
from enum import Enum

# Global constants and configuration settings

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Grid and sprite settings
GRID_SIZE = 32
GRID_TOLERANCE = 5  # Added GRID_TOLERANCE per requirements
CELL_SIZE = 32    # Added constant per requirements
SPRITE_WIDTH = 32
SPRITE_HEIGHT = 32

# Colors (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

# Asset file paths
IMAGE_PLAYER_PATH = "assets/player.png"
IMAGE_GHOST_PATH = "assets/ghost.png"
IMAGE_WALL_PATH = "assets/wall.png"
SOUND_EFFECT_PATH = "assets/sound_effect.wav"

# Audio asset file paths and volume settings
AUDIO_PELLET_SOUND = "assets/sounds/pellet.wav"
AUDIO_GHOST_ENCOUNTER_SOUND = "assets/sounds/ghost_encounter.wav"
AUDIO_POWERUP_SOUND = "assets/sounds/powerup.wav"
AUDIO_LIFE_LOSS_SOUND = "assets/sounds/life_loss.wav"
BACKGROUND_MUSIC = "assets/music/background.mp3"
SOUND_VOLUME = 0.7
MUSIC_VOLUME = 0.5

# Gameplay constants
PLAYER_SPEED = 5.0  # pixels per frame
GHOST_SPEED = 2.5   # pixels per frame
GHOST_BEHAVIOR_TIMING = 5.0  # seconds for behavior switch

# HUD and UI settings
SCORE_POS = (10, 10)
LIVES_POS = (10, 50)
LEVEL_POS = (10, 90)
HUD_FONT = "assets/fonts/hud_font.ttf"
MENU_FONT = "assets/fonts/menu_font.ttf"
FONT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 215, 0)
POPUP_COLOR = (200, 200, 200)
POPUP_RECT = (100, 100, 600, 400)

# Enumerations for game states
class GameState(Enum):
    STARTUP = 0
    MAIN_MENU = 1
    GAMEPLAY = 2
    PAUSE = 3
    GAME_OVER = 4
    LEVEL_TRANSITION = 5

# Assertions to ensure value ranges
assert SCREEN_WIDTH > 0, "SCREEN_WIDTH must be positive."
assert SCREEN_HEIGHT > 0, "SCREEN_HEIGHT must be positive."
assert GRID_SIZE > 0, "GRID_SIZE must be positive."
assert GRID_TOLERANCE >= 0, "GRID_TOLERANCE must be zero or positive."
assert CELL_SIZE > 0, "CELL_SIZE must be positive."
assert PLAYER_SPEED > 0, "PLAYER_SPEED must be positive."
assert GHOST_SPEED > 0, "GHOST_SPEED must be positive."
assert GHOST_BEHAVIOR_TIMING > 0, "GHOST_BEHAVIOR_TIMING must be positive."
assert isinstance(SOUND_VOLUME, float) and 0.0 <= SOUND_VOLUME <= 1.0, "SOUND_VOLUME must be a float between 0 and 1."
assert isinstance(MUSIC_VOLUME, float) and 0.0 <= MUSIC_VOLUME <= 1.0, "MUSIC_VOLUME must be a float between 0 and 1."

def main():
    global SCREEN_WIDTH
    # Testing and demonstration of configuration settings and GameState enum

    # Test screen dimensions and FPS
    print("Testing screen settings:")
    print("SCREEN_WIDTH =", SCREEN_WIDTH)
    print("SCREEN_HEIGHT =", SCREEN_HEIGHT)
    print("FPS =", FPS)
    assert SCREEN_WIDTH == 800, "Expected SCREEN_WIDTH to be 800."
    assert SCREEN_HEIGHT == 600, "Expected SCREEN_HEIGHT to be 600."
    assert FPS == 60, "Expected FPS to be 60."

    # Test grid, cell, sprite dimensions and tolerance
    print("\nTesting grid, cell, sprite settings and grid tolerance:")
    print("GRID_SIZE =", GRID_SIZE)
    print("GRID_TOLERANCE =", GRID_TOLERANCE)
    print("CELL_SIZE =", CELL_SIZE)
    print("SPRITE_WIDTH =", SPRITE_WIDTH)
    print("SPRITE_HEIGHT =", SPRITE_HEIGHT)
    assert GRID_SIZE == 32, "Expected GRID_SIZE to be 32."
    assert GRID_TOLERANCE == 5, "Expected GRID_TOLERANCE to be 5."
    assert CELL_SIZE == 32, "Expected CELL_SIZE to be 32."
    assert SPRITE_WIDTH == 32, "Expected SPRITE_WIDTH to be 32."
    assert SPRITE_HEIGHT == 32, "Expected SPRITE_HEIGHT to be 32."

    # Test color definitions
    print("\nTesting color values:")
    print("COLOR_BLACK =", COLOR_BLACK)
    print("COLOR_WHITE =", COLOR_WHITE)
    print("COLOR_RED =", COLOR_RED)
    print("COLOR_GREEN =", COLOR_GREEN)
    print("COLOR_BLUE =", COLOR_BLUE)
    assert isinstance(COLOR_BLACK, tuple) and len(COLOR_BLACK) == 3, "COLOR_BLACK should be an RGB tuple."
    assert COLOR_WHITE == (255, 255, 255), "COLOR_WHITE should be (255, 255, 255)."

    # Test asset file paths
    print("\nTesting asset file paths:")
    print("IMAGE_PLAYER_PATH =", IMAGE_PLAYER_PATH)
    print("IMAGE_GHOST_PATH =", IMAGE_GHOST_PATH)
    print("IMAGE_WALL_PATH =", IMAGE_WALL_PATH)
    print("SOUND_EFFECT_PATH =", SOUND_EFFECT_PATH)
    for path in [IMAGE_PLAYER_PATH, IMAGE_GHOST_PATH, IMAGE_WALL_PATH, SOUND_EFFECT_PATH]:
        assert isinstance(path, str) and path != "", "Asset paths should be non-empty strings."

    # Test audio asset file paths and volume settings
    print("\nTesting audio settings:")
    print("AUDIO_PELLET_SOUND =", AUDIO_PELLET_SOUND)
    print("AUDIO_GHOST_ENCOUNTER_SOUND =", AUDIO_GHOST_ENCOUNTER_SOUND)
    print("AUDIO_POWERUP_SOUND =", AUDIO_POWERUP_SOUND)
    print("AUDIO_LIFE_LOSS_SOUND =", AUDIO_LIFE_LOSS_SOUND)
    print("BACKGROUND_MUSIC =", BACKGROUND_MUSIC)
    print("SOUND_VOLUME =", SOUND_VOLUME)
    print("MUSIC_VOLUME =", MUSIC_VOLUME)
    for path in [AUDIO_PELLET_SOUND, AUDIO_GHOST_ENCOUNTER_SOUND, AUDIO_POWERUP_SOUND, AUDIO_LIFE_LOSS_SOUND, BACKGROUND_MUSIC]:
        assert isinstance(path, str) and path != "", "Audio asset paths should be non-empty strings."
    assert 0.0 <= SOUND_VOLUME <= 1.0, "SOUND_VOLUME must be between 0 and 1."
    assert 0.0 <= MUSIC_VOLUME <= 1.0, "MUSIC_VOLUME must be between 0 and 1."

    # Test gameplay constants
    print("\nTesting gameplay constants:")
    print("PLAYER_SPEED =", PLAYER_SPEED)
    print("GHOST_SPEED =", GHOST_SPEED)
    print("GHOST_BEHAVIOR_TIMING =", GHOST_BEHAVIOR_TIMING)
    assert PLAYER_SPEED > 0, "PLAYER_SPEED should be positive."
    assert GHOST_SPEED > 0, "GHOST_SPEED should be positive."
    assert GHOST_BEHAVIOR_TIMING > 0, "GHOST_BEHAVIOR_TIMING should be positive."

    # Test HUD and UI settings
    print("\nTesting HUD and UI settings:")
    print("SCORE_POS =", SCORE_POS)
    print("LIVES_POS =", LIVES_POS)
    print("LEVEL_POS =", LEVEL_POS)
    print("HUD_FONT =", HUD_FONT)
    print("MENU_FONT =", MENU_FONT)
    print("FONT_COLOR =", FONT_COLOR)
    print("HIGHLIGHT_COLOR =", HIGHLIGHT_COLOR)
    print("POPUP_COLOR =", POPUP_COLOR)
    print("POPUP_RECT =", POPUP_RECT)
    for pos in [SCORE_POS, LIVES_POS, LEVEL_POS]:
        assert isinstance(pos, tuple) and len(pos) == 2, "HUD positions should be tuples of (x, y)."
    for font in [HUD_FONT, MENU_FONT]:
        assert isinstance(font, str) and font != "", "Font paths should be non-empty strings."
    for color in [FONT_COLOR, HIGHLIGHT_COLOR, POPUP_COLOR]:
        assert isinstance(color, tuple) and len(color) == 3, "Font and highlight colors should be RGB tuples."
    assert isinstance(POPUP_RECT, tuple) and len(POPUP_RECT) == 4, "POPUP_RECT should be a tuple of 4 values."

    # Test GameState enum
    print("\nTesting GameState enum:")
    gs_startup = GameState.STARTUP
    gs_gameplay = GameState.GAMEPLAY
    print("GameState.STARTUP =", gs_startup)
    print("GameState.GAMEPLAY =", gs_gameplay)
    assert gs_startup.value == 0, "GameState.STARTUP should have value 0."
    assert gs_gameplay.value == 2, "GameState.GAMEPLAY should have value 2."
    # Iterate through all states
    for state in GameState:
        print(f"{state.name} = {state.value}")

    # Test modification of a global constant
    print("\nTesting modification of global constant SCREEN_WIDTH:")
    original_width = SCREEN_WIDTH
    SCREEN_WIDTH = 1024
    print("Modified SCREEN_WIDTH =", SCREEN_WIDTH)
    assert SCREEN_WIDTH == 1024, "SCREEN_WIDTH should be updated to 1024."
    # Reset SCREEN_WIDTH
    SCREEN_WIDTH = original_width
    print("Reset SCREEN_WIDTH =", SCREEN_WIDTH)
    assert SCREEN_WIDTH == 800, "SCREEN_WIDTH should be reset to 800."

    print("\nAll configuration tests passed.")

if __name__ == "__main__":
    main()