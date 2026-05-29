import pygame
import sys

# play sound when collision with flag
pygame.init()
pygame.mixer.init()
my_sound = pygame.mixer.Sound('assets/mario_coin_sound.mp3')

pygame.time.wait(int(my_sound.get_length() * 1000))
# Screen variables
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super cube game")
clock = pygame.time.Clock()

# Colors and backgrounds
WHITE = (240, 240, 240)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 100)
GREENER = (41, 204, 0)
DARK = (30, 30, 30)
MOON = (148, 144, 141)
BOX_COLOR = (255, 80, 80)
backgrounds = {
    'moon': pygame.transform.scale(pygame.image.load('assets/moon_background.png').convert(), (WIDTH, HEIGHT)),
    'dark': pygame.transform.scale(pygame.image.load('assets/background.jpg').convert(), (WIDTH, HEIGHT)),
    'green_flag': pygame.transform.scale(pygame.image.load('assets/green_flag.png').convert(), (WIDTH, HEIGHT)),
    'red_flag': pygame.transform.scale(pygame.image.load('assets/red_flag.png').convert(), (WIDTH, HEIGHT)),
}
# set 'dark' as the background on start level
background = backgrounds['dark']

# Sprites
cloud_img = pygame.image.load('assets/cloud.png').convert()
cloud_img = pygame.transform.scale(cloud_img, (120, 15))
flag_red = pygame.transform.scale(pygame.image.load('assets/red_flag.png').convert_alpha(), (25, 100))
flag_green = pygame.transform.scale(pygame.image.load('assets/green_flag.png').convert_alpha(), (25, 100))
frog_player = pygame.transform.scale(pygame.image.load('assets/frog.png').convert_alpha(), (35, 35))

# Player
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 35, 35)
speed = 9

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

# platforms listed for each level
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
        pygame.Rect(150, 650, 90, 15),
        pygame.Rect(350, 580, 80, 15),
        pygame.Rect(180, 500, 80, 15),
        pygame.Rect(450, 440, 80, 15),
        pygame.Rect(650, 370, 80, 15),
        pygame.Rect(850, 430, 80, 15),
        pygame.Rect(1050, 350, 80, 15),
        pygame.Rect(1300, 280, 80, 15),
        pygame.Rect(1100, 200, 80, 15),
        pygame.Rect(1500, 500, 80, 15),
        pygame.Rect(1700, 400, 80, 15),
        pygame.Rect(1900, 300, 80, 15),
        pygame.Rect(2100, 220, 80, 15),
        pygame.Rect(1900, 140, 80, 15),
        pygame.Rect(2300, 480, 80, 15),
        pygame.Rect(2500, 380, 80, 15),
        pygame.Rect(2700, 280, 80, 15),
        pygame.Rect(2900, 180, 80, 15),
        pygame.Rect(3100, 100, 120, 15),
    ],
    [
        pygame.Rect(150, 650, 90, 15)
    ]
]
platformLevel = platforms[0]

# JumpPad
jumpPad = pygame.Rect(100, -10, 100, 10)

# Target box
box = pygame.Rect(1025, 100, 40, 80)
font = pygame.font.SysFont(None, 32)

# world edge for camera movement
worldEdge_left = pygame.Rect(0, 0, 5, HEIGHT)
worldEdge_right = pygame.Rect(WIDTH - 5, 0, 5, HEIGHT)

# menu logic loop thingy
menu = "menu"


def draw_menu():
    screen.blit(backgrounds['dark'], (0, 0))
    title = font.render("Super Cube Game", True, WHITE)
    start = font.render("Press ENTER to start", True, GREEN)
    screen.blit(title, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(start, (WIDTH // 2 - 120, HEIGHT // 2 + 20))
    pygame.display.flip()


while menu == "menu":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                menu = "playing"
    draw_menu()
    clock.tick(60)


def draw_pause():
    screen.blit(backgrounds['dark'], (0, 0))
    pause_title = font.render("pause menu", True, WHITE)
    screen.blit(pause_title, (WIDTH // 2 - 120, HEIGHT // 2 + 20))
    pygame.display.flip()
    exit_btn = {
        pygame.rect
    }
    pygame.draw.rect(screen, GREEN, exit_btn)


# Game loop
while True:
    if menu == "pause": #check if pause is true
        draw_pause() #clears screen and uses the draw pause def
        for event in pygame.event.get(): #check for keys and resize and close button use
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = "playing"
        clock.tick(0)
        continue #breaks out of this loop and continues the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # pause screen logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = "pause"

        # double jump logic
        # uses a counter that allows you to jump if the jump counter is less than 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jumpCount < maxJumps:
                    y_velocity = jump_strength
                    jumpCount += 1

    # Left and right movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: player.x -= speed
    if keys[pygame.K_d]: player.x += speed
    # "camera" movement (kinda AI coded)
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

    # reset on_ground before all collision checks to make double jump work better (found on Google (no AI) but not completely my code
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

    # Ground check to reset jump counter
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity = 0
        on_ground = True

    if on_ground:
        jumpCount = 0
    # logic to make the JumpPad work
    colliding = player.colliderect(box)
    boosting = player.colliderect(jumpPad)
    if boosting:
        for y_velocity in range(1, -23, -1):  # for loop to make the boost smoother
            print(y_velocity)
            pygame.draw.rect(screen, GREENER if colliding else BLUE, player)

    # Draw
    flag_img = flag_green if next_level else flag_red

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, WHITE, (0, ground_y, WIDTH, HEIGHT - ground_y))
    for plat in platformLevel:
        screen.blit(cloud_img, (plat.x, plat.y))
    pygame.draw.rect(screen, GREENER if boosting else GREEN, jumpPad)
    screen.blit(flag_img, (box.x, box.y))
    screen.blit(frog_player, (player.x, player.y))
    pygame.draw.rect(screen, GREEN, worldEdge_left)
    pygame.draw.rect(screen, GREEN, worldEdge_right)


    # show and hide text logic
    if jumpCount >= 2:
        double_jump_label = font.render("No Jump", 0, RED)
    else:
        double_jump_label = font.render("Jump", 0, GREEN)

    if level == 0:
        controls_label = font.render("A and D to move and SPACE to jump", 0, WHITE)
    else:
        controls_label = font.render("", 0, 0)

    if level == 5:
        victory_text = font.render("Well done, you beat my game", True, WHITE)
        end_text = font.render("Touch the flag to quit/finish", True, WHITE)

    else:
        victory_text = font.render("", True, WHITE)
        end_text = font.render("", True, WHITE)

    # print text contents
    label = font.render("Next level" if colliding else "", True, WHITE),
    screen.blit(controls_label, (400, 100))
    screen.blit(double_jump_label, (20, 40))
    screen.blit(victory_text, (400, 200))
    screen.blit(end_text, (400, 400))

    # next level logic
    if colliding and not next_level:
        my_sound.play()
        next_level = True
        level += 1
        # changes to first level
        if level == 1:
            platformLevel = platforms[level]  # collects the next platform list from the list
            jumpPad = pygame.Rect(50, 600, 100, 20)
            box = pygame.Rect(1060, 100, 40, 40)  # where the next level flag is placed
            player.x = 100  # where the player spawns in
            player.y = 600
            speed = 7  # change speed variable
            jump_strength = -12  # and jump strength
            next_level = False  # makes so the level change only triggers once

        # basically same as level 1 and 2
        if level == 2:
            platformLevel = platforms[level]
            jumpPad = pygame.Rect(100, -10, 100, 10)
            box = pygame.Rect(990, 70, 40, 40)
            player.x = 50
            player.y = 630
            next_level = False

        # moon level with changed background and lower gravity
        if level == 3:
            platformLevel = platforms[2]
            box = pygame.Rect(840, 20, 40, 40)
            player.x = 50
            player.y = 650
            gravity = 0.3  # set gravity lower
            next_level = False
            background = backgrounds['moon']

        if level == 4:
            platformLevel = platforms[3]
            box = pygame.Rect(3120, 60, 40, 40)
            player.x = 50
            player.y = 670
            gravity = 0.6  # change back the gravity
            background = backgrounds['dark']  # also change back the background
            next_level = False

        # victory level
        if level == 5:
            platformLevel = platforms[4]
            box = pygame.Rect(840, 500, 40, 200)
            player.x = 50
            player.y = 200
            gravity = 0.6
            next_level = False
            flag_img = pygame.transform.scale(flag_img, (100, 400))

        if level == 6:
            print("Well done beating my game please give star on github repo")
            pygame.quit()  # quit game
            sys.exit()  # also quit game

    pygame.display.flip()
    clock.tick(60)

    # another ground check
    # I use ths for consistency
    if player.bottom >= ground_y:
        player.bottom = ground_y
        y_velocity = 0
        on_ground = True
