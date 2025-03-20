#!/usr/bin/env python3
import time
import config

class AudioManager:
    _instance = None

    def __init__(self):
        self._music_paused = False
        self._paused_position = 0.0
        self._start_time = None
        self.volume = getattr(config, 'MUSIC_VOLUME', 1.0)
        AudioManager._instance = self
        self.play_background_music()

    def play_background_music(self):
        print("Background music started playing.")
        self._start_time = time.time()
        self._paused_position = 0.0
        self._music_paused = False

    def pause_background_music(self):
        if not self._music_paused and self._start_time is not None:
            self._paused_position = time.time() - self._start_time
            self._music_paused = True
            print("Background music paused at position", self._paused_position)

    def resume_audio(self):
        if self._music_paused:
            self._start_time = time.time() - self._paused_position
            self._music_paused = False
            print("Background music resumed from position", self._paused_position)

    def get_music_position(self):
        if self._music_paused:
            return self._paused_position
        else:
            if self._start_time is None:
                return 0.0
            return time.time() - self._start_time

    def update_audio(self):
        # In a real implementation, this would update the audio stream.
        pass

    def initialize_gameplay(self):
        print("AudioManager gameplay initialized.")
        self.play_background_music()

def initialize_menu():
    print("Menu initialized.")

def initialize_gameplay():
    print("Gameplay initialized.")

def pause_audio():
    if AudioManager._instance:
        AudioManager._instance.pause_background_music()
    else:
        raise Exception("AudioManager instance not initialized.")

def resume_audio():
    if AudioManager._instance:
        AudioManager._instance.resume_audio()
    else:
        raise Exception("AudioManager instance not initialized.")

def update_audio():
    if AudioManager._instance:
        AudioManager._instance.update_audio()
    else:
        print("AudioManager not initialized, update_audio doing nothing.")

def play_level_transition():
    print("Level transition sound played.")

def play_game_over():
    print("Game over sound played.")

def main():
    print("Testing Audio Module...")

    # Test the initialize_menu function
    initialize_menu()

    # Test the initialize_gameplay module-level function
    initialize_gameplay()

    # Create an instance of AudioManager and test background music playback
    am = AudioManager()
    time.sleep(0.1)
    pos1 = am.get_music_position()
    time.sleep(0.1)
    pos2 = am.get_music_position()
    assert pos2 > pos1, "Music position should increase when playing."

    # Test pausing background music using the AudioManager method
    pos_before_pause = am.get_music_position()
    am.pause_background_music()
    time.sleep(0.2)
    pos_after_pause = am.get_music_position()
    # Allow a small margin of error due to timing
    assert abs(pos_after_pause - pos_before_pause) < 0.01, "Background music position should not change when paused."

    # Test resuming background music using the AudioManager method
    am.resume_audio()
    pos_resume = am.get_music_position()
    time.sleep(0.2)
    pos_after_resume = am.get_music_position()
    assert pos_after_resume > pos_resume, "Background music position should increase after resume."

    # Test module-level pause_audio and resume_audio functions
    pause_audio()
    paused_pos = am.get_music_position()
    time.sleep(0.2)
    assert abs(am.get_music_position() - paused_pos) < 0.01, "Module pause_audio: position should remain same when paused."
    resume_audio()
    pos_module_resume = am.get_music_position()
    time.sleep(0.2)
    assert am.get_music_position() > pos_module_resume, "Module resume_audio: position should increase after resume."

    # Test update_audio function (should not change state)
    update_audio()

    # Test play_level_transition and play_game_over functions
    play_level_transition()
    play_game_over()

    print("All audio module tests passed.")

if __name__ == "__main__":
    main()