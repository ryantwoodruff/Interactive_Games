import pygame
import sys
import os
import subprocess
from music_manager import MusicManager

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

FONT = pygame.font.SysFont(None, 72)
BG_COLOR = (245, 245, 245)
BOX_COLOR = (100, 100, 200)
BOX_HOVER = (150, 150, 250)
TEXT_COLOR = (255, 255, 255)

labels = ["Fish Game", "Bird Game"]
BUTTON_W = 500
BUTTON_H = 200
COLS = 2
ROWS = 1
H_SPACING = 50
V_SPACING = 50

total_w = COLS * BUTTON_W + (COLS - 1) * H_SPACING
total_h = ROWS * BUTTON_H + (ROWS - 1) * V_SPACING
start_x = (SCREEN_WIDTH - total_w) // 2
start_y = (SCREEN_HEIGHT - total_h) // 2

buttons = []
for i, label in enumerate(labels):
    col = i % COLS
    row = i // COLS
    x = start_x + col * (BUTTON_W + H_SPACING)
    y = start_y + row * (BUTTON_H + V_SPACING)
    rect = pygame.Rect(x, y, BUTTON_W, BUTTON_H)
    buttons.append((rect, label))


def launch(script_name: str):
    """Start a Python script in a separate process and quit the menu."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    try:
        subprocess.Popen([sys.executable, script_path])
    except Exception as exc:
        print(f"Failed to launch {script_name}: {exc}")
    pygame.quit()
    sys.exit()


running = True
clock = pygame.time.Clock()

music = MusicManager('music')

while running:
    screen.fill(BG_COLOR)
    music.update()
    mouse_pos = pygame.mouse.get_pos()

    # Music control buttons (same style as bird_game)
    MENU_FONT = pygame.font.SysFont(None, 32)
    hover_color = (80, 80, 80, 220)
    
    # Quit button (red, bottom left)
    QUIT_BTN_X = 20
    QUIT_BTN_Y = SCREEN_HEIGHT - 80
    MENU_BTN_W = 120
    MENU_BTN_H = 60
    quit_rect = pygame.Rect(QUIT_BTN_X, QUIT_BTN_Y, MENU_BTN_W, MENU_BTN_H)
    quit_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
    quit_surf.fill((100, 40, 40, 180))
    quit_hover_color = (140, 60, 60, 220)
    quit_text = MENU_FONT.render("Quit", True, (255, 255, 255))
    
    MUTE_BTN_X = 1660
    MUTE_BTN_Y = SCREEN_HEIGHT - 80
    SKIP_BTN_X = 1780
    SKIP_BTN_Y = SCREEN_HEIGHT - 80
    PREV_BTN_X = 1540
    PREV_BTN_Y = SCREEN_HEIGHT - 80
    MENU_BTN_W = 120
    MENU_BTN_H = 60
    
    mute_rect = pygame.Rect(MUTE_BTN_X, MUTE_BTN_Y, MENU_BTN_W, MENU_BTN_H)
    mute_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
    mute_surf.fill((40, 40, 40, 180))
    mute_text = MENU_FONT.render("Mute", True, (255, 255, 255))

    skip_rect = pygame.Rect(SKIP_BTN_X, SKIP_BTN_Y, MENU_BTN_W, MENU_BTN_H)
    skip_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
    skip_surf.fill((40, 40, 40, 180))
    skip_text = MENU_FONT.render("Skip", True, (255, 255, 255))

    prev_rect = pygame.Rect(PREV_BTN_X, PREV_BTN_Y, MENU_BTN_W, MENU_BTN_H)
    prev_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
    prev_surf.fill((40, 40, 40, 180))
    prev_text = MENU_FONT.render("Prev", True, (255, 255, 255))

    # Draw music buttons
    # Mute
    shadow_rect = mute_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = mute_rect.collidepoint(mouse_pos)
    if mouse_over:
        hover_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (MUTE_BTN_X, MUTE_BTN_Y))
    else:
        screen.blit(mute_surf, (MUTE_BTN_X, MUTE_BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), mute_rect, 2)
    text_rect = mute_text.get_rect(center=mute_rect.center)
    screen.blit(mute_text, text_rect)

    # Skip
    shadow_rect = skip_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = skip_rect.collidepoint(mouse_pos)
    if mouse_over:
        hover_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (SKIP_BTN_X, SKIP_BTN_Y))
    else:
        screen.blit(skip_surf, (SKIP_BTN_X, SKIP_BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), skip_rect, 2)
    text_rect = skip_text.get_rect(center=skip_rect.center)
    screen.blit(skip_text, text_rect)

    # Prev button
    shadow_rect = prev_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = prev_rect.collidepoint(mouse_pos)
    if mouse_over:
        hover_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (PREV_BTN_X, PREV_BTN_Y))
    else:
        screen.blit(prev_surf, (PREV_BTN_X, PREV_BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), prev_rect, 2)
    text_rect = prev_text.get_rect(center=prev_rect.center)
    screen.blit(prev_text, text_rect)

    # Draw quit button
    shadow_rect = quit_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = quit_rect.collidepoint(mouse_pos)
    if mouse_over:
        hover_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
        hover_surf.fill(quit_hover_color)
        screen.blit(hover_surf, (QUIT_BTN_X, QUIT_BTN_Y))
    else:
        screen.blit(quit_surf, (QUIT_BTN_X, QUIT_BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), quit_rect, 2)
    text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, text_rect)

    for rect, label in buttons:
        color = BOX_COLOR
        if rect.collidepoint(mouse_pos):
            color = BOX_HOVER
        pygame.draw.rect(screen, color, rect)
        text_surf = FONT.render(label, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()
            elif mute_rect.collidepoint(mouse_pos):
                music.mute()
            elif skip_rect.collidepoint(mouse_pos):
                music.skip()
            elif prev_rect.collidepoint(mouse_pos):
                music.play_previous()
            else:
                for rect, label in buttons:
                    if rect.collidepoint(mouse_pos):
                        if label == "Fish Game":
                            launch("fish_game.py")
                        if label == "Bird Game":
                            launch("bird_game.py")
                        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
