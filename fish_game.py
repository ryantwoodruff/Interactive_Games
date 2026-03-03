import pygame
import random
import math
import os
import sys
import subprocess

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish Game")

BLUE = (0, 0, 255)
FISH_COLORS = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

try:
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    use_image_bg = True
except Exception:
    print("Background image not found. Using solid blue background.")
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
        self.speed = random.randint(1, 4)
        self.fallback_color = fallback_color
        self.use_image = True

        try:
            self.original_image = pygame.image.load(image_file)
            original_width, original_height = self.original_image.get_size()
            max_width = 100
            scale_factor = min(max_width / original_width, 1)
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            self.original_image = pygame.transform.scale(self.original_image, (new_width, new_height))
            self.original_image.set_colorkey((255, 255, 255))
            self.flipped_image = pygame.transform.flip(self.original_image, True, False)
            self.flipped_image.set_colorkey((255, 255, 255))
            self.width = new_width
            self.height = new_height
        except Exception:
            print(f"Image {image_file} not found. Using fallback color.")
            self.use_image = False
            self.width = 50
            self.height = 20

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
for i in range(25):
    image_file = random.choice(FISH_IMAGES)
    fallback_color = random.choice(FISH_COLORS)
    fish = Fish(0, 0, image_file, fallback_color)
    x = random.randint(0, SCREEN_WIDTH - fish.width)
    y = random.randint(50, SCREEN_HEIGHT - fish.height)
    fish.x = x
    fish.y = y
    fish_list.append(fish)


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
            for fish in fish_list:
                if fish.is_clicked(mouse_pos):
                    fish.reverse_direction()

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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
