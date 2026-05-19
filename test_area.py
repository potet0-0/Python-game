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

# Gravity / jumping / variables
y_velocity    = 0
gravity       = 0.6
jump_strength = -15
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
                jump_buffer = 4

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

    # Platform collision
    for plat in platforms:
        if player.colliderect(plat):
            if prev_bottom <= plat.top + 5:
                player.bottom = plat.top
                y_velocity    = 0
                on_ground     = True
            else:
                if player.centerx < plat.centerx:
                    y_velocity = 2
                    on_ground = True
                   # player.right = plat.left
                else:
                    y_velocity = 2
                    on_ground = True

    # Ground check
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity    = 0
        on_ground     = True

    # Reset double jump on landing
    if on_ground:
        doubleJump = 1

    # Resolve jump buffer
    if jump_buffer > 0:
        jump_buffer -= 1
        if on_ground:
            y_velocity  = jump_strength
            on_ground   = False
            jump_buffer = 0
        elif doubleJump > 0:
            y_velocity  = jump_strength
            doubleJump  = 0
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
                pygame.Rect(100, 709, 120, 15),
                pygame.Rect(100, 495, 150, 15),
                pygame.Rect(100, 245, 120, 15),
                pygame.Rect(1025, 186, 120, 15),
            ]
            player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 25, 25)
            speed = 7

            player.x = 100
            player.y = 600
            next_level = False

    pygame.display.flip()
    clock.tick(60)