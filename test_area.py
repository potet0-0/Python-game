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
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 40, 40)
speed  = 9

# Gravity / jumping
y_velocity    = 0
gravity       = 0.6
jump_strength = -12
on_ground     = False
doubleJump = 1

# Ground
ground_y = HEIGHT - 50

# Target box
box  = pygame.Rect(350, 700, 40, 40)
font = pygame.font.SysFont(None, 32)

platforms = [
    pygame.Rect(200, 600, 200, 15),  # fix: missing commas
    pygame.Rect(500, 500, 180, 15),
    pygame.Rect(100, 380, 150, 15),
]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                if on_ground:
                    y_velocity = jump_strength
                    on_ground  = False
                elif doubleJump > 0:
                    y_velocity = jump_strength
                    doubleJump = 1

    # Left / right movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed

    player.x = max(0, min(WIDTH - player.width, player.x))

    # fix: save prev_bottom each frame, before moving
    prev_bottom = player.bottom

    # Apply gravity
    y_velocity += gravity
    player.y   += int(y_velocity)

    # fix: reset on_ground before all collision checks
    on_ground = False

    # Platform collision
    for plat in platforms:
        if player.colliderect(plat):
            if prev_bottom <= plat.top + 5:  # fix: prev_bottom not prev.bottom
                player.bottom = plat.top
                y_velocity    = 0
                on_ground     = True
            else:
                if player.centerx < plat.centerx:
                    y_velocity = -5
                    
                    on_ground = True
                   # player.right = plat.left
                else:
                    y_velocity = -5

                    on_ground = True

    # Ground check
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity    = 0
        on_ground     = True


    colliding = player.colliderect(box)

    # Draw — everything after screen.fill so nothing gets wiped
    screen.fill(DARK)
    pygame.draw.rect(screen, WHITE, (0, ground_y, WIDTH, HEIGHT - ground_y))
    for plat in platforms:  # fix: draw platforms here, not in collision loop
        pygame.draw.rect(screen, WHITE, plat)
    pygame.draw.rect(screen, BOX_COLOR, box)
    pygame.draw.rect(screen, GREEN if colliding else BLUE, player)

    label = font.render("Touching!" if colliding else "Not Touching Square", True, WHITE)
    screen.blit(label, (20, 20))

    pygame.display.flip()
    clock.tick(60)