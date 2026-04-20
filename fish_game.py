import pygame
import random
import math
import os
import sys
import subprocess
from music_manager import MusicManager

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish Game")

BLUE = (0, 0, 255)
FISH_COLORS = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

base_dir = os.path.dirname(__file__)
try:
    background_path = os.path.join(base_dir, 'background.jpg')
    background_image = pygame.image.load(background_path)
    print(f"Loaded background: {background_path}")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    use_image_bg = True
except Exception as e:
    print(f"Background image failed: {e}")
    use_image_bg = False

vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
max_dist = math.sqrt(center_x**2 + center_y**2)
for x in range(0, SCREEN_WIDTH, 16):
    for y in range(0, SCREEN_HEIGHT, 16):
        dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        alpha = int(255 * (dist / max_dist)**2)
        rect = pygame.Rect(x, y, 16, 16)
        vignette.fill((0, 0, 0, min(alpha, 255)), rect)

FISH_IMAGES = ['fish_1.png', 'fish_2.png']


class Fish:
    def __init__(self, x, y, image_file, fallback_color):
        self.x = x
        self.y = y
        self.direction = 1
        self.speed = random.randint(1, 3)
        self.fallback_color = fallback_color
        self.use_image = True

        base_dir = os.path.dirname(__file__)
        try:
            image_path = os.path.join(base_dir, image_file)
            self.original_image = pygame.image.load(image_path)
            print(f"Loaded fish image: {image_path}")
            original_width, original_height = self.original_image.get_size()
            max_width = 150
            scale_factor = min(max_width / original_width, 1.0)
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            self.original_image = pygame.transform.scale(self.original_image, (new_width, new_height))
            # Conditional colorkey only if image appears to have white background
            if self.original_image.get_at((0,0))[:3] == (255,255,255):
                self.original_image.set_colorkey((255, 255, 255))
            self.flipped_image = pygame.transform.flip(self.original_image, True, False)
            if self.original_image.get_colorkey():
                self.flipped_image.set_colorkey((255, 255, 255))
            self.width = new_width
            self.height = new_height
        except Exception as e:
            print(f"Fish image {image_file} failed: {e}. Using fallback color.")
            self.use_image = False
            self.width = 100
            self.height = 40

        self.update_image()

    def update_image(self):
        if self.use_image:
            if self.direction == 1:
                self.image = self.original_image
            else:
                self.image = self.flipped_image

    def move(self):
        self.x += self.direction * self.speed
        if self.x > SCREEN_WIDTH:
            self.x = -self.width
        elif self.x < -self.width:
            self.x = SCREEN_WIDTH

    def draw(self, screen):
        if self.use_image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.fallback_color, (self.x, self.y, self.width, self.height))

    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    def reverse_direction(self):
        self.direction *= -1
        self.update_image()


fish_list = []
for i in range(11):
    image_file = random.choice(FISH_IMAGES)
    fallback_color = random.choice(FISH_COLORS)
    fish = Fish(0, 0, image_file, fallback_color)
    x = random.randint(0, SCREEN_WIDTH - fish.width)
    y = random.randint(50, SCREEN_HEIGHT - fish.height)
    fish.x = x
    fish.y = y
    fish_list.append(fish)

music = MusicManager('music')

MENU_BTN_W = 120
MENU_BTN_H = 60
MENU_BTN_X = 20
MENU_BTN_Y = SCREEN_HEIGHT - 80
menu_rect = pygame.Rect(MENU_BTN_X, MENU_BTN_Y, MENU_BTN_W, MENU_BTN_H)
menu_surf = pygame.Surface((MENU_BTN_W, MENU_BTN_H), pygame.SRCALPHA)
menu_color = (40, 40, 40, 180) 
menu_surf.fill(menu_color)
MENU_FONT = pygame.font.SysFont(None, 32)
menu_text = MENU_FONT.render("Quit", True, (255, 255, 255))
hover_color = (80, 80, 80, 220)

# Button definitions for bottom right
BTN_W = 120
BTN_H = 60
MUTE_BTN_X = 1660
SKIP_BTN_X = 1780
PREV_BTN_X = 1540
BTN_Y = SCREEN_HEIGHT - 80

mute_rect = pygame.Rect(MUTE_BTN_X, BTN_Y, BTN_W, BTN_H)
skip_rect = pygame.Rect(SKIP_BTN_X, BTN_Y, BTN_W, BTN_H)
prev_rect = pygame.Rect(PREV_BTN_X, BTN_Y, BTN_W, BTN_H)

mute_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
mute_surf.fill((40, 40, 40, 180))
skip_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
skip_surf.fill((40, 40, 40, 180))
prev_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
prev_surf.fill((40, 40, 40, 180))

mute_text = MENU_FONT.render("Mute", True, (255, 255, 255))
skip_text = MENU_FONT.render("Skip", True, (255, 255, 255))
prev_text = MENU_FONT.render("Prev", True, (255, 255, 255))

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
            elif prev_rect.collidepoint(mouse_pos):
                music.play_previous()
            elif mute_rect.collidepoint(mouse_pos):
                music.mute()
            elif skip_rect.collidepoint(mouse_pos):
                music.skip()
            for fish in fish_list:
                if fish.is_clicked(mouse_pos):
                    fish.reverse_direction()

    music.update()

    for fish in fish_list:
        fish.move()
        fish.draw(screen)

    screen.blit(vignette, (0, 0))

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

    # Draw mute button
    shadow_rect = mute_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = mute_rect.collidepoint(pygame.mouse.get_pos())
    if mouse_over:
        hover_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (MUTE_BTN_X, BTN_Y))
    else:
        screen.blit(mute_surf, (MUTE_BTN_X, BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), mute_rect, 2)
    text_rect = mute_text.get_rect(center=mute_rect.center)
    screen.blit(mute_text, text_rect)

    # Draw skip button
    shadow_rect = skip_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = skip_rect.collidepoint(pygame.mouse.get_pos())
    if mouse_over:
        hover_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (SKIP_BTN_X, BTN_Y))
    else:
        screen.blit(skip_surf, (SKIP_BTN_X, BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), skip_rect, 2)
    text_rect = skip_text.get_rect(center=skip_rect.center)
    screen.blit(skip_text, text_rect)

    # Draw previous button
    shadow_rect = prev_rect.move(4, 4)
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
    mouse_over = prev_rect.collidepoint(pygame.mouse.get_pos())
    if mouse_over:
        hover_surf = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        hover_surf.fill(hover_color)
        screen.blit(hover_surf, (PREV_BTN_X, BTN_Y))
    else:
        screen.blit(prev_surf, (PREV_BTN_X, BTN_Y))
    pygame.draw.rect(screen, (255, 255, 255), prev_rect, 2)
    text_rect = prev_text.get_rect(center=prev_rect.center)
    screen.blit(prev_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
