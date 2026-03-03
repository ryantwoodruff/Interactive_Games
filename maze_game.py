import pygame
import sys
import random
import os
import subprocess

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# utility to launch the main menu program
# (runs in separate process so this window can close)
def launch_main_menu():
    script_path = os.path.join(os.path.dirname(__file__), 'main_menu.py')
    try:
        subprocess.Popen([sys.executable, script_path])
    except Exception as exc:
        print(f"Failed to launch main_menu.py: {exc}")

BG_COLOR = (30, 30, 30)
WALL_COLOR = (200, 200, 200)
BALL_COLOR = (255, 50, 50)  # red
BALL_RADIUS = 15  # medium sized ball

# quit button parameters
BTN_W = 150
BTN_H = 54
BTN_X = 20
BTN_Y = 20
btn_rect = pygame.Rect(BTN_X, BTN_Y, BTN_W, BTN_H)
btn_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
btn_color = (40, 40, 40, 180)
btn_surf.fill(btn_color)
hover_color = (80, 80, 80, 220)
BTN_FONT = pygame.font.SysFont(None, 28)
btn_text = BTN_FONT.render("Quit", True, (255, 255, 255))

# level definitions: each base level holds wall rects and a start pos
base_width = 800
base_height = 600
scale_x = SCREEN_WIDTH / base_width
scale_y = SCREEN_HEIGHT / base_height

level1 = {
    'walls': [
        pygame.Rect(0, 0, base_width, 20),
        pygame.Rect(0, 0, 20, base_height),
        pygame.Rect(0, base_height - 20, base_width, 20),
        pygame.Rect(base_width - 20, 0, 20, base_height),
        pygame.Rect(100, 100, 600, 20),
        pygame.Rect(100, 100, 20, 400),
        pygame.Rect(100, 480, 600, 20),
        pygame.Rect(680, 100, 20, 400),
        pygame.Rect(200, 200, 400, 20),
        pygame.Rect(200, 200, 20, 200),
        pygame.Rect(200, 380, 400, 20),
        pygame.Rect(580, 200, 20, 200),
    ],
    'start': (50, 50)
}

level2 = {
    'walls': [
        pygame.Rect(0, 0, base_width, 20),
        pygame.Rect(0, 0, 20, base_height),
        pygame.Rect(0, base_height - 20, base_width, 20),
        pygame.Rect(base_width - 20, 0, 20, base_height),
        pygame.Rect(150, 150, 500, 20),
        pygame.Rect(150, 150, 20, 300),
        pygame.Rect(150, 430, 500, 20),
        pygame.Rect(630, 150, 20, 300),
        pygame.Rect(300, 300, 200, 20),
    ],
    'start': (100, 100)
}

# new level based on provided icon, roughly a spiral
level3 = {
    'walls': [
        pygame.Rect(0, 0, base_width, 20),
        pygame.Rect(0, 0, 20, base_height),
        pygame.Rect(0, base_height - 20, base_width, 20),
        pygame.Rect(base_width - 20, 0, 20, base_height),
        # inner spiral walls
        pygame.Rect(100, 100, 600, 20),
        pygame.Rect(100, 100, 20, 400),
        pygame.Rect(100, 480, 600, 20),
        pygame.Rect(680, 100, 20, 400),
        pygame.Rect(200, 200, 400, 20),
        pygame.Rect(200, 200, 20, 200),
        pygame.Rect(200, 380, 200, 20),
        pygame.Rect(400, 380, 20, 100),
        pygame.Rect(400, 330, 200, 20),
        pygame.Rect(580, 330, 20, 50),
    ],
    'start': (50, 50)
}

base_levels = [level1, level2, level3]

walls = []
ball_pos = pygame.Vector2(0, 0)
current_level = None

def load_level(level):
    global walls, ball_pos, goal_rect, current_level
    current_level = level
    # scale walls
    walls = []
    for bw in level['walls']:
        walls.append(pygame.Rect(int(bw.x * scale_x), int(bw.y * scale_y),
                                 int(bw.width * scale_x), int(bw.height * scale_y)))
    # starting position
    sx, sy = level['start']
    ball_pos = pygame.Vector2(sx * scale_x, sy * scale_y)
    # goal square in center
    gw = 40
    gh = 40
    goal_rect = pygame.Rect((SCREEN_WIDTH - gw) // 2, (SCREEN_HEIGHT - gh) // 2, gw, gh)

# pick random level initially
load_level(random.choice(base_levels))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(event.pos):
                launch_main_menu()
                running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    desired = pygame.Vector2(mouse_x, mouse_y)

    # constrain ball center to avoid wall collision
    new_pos = desired
    ball_rect = pygame.Rect(new_pos.x - BALL_RADIUS, new_pos.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    collision = False
    for wall in walls:
        if ball_rect.colliderect(wall):
            collision = True
            break
    if not collision:
        ball_pos = new_pos

    # check goal collision
    if ball_rect.colliderect(goal_rect):
        # pick a random next level not equal to current
        next_level = random.choice(base_levels)
        while next_level is current_level and len(base_levels) > 1:
            next_level = random.choice(base_levels)
        load_level(next_level)
        continue

    screen.fill(BG_COLOR)
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)
    # draw goal square
    pygame.draw.rect(screen, (255, 255, 0), goal_rect)
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos.x), int(ball_pos.y)), BALL_RADIUS)

    # draw quit button with hover effect
    mouse_over = btn_rect.collidepoint(pygame.mouse.get_pos())
    if mouse_over:
        hover_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (BTN_X, BTN_Y))
    else:
        screen.blit(btn_surf, (BTN_X, BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2)
    text_rect = btn_text.get_rect(center=btn_rect.center)
    screen.blit(btn_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
