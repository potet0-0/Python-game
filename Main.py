import pygame
import sys
import time


pygame.init()
pygame.mixer.init()
my_sound = pygame.mixer.Sound('assets/mario_coin_sound.mp3')

pygame.time.wait(int(my_sound.get_length() * 1000))
# Screen
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super cube game")
clock = pygame.time.Clock()

# Colors
WHITE = (240, 240, 240)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 100)
GREENER = (41, 204, 0)
DARK = (30, 30, 30)
MOON = (148, 144, 141)
BOX_COLOR = (255, 80, 80)
color = DARK
# Player
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 35, 35)
speed = 9
#
# variables
y_velocity = 0
gravity = 0.6
jump_strength = -13
on_ground = False
maxJumps = 2
jumpCount = 0
level = 0
next_level = False
# Ground
ground_y = HEIGHT - 50

# platforms
platforms = [
    [
        pygame.Rect(293, 709, 120, 15),
        pygame.Rect(510, 495, 150, 15),
        pygame.Rect(737, 245, 120, 15),
        pygame.Rect(1025, 186, 120, 15),
    ],
    [
        pygame.Rect(700, 430, 200, 15),
        pygame.Rect(300, 320, 160, 15),
        pygame.Rect(1050, 180, 120, 15),
    ],
    [
        pygame.Rect(50, 680, 160, 15),
        pygame.Rect(280, 580, 120, 15),
        pygame.Rect(500, 650, 100, 15),
        pygame.Rect(680, 490, 140, 15),
        pygame.Rect(450, 370, 120, 15),
        pygame.Rect(200, 280, 100, 15),
        pygame.Rect(420, 180, 120, 15),
        pygame.Rect(700, 250, 100, 15),
        pygame.Rect(950, 150, 140, 15),
    ],
    [
        pygame.Rect(150,  650,  90, 15),
        pygame.Rect(350,  580,  80, 15),
        pygame.Rect(180,  500,  80, 15),
        pygame.Rect(450,  440,  80, 15),
        pygame.Rect(650,  370,  80, 15),
        pygame.Rect(850,  430,  80, 15),
        pygame.Rect(1050, 350,  80, 15),
        pygame.Rect(1300, 280,  80, 15),
        pygame.Rect(1100, 200,  80, 15),
        pygame.Rect(1500, 500,  80, 15),
        pygame.Rect(1700, 400,  80, 15),
        pygame.Rect(1900, 300,  80, 15),
        pygame.Rect(2100, 220,  80, 15),
        pygame.Rect(1900, 140,  80, 15),
        pygame.Rect(2300, 480,  80, 15),
        pygame.Rect(2500, 380,  80, 15),
        pygame.Rect(2700, 280,  80, 15),
        pygame.Rect(2900, 180,  80, 15),
        pygame.Rect(3100, 100, 120, 15),
    ],
]
platformLevel = platforms[0]
# Jumppad
jumpPad = pygame.Rect(100, -10, 100, 10)

# Target box
box = pygame.Rect(1025, 146, 40, 40)
font = pygame.font.SysFont(None, 32)

worldEdge_left = pygame.Rect(0, 0, 5, HEIGHT)
worldEdge_right = pygame.Rect(WIDTH - 5, 0, 5, HEIGHT)



# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # ground check

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jumpCount < maxJumps:
                    y_velocity = jump_strength
                    jumpCount += 1
            if event.type == pygame.K_ESCAPE:
                sys.exit()
                quit()

    # Left and right movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed

    # "camera" movement (kinda ai coded)
    scroll_speed = speed
    if player.x <= 0:
        player.x = 0
        for plat in platformLevel:
            plat.move_ip(scroll_speed, 0)
        box.move_ip(scroll_speed, 0)
        jumpPad.move_ip(scroll_speed, 0)

    elif player.x >= WIDTH - player.width:
        player.x = WIDTH - player.width
        for plat in platformLevel:
            plat.move_ip(-scroll_speed, 0)
        box.move_ip(-scroll_speed, 0)
        jumpPad.move_ip(-scroll_speed, 0)


    player.x = max(0, min(WIDTH - player.width, player.x))

    prev_bottom = player.bottom

    # Apply gravity
    y_velocity += gravity
    player.y += int(y_velocity)

    # reset on_ground before all collision checks

    on_ground = False
    # Platform collision
    for plat in platformLevel:
        if player.colliderect(plat):
            on_ground = True
            jumpCount = 0
            if prev_bottom <= plat.top + 5:
                player.bottom = plat.top
                y_velocity = 0
                on_ground = True
                jumpCount = 0
            else:
                if player.centerx < plat.centerx:
                    y_velocity = 2
                else:
                    y_velocity = 2


    # Ground check
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity = 0
        on_ground = True

    if on_ground:
        jumpCount = 0


    colliding = player.colliderect(box)
    boosting = player.colliderect(jumpPad)
    if boosting:
        for y_velocity in range(1, -23, -1):
            print(y_velocity)
            pygame.draw.rect(screen, GREENER if colliding else BLUE, player)

    # Draw
    screen.fill(color)
    pygame.draw.rect(screen, WHITE, (0, ground_y, WIDTH, HEIGHT - ground_y))
    for plat in platformLevel:
        pygame.draw.rect(screen, WHITE, plat)
    pygame.draw.rect(screen, GREENER if boosting else GREEN, jumpPad)
    pygame.draw.rect(screen, BOX_COLOR, box)
    pygame.draw.rect(screen, GREEN if colliding else BLUE, player)
    pygame.draw.rect(screen, GREEN, worldEdge_left)
    pygame.draw.rect(screen, GREEN, worldEdge_right)

    if jumpCount >= 2:
        double_jump_label = font.render("No Jump", 0, RED)
    else:
        double_jump_label = font.render("Jump", 0, GREEN)

    if level == 0:
        controls_label = font.render("A and D to move and SPACE to jump", 0, WHITE)
    else:
        controls_label = font.render("", 0, 0)

    label = font.render("Next level" if colliding else "", True, WHITE),
    screen.blit(controls_label, (400, 100))
    screen.blit(double_jump_label, (20, 40))
    screen.blit(label, (20, 20))

    if colliding and not next_level:
        my_sound.play()
        next_level = True
        level += 1
        if level == 1:
            platformLevel = platforms[level]
            jumpPad = pygame.Rect(50, 600, 100, 20)
            box = pygame.Rect(1060, 140, 40, 40)
            player.x = 100
            player.y = 600
            speed = 7
            jump_strength = -12
            next_level = False

        if level == 2:
            platformLevel = platforms[level]
            jumpPad = pygame.Rect(100, -10, 100, 10)
            box = pygame.Rect(990, 110, 40, 40)
            player.x = 50
            player.y = 630
            next_level = False

        if level == 3:
            platformLevel = platforms[2]
            box = pygame.Rect(840, 60, 40, 40)
            player.x = 50
            player.y = 650
            gravity = 0.3
            next_level = False
            color = (MOON)
        if level == 4:
            platformLevel = platforms[3]
            box = pygame.Rect(3120, 60, 40, 40)
            player.x = 50
            player.y = 670
            gravity = 0.6
            color = (DARK)
            next_level = False

    pygame.display.flip()
    clock.tick(60)


    # another ground check
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity = 0
        on_ground = True
