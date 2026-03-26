import pygame
import os
import sys
import subprocess

pygame.init()
pygame.mixer.init()  # Initialize mixer for audio

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bird Chirping Game")

BLUE = (135, 206, 235)  # Sky blue background

try:
    background_image = pygame.image.load('tree_background.jpg')  # Replace with your image file
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    use_image_bg = True
except Exception:
    print("Background image not found. Using solid blue background.")
    use_image_bg = False

# Vignette effect (optional, same as fish game)
import math
vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
max_dist = math.sqrt(center_x**2 + center_y**2)
for x in range(0, SCREEN_WIDTH, 16):
    for y in range(0, SCREEN_HEIGHT, 16):
        dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        alpha = int(255 * (dist / max_dist)**2)
        rect = pygame.Rect(x, y, 16, 16)
        vignette.fill((0, 0, 0, min(alpha, 255)), rect)

class Bird:
    def __init__(self, x, y, width, height, sound_file):
        self.rect = pygame.Rect(x, y, width, height)
        self.sound_file = sound_file
        try:
            self.sound = pygame.mixer.Sound(sound_file)
        except Exception as e:
            print(f"Could not load sound {sound_file}: {e}")
            self.sound = None

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def chirp(self):
        if self.sound:
            self.sound.play()

# Define birds with their positions and sound files
# Replace these with actual coordinates and sound files
birds = [
    Bird(310, 210, 100, 100, 'bird1.wav'),  # Black bird on far left
    Bird(710, 160, 110, 110, 'bird2.wav'),  # Blue bird
    Bird(700, 490, 130, 130, 'bird3.wav'),  # Orange bird, middle
    Bird(985, 310, 140, 140, 'bird4.wav'),  # Red bird, middle
    Bird(1280, 420, 80, 80, 'bird5.wav'),   # Small tan bird
    Bird(290, 900, 110, 110, 'bird1.wav'),  # morning bird on left
    Bird(520, 935, 110, 110, 'bird1.wav'),  # mourning bird right of previous
    Bird(1210, 810, 100, 100, 'bird4.wav'),  # Red bird, middle
    Bird(1550, 710, 100, 100, 'bird4.wav'),  # blue bird, right
    # Add more birds as needed
]

# Menu button (same as fish game)
MENU_BTN_W = 150
MENU_BTN_H = 54
MENU_BTN_X = 20
MENU_BTN_Y = 20
menu_rect = pygame.Rect(MENU_BTN_X, MENU_BTN_Y, MENU_BTN_W, MENU_BTN_H)
menu_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
menu_color = (40, 40, 40, 180)
menu_surf.fill(menu_color)
MENU_FONT = pygame.font.SysFont(None, 28)
menu_text = MENU_FONT.render("Quit", True, (255, 255, 255))
hover_color = (80, 80, 80, 220)

def launch_main_menu():
    script_path = os.path.join(os.path.dirname(__file__), 'main_menu.py')
    try:
        subprocess.Popen([sys.executable, script_path])
    except Exception as exc:
        print(f"Failed to launch main_menu.py: {exc}")

running = True
clock = pygame.time.Clock()

while running:
    if use_image_bg:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if menu_rect.collidepoint(mouse_pos):
                launch_main_menu()
                running = False
                break
            for bird in birds:
                if bird.is_clicked(mouse_pos):
                    bird.chirp()

    # No need to move or draw birds since they are part of the background image

    screen.blit(vignette, (0, 0))

    # Draw menu button
    shadow_rect = menu_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = menu_rect.collidepoint(pygame.mouse.get_pos())
    if mouse_over:
        hover_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (MENU_BTN_X, MENU_BTN_Y))
    else:
        screen.blit(menu_surf, (MENU_BTN_X, MENU_BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 2)
    text_rect = menu_text.get_rect(center=menu_rect.center)
    screen.blit(menu_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
