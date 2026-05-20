import pygame
import sys
import time
pygame.init()

# Screen
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super cube game")
clock = pygame.time.Clock()

# Colors
WHITE     = (240, 240, 240)
BLUE      = (0, 150, 255)
GREEN     = (0, 255, 100)
DARK      = (30, 30, 30)
BOX_COLOR = (255, 80, 80)

# Player
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 35, 35)
speed  = 9

# variables
y_velocity    = 0
gravity       = 0.6
jump_strength = -13
on_ground     = False
doubleJump    = 1
jump_buffer   = 0
level         = 1
next_level    = False

# Ground
ground_y = HEIGHT - 50

# Target box
box  = pygame.Rect(1025, 146, 40, 40)
font = pygame.font.SysFont(None, 32)

platforms = [
    pygame.Rect(293,  709, 120, 15),
    pygame.Rect(510,  495, 150, 15),
    pygame.Rect(737,  245, 120, 15),
    pygame.Rect(1025, 186, 120, 15),
]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if on_ground:
                    jump_buffer = 4   # normal jump buffer

    # Left / right movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed

    player.x = max(0, min(WIDTH - player.width, player.x))

    prev_bottom = player.bottom

    # Apply gravity
    y_velocity += gravity
    player.y   += int(y_velocity)

    # reset on_ground before all collision checks
    on_ground = False

    # Platform collision (unchanged)
    for plat in platforms:
        if player.colliderect(plat):
            if prev_bottom <= plat.top + 5:
                player.bottom = plat.top
                y_velocity = 0
                on_ground = True
            else:
                if player.centerx < plat.centerx:
                    y_velocity = 2
                else:
                    y_velocity = 2

    # Ground check
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity    = 0
        on_ground     = True

    # Reset double jump on landing
    if on_ground:
        doubleJump = 1

    # ⭐ FIXED DOUBLE JUMP ⭐
    if keys[pygame.K_SPACE] and not on_ground and doubleJump > 0:
        y_velocity = jump_strength
        doubleJump = 0

    # Resolve jump buffer (ground only)
    if jump_buffer > 0:
        jump_buffer -= 1
        if on_ground:
            y_velocity  = jump_strength
            on_ground   = False
            jump_buffer = 0

    colliding = player.colliderect(box)

    # Draw
    screen.fill(DARK)
    pygame.draw.rect(screen, WHITE, (0, ground_y, WIDTH, HEIGHT - ground_y))
    for plat in platforms:
        pygame.draw.rect(screen, WHITE, plat)
    pygame.draw.rect(screen, BOX_COLOR, box)
    pygame.draw.rect(screen, GREEN if colliding else BLUE, player)

    label = font.render("Next level" if colliding else "Not Touching Square", True, WHITE)
    screen.blit(label, (20, 20))

    if colliding and not next_level:
        next_level = True
        level += 1
        if level == 2:
            platforms = [
                pygame.Rect(100, 650, 200, 15),
                pygame.Rect(400, 550, 180, 15),
                pygame.Rect(700, 430, 200, 15),
                pygame.Rect(300, 320, 160, 15),
                pygame.Rect(600, 210, 180, 15),
                pygame.Rect(1050, 180, 120, 15),
            ]
            box = pygame.Rect(1060, 140, 40, 40)
            player.x = 100
            player.y = 600
            speed = 7
            jump_strength = -12
            next_level = False

        if level == 3:
            platforms = [
                pygame.Rect(50,  680, 160, 15),
                pygame.Rect(280, 580, 120, 15),
                pygame.Rect(500, 650, 100, 15),
                pygame.Rect(680, 490, 140, 15),
                pygame.Rect(450, 370, 120, 15),
                pygame.Rect(200, 280, 100, 15),
                pygame.Rect(420, 180, 120, 15),
                pygame.Rect(700, 250, 100, 15),
                pygame.Rect(950, 150, 140, 15),
            ]
            box = pygame.Rect(990, 110, 40, 40)
            player.x = 50
            player.y = 630
            next_level = False

        if level == 4:
            platforms = [
                pygame.Rect(50,   700, 130, 15),
                pygame.Rect(350,  600, 100, 15),
                pygame.Rect(150,  490, 100, 15),
                pygame.Rect(500,  400, 100, 15),
                pygame.Rect(250,  300, 100, 15),
                pygame.Rect(600,  220, 100, 15),
                pygame.Rect(850,  310, 100, 15),
                pygame.Rect(1000, 200, 100, 15),
                pygame.Rect(800,  100, 130, 15),
            ]
            box = pygame.Rect(840, 60, 40, 40)
            player.x = 50
            player.y = 650
            next_level = False

        if level == 5:
            platforms = [
                pygame.Rect(50,  720, 100, 15),
                pygame.Rect(280, 640,  80, 15),
                pygame.Rect(520, 530,  80, 15),
                pygame.Rect(750, 620,  80, 15),
                pygame.Rect(950, 480,  80, 15),
                pygame.Rect(700, 350,  80, 15),
                pygame.Rect(400, 250,  80, 15),
                pygame.Rect(650, 140,  80, 15),
                pygame.Rect(950, 100, 100, 15),
            ]
            box = pygame.Rect(975, 60, 40, 40)
            player.x = 50
            player.y = 670
            next_level = False

    pygame.display.flip()
    clock.tick(60)