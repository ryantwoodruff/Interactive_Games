import pygame
import sys
import os
import subprocess

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

FONT = pygame.font.SysFont(None, 36)
BG_COLOR = (50, 50, 50)
BOX_COLOR = (100, 100, 200)
BOX_HOVER = (150, 150, 250)
TEXT_COLOR = (255, 255, 255)

labels = ["Fish Game", "Maze Game", "Game 3", "Game 4"]
BUTTON_W = 300
BUTTON_H = 150
COLS = 2
ROWS = 2
H_SPACING = 100
V_SPACING = 80

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

while running:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()

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
            for rect, label in buttons:
                if rect.collidepoint(event.pos):
                    if label == "Fish Game":
                        launch("fish_game.py")
                    elif label == "Maze Game":
                        launch("maze_game.py")
                    else:
                        print(f"{label} is not implemented yet.")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
