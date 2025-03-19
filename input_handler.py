import pygame
import config

class InputHandler:
    def __init__(self):
        pygame.init()
        self.debounce_threshold = 200  # in milliseconds
        self.last_pressed = {}
        # Key mapping from config, with defaults if not defined in config
        self.key_up = getattr(config, 'KEY_UP', pygame.K_UP)
        self.key_down = getattr(config, 'KEY_DOWN', pygame.K_DOWN)
        self.key_left = getattr(config, 'KEY_LEFT', pygame.K_LEFT)
        self.key_right = getattr(config, 'KEY_RIGHT', pygame.K_RIGHT)
        self.key_enter = getattr(config, 'KEY_ENTER', pygame.K_RETURN)

    def map_key_to_direction(self, key):
        if key == self.key_up:
            return "UP"
        elif key == self.key_down:
            return "DOWN"
        elif key == self.key_left:
            return "LEFT"
        elif key == self.key_right:
            return "RIGHT"
        else:
            return None

    def process_events(self, context="game"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"action": "quit"}
            if event.type == pygame.KEYDOWN:
                current_time = pygame.time.get_ticks()
                key = event.key
                if key in self.last_pressed and (current_time - self.last_pressed[key] < self.debounce_threshold):
                    continue
                self.last_pressed[key] = current_time

                if context == "game":
                    if key in [self.key_up, self.key_down, self.key_left, self.key_right]:
                        direction = self.map_key_to_direction(key)
                        return {"action": "move", "direction": direction}
                elif context == "menu":
                    if key in [self.key_up, self.key_down, self.key_left, self.key_right]:
                        direction = self.map_key_to_direction(key)
                        return {"action": "navigate", "direction": direction}
                    elif key == self.key_enter:
                        return {"action": "select", "selection": "enter"}
        return None

def main():
    # Initialize pygame display to allow event processing in tests.
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("InputHandler Test Harness")

    # Create an instance of InputHandler
    input_handler = InputHandler()

    # Clear any existing events
    pygame.event.clear()

    # Test 1: Game context, arrow key mapping (UP)
    test_event = pygame.event.Event(pygame.KEYDOWN, {'key': input_handler.key_up})
    pygame.event.post(test_event)
    result = input_handler.process_events(context="game")
    assert result is not None, "Failed to process KEYDOWN event in game context"
    assert result.get("action") == "move", "Expected action 'move' in game context"
    assert result.get("direction") == "UP", "Expected direction 'UP' for key_up event"

    # Test 2: Menu context, arrow key mapping (LEFT)
    pygame.event.clear()
    test_event = pygame.event.Event(pygame.KEYDOWN, {'key': input_handler.key_left})
    pygame.event.post(test_event)
    result = input_handler.process_events(context="menu")
    assert result is not None, "Failed to process KEYDOWN event in menu context"
    assert result.get("action") == "navigate", "Expected action 'navigate' in menu context"
    assert result.get("direction") == "LEFT", "Expected direction 'LEFT' for key_left event"

    # Test 3: Menu context, select action (ENTER)
    pygame.event.clear()
    test_event = pygame.event.Event(pygame.KEYDOWN, {'key': input_handler.key_enter})
    pygame.event.post(test_event)
    result = input_handler.process_events(context="menu")
    assert result is not None, "Failed to process KEYDOWN event for selection in menu context"
    assert result.get("action") == "select", "Expected action 'select' for key_enter event"
    assert result.get("selection") == "enter", "Expected selection 'enter' for key_enter event"

    # Test 4: Debounce check - rapid duplicate key presses should be debounced.
    pygame.event.clear()
    # Post two events with the same key immediately.
    test_event1 = pygame.event.Event(pygame.KEYDOWN, {'key': input_handler.key_down})
    test_event2 = pygame.event.Event(pygame.KEYDOWN, {'key': input_handler.key_down})
    pygame.event.post(test_event1)
    pygame.event.post(test_event2)
    result = input_handler.process_events(context="game")
    # The first event should be processed.
    assert result is not None, "First key_down event not processed"
    assert result.get("action") == "move" and result.get("direction") == "DOWN", "Incorrect mapping for key_down event"
    # The second event should be debounced; calling process_events again should return None since event remains debounced.
    result_debounced = input_handler.process_events(context="game")
    assert result_debounced is None, "Debounced event should not be processed"

    # Test 5: After waiting past the debounce threshold, the same key should be processed.
    pygame.time.delay(input_handler.debounce_threshold + 50)
    pygame.event.clear()
    test_event = pygame.event.Event(pygame.KEYDOWN, {'key': input_handler.key_down})
    pygame.event.post(test_event)
    result = input_handler.process_events(context="game")
    assert result is not None, "Key_down event not processed after debounce delay"
    assert result.get("action") == "move" and result.get("direction") == "DOWN", "Incorrect mapping for key_down event after delay"

    # Test 6: Processing a QUIT event.
    pygame.event.clear()
    test_event = pygame.event.Event(pygame.QUIT, {})
    pygame.event.post(test_event)
    result = input_handler.process_events(context="game")
    assert result is not None, "QUIT event not processed"
    assert result.get("action") == "quit", "Expected action 'quit' for QUIT event"

    print("All tests passed successfully.")
    pygame.quit()

if __name__ == "__main__":
    main()