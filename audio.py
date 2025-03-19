import pygame
import os
import time
from config import AUDIO_PELLET_SOUND, AUDIO_GHOST_ENCOUNTER_SOUND, AUDIO_POWERUP_SOUND, AUDIO_LIFE_LOSS_SOUND, BACKGROUND_MUSIC, SOUND_VOLUME, MUSIC_VOLUME

class AudioManager:
    def __init__(self):
        # Initialize pygame mixer with pre_init before full init for reduced latency
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        # Set music volume from config
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        # Preload sound effects into a dictionary
        self.sounds = {}
        self.sounds['pellet'] = self.load_sound(AUDIO_PELLET_SOUND)
        self.sounds['ghost_encounter'] = self.load_sound(AUDIO_GHOST_ENCOUNTER_SOUND)
        self.sounds['powerup'] = self.load_sound(AUDIO_POWERUP_SOUND)
        self.sounds['life_loss'] = self.load_sound(AUDIO_LIFE_LOSS_SOUND)
        # Set volume for each sound effect based on config
        for key in self.sounds:
            self.sounds[key].set_volume(SOUND_VOLUME)

    def load_sound(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError("Sound file not found: " + filepath)
        return pygame.mixer.Sound(filepath)

    def play_sound(self, sound_name):
        if sound_name not in self.sounds:
            raise ValueError("No sound loaded for event: " + sound_name)
        self.sounds[sound_name].play()

    def play_background_music(self, loop=True):
        if not os.path.exists(BACKGROUND_MUSIC):
            raise FileNotFoundError("Background music file not found: " + BACKGROUND_MUSIC)
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        loops = -1 if loop else 0
        pygame.mixer.music.play(loops=loops)

    def pause_background_music(self):
        pygame.mixer.music.pause()

    def unpause_background_music(self):
        pygame.mixer.music.unpause()

    def stop_background_music(self):
        pygame.mixer.music.stop()

def main():
    # Initialize AudioManager instance
    audio_manager = AudioManager()

    # Test: All sound assets should be loaded correctly
    expected_sounds = ['pellet', 'ghost_encounter', 'powerup', 'life_loss']
    for sound_key in expected_sounds:
        assert sound_key in audio_manager.sounds, "Sound {} not loaded.".format(sound_key)
        assert isinstance(audio_manager.sounds[sound_key], pygame.mixer.Sound), \
            "Loaded asset for {} is not a pygame Sound.".format(sound_key)

    # Test: Play each sound effect
    try:
        for sound_key in expected_sounds:
            audio_manager.play_sound(sound_key)
            # Wait a short moment to allow the sound to play
            time.sleep(0.5)
    except Exception as e:
        assert False, "Playing sound {} raised an exception: {}".format(sound_key, e)

    # Test: Background music playback, pause (check if paused), unpause, and stop.
    try:
        audio_manager.play_background_music(loop=True)
        # Allow time for music to start
        time.sleep(1)
        # Check if music is playing
        assert pygame.mixer.music.get_busy(), "Background music should be playing after play_background_music call."

        # Capture current music position
        pos_before_pause = pygame.mixer.music.get_pos()
        audio_manager.pause_background_music()
        # Wait to see if position remains the same (since paused, time should not progress)
        time.sleep(1)
        pos_after_pause = pygame.mixer.music.get_pos()
        # pygame.mixer.music.get_pos() may return -1 if the music is not playing,
        # so we allow for that case; otherwise, ensure that the position did not increase.
        if pos_before_pause != -1 and pos_after_pause != -1:
            assert pos_after_pause == pos_before_pause, "Background music position should not change when paused."

        audio_manager.unpause_background_music()
        time.sleep(1)
        pos_after_unpause = pygame.mixer.music.get_pos()
        if pos_after_unpause != -1 and pos_after_pause != -1:
            assert pos_after_unpause > pos_after_pause, "Background music position should advance after unpausing."

        audio_manager.stop_background_music()
        time.sleep(0.5)
        assert not pygame.mixer.music.get_busy(), "Background music should be stopped after stop_background_music call."
    except Exception as e:
        assert False, "Background music operations raised an exception: {}".format(e)

    print("All tests passed successfully.")
    # Quit pygame mixer and pygame
    pygame.mixer.quit()
    pygame.quit()

if __name__ == "__main__":
    main()