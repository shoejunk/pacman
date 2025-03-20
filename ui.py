import pygame
import sys
from config import SCORE_POS, LIVES_POS, LEVEL_POS, HUD_FONT, MENU_FONT, FONT_COLOR, HIGHLIGHT_COLOR, POPUP_COLOR, POPUP_RECT

if not pygame.font.get_init():
    pygame.font.init()

class Menu:
    def __init__(self, options, position, spacing):
        self.options = options
        self.position = position
        self.spacing = spacing
        self.selected_index = 0
        if not hasattr(MENU_FONT, "render"):
            self.menu_font = pygame.font.SysFont(MENU_FONT, 24)
        else:
            self.menu_font = MENU_FONT

    def draw(self, screen):
        for idx, option in enumerate(self.options):
            color = HIGHLIGHT_COLOR if idx == self.selected_index else FONT_COLOR
            text_surface = self.menu_font.render(option, True, color)
            pos = (self.position[0], self.position[1] + idx * self.spacing)
            screen.blit(text_surface, pos)

    def update_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected(self):
        return self.options[self.selected_index]

def initialize_menu(screen):
    screen_width, screen_height = screen.get_width(), screen.get_height()
    return Menu(["Start", "Options", "High Scores", "Quit"],
                (screen_width // 2 - 100, screen_height // 2 - 50),
                40)

def initialize_gameplay():
    print("Gameplay UI initialized.")

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        if not hasattr(HUD_FONT, "render"):
            self.hud_font = pygame.font.SysFont(HUD_FONT, 24)
        else:
            self.hud_font = HUD_FONT
        self.menus = {}
        screen_width, screen_height = screen.get_width(), screen.get_height()
        self.menus['main'] = initialize_menu(screen)
        self.menus['pause'] = Menu(["Resume", "Restart", "Quit"],
                                   (screen_width // 2 - 100, screen_height // 2 - 30),
                                   40)
        self.menus['game_over'] = Menu(["Restart", "Quit"],
                                       (screen_width // 2 - 100, screen_height // 2 - 20),
                                       40)

    def render_hud(self, score, lives, level):
        score_text = self.hud_font.render("Score: " + str(score), True, FONT_COLOR)
        lives_text = self.hud_font.render("Lives: " + str(lives), True, FONT_COLOR)
        level_text = self.hud_font.render("Level: " + str(level), True, FONT_COLOR)
        self.screen.blit(score_text, SCORE_POS)
        self.screen.blit(lives_text, LIVES_POS)
        self.screen.blit(level_text, LEVEL_POS)

    def draw_menu(self, menu_type):
        if menu_type in self.menus:
            self.menus[menu_type].draw(self.screen)

    def render_menu(self, menu_type):
        self.draw_menu(menu_type)

    def handle_menu_input(self, menu_type, event):
        if menu_type in self.menus:
            self.menus[menu_type].update_selection(event)
            return self.menus[menu_type].get_selected()
        return None

    def draw_popup(self, message):
        popup_rect = POPUP_RECT
        popup_surface = pygame.Surface((popup_rect[2], popup_rect[3]), pygame.SRCALPHA)
        popup_surface.fill(POPUP_COLOR)
        self.screen.blit(popup_surface, (popup_rect[0], popup_rect[1]))
        text_surface = self.hud_font.render(message, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(popup_rect[0] + popup_rect[2] // 2,
                                                  popup_rect[1] + popup_rect[3] // 2))
        self.screen.blit(text_surface, text_rect)

    def show_pause_screen(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        self.draw_menu('pause')

    def hide_pause_screen(self):
        self.screen.fill((0, 0, 0))

    def initialize_level_transition(self):
        print("Level transition UI initialized.")

    def show_game_over(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        self.draw_popup("Game Over!")
        self.draw_menu('game_over')

    def render_game_play(self):
        self.render_hud(0, 0, 0)

    def render_pause_screen(self):
        self.show_pause_screen()

    def cleanup(self):
        pygame.quit()

def main():
    pygame.init()
    if not pygame.font.get_init():
        pygame.font.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("UIManager Test")
    clock = pygame.time.Clock()

    ui_manager = UIManager(screen)

    # Test 1: Render HUD elements and verify rendering
    screen.fill((0, 0, 0))
    ui_manager.render_hud(123, 3, 2)
    pygame.display.flip()
    hud_pixels = pygame.surfarray.array3d(screen)
    assert hud_pixels.sum() != 0, "HUD rendering failed: screen appears blank after rendering HUD."

    # Test 2: Test Menu navigation for main menu
    main_menu = ui_manager.menus['main']
    initial_selection = main_menu.get_selected()
    down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    main_menu.update_selection(down_event)
    new_selection = main_menu.get_selected()
    assert new_selection != initial_selection, "Menu selection did not change after DOWN key."
    up_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    main_menu.update_selection(up_event)
    reverted_selection = main_menu.get_selected()
    assert reverted_selection == initial_selection, "Menu selection did not revert after UP key."

    # Test 3: Test UIManager handle_menu_input for pause menu
    pause_menu_initial = ui_manager.menus['pause'].get_selected()
    simulated_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    selected_after_input = ui_manager.handle_menu_input('pause', simulated_event)
    assert selected_after_input != pause_menu_initial, "Pause menu selection did not change after input event."

    # Test 4: Test drawing popup
    screen.fill((0, 0, 0))
    ui_manager.draw_popup("Level Complete!")
    pygame.display.flip()
    popup_pixels = pygame.surfarray.array3d(screen)
    assert popup_pixels.sum() != 0, "Popup rendering failed: screen appears blank after drawing popup."

    # Test 5: Test show_pause_screen function
    screen.fill((0, 0, 0))
    ui_manager.show_pause_screen()
    pygame.display.flip()
    pause_pixels = pygame.surfarray.array3d(screen)
    assert pause_pixels.sum() != 0, "Pause screen rendering failed: screen appears blank after showing pause screen."

    # Test 6: Visual test - Render HUD and main menu for a short duration
    test_duration = 2000  # milliseconds
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_ticks < test_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ui_manager.cleanup()
                sys.exit()
        screen.fill((0, 0, 0))
        ui_manager.render_hud(456, 5, 3)
        ui_manager.draw_menu('main')
        pygame.display.flip()
        clock.tick(60)

    # Test 7: Test initialize_gameplay function
    try:
        initialize_gameplay()
    except Exception as e:
        assert False, f"initialize_gameplay() raised an exception: {e}"

    # Test 8: Test initialize_level_transition function
    try:
        ui_manager.initialize_level_transition()
    except Exception as e:
        assert False, f"initialize_level_transition() raised an exception: {e}"

    # Test 9: Test show_game_over function
    screen.fill((0, 0, 0))
    ui_manager.show_game_over()
    pygame.display.flip()
    game_over_pixels = pygame.surfarray.array3d(screen)
    assert game_over_pixels.sum() != 0, "Game Over screen rendering failed: screen appears blank after showing game over screen."

    # Test 10: Test hide_pause_screen function
    screen.fill((255, 255, 255))
    ui_manager.hide_pause_screen()
    pygame.display.flip()
    hidden_pixels = pygame.surfarray.array3d(screen)
    assert hidden_pixels.sum() == 0, "hide_pause_screen() failed: screen is not cleared properly."

    # Test 11: Test render_game_play function
    screen.fill((0, 0, 0))
    ui_manager.render_game_play()
    pygame.display.flip()
    gameplay_pixels = pygame.surfarray.array3d(screen)
    assert gameplay_pixels.sum() != 0, "render_game_play() failed: screen appears blank after rendering gameplay UI."

    # Test 12: Test render_pause_screen function
    screen.fill((0, 0, 0))
    ui_manager.render_pause_screen()
    pygame.display.flip()
    pause_render_pixels = pygame.surfarray.array3d(screen)
    assert pause_render_pixels.sum() != 0, "render_pause_screen() failed: screen appears blank after rendering pause screen."

    # Test 13: Test render_menu function for 'pause' menu
    screen.fill((0, 0, 0))
    ui_manager.render_menu('pause')
    pygame.display.flip()
    menu_pixels = pygame.surfarray.array3d(screen)
    assert menu_pixels.sum() != 0, "render_menu() failed: screen appears blank after rendering pause menu."

    ui_manager.cleanup()
    print("All UIManager tests passed.")

if __name__ == "__main__":
    main()