import pygame
from pygame import mixer
import random
import math

# initialize the pygame
pygame.init()

# Screen of the game
screen = pygame.display.set_mode((800, 600))

# Score
score_value = 0
font = pygame.font.Font(None,32) # dafont is a website that you can download a font, remember that the extensions is essentialy .ttf
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Background
background = pygame.image.load(r"images\background.png")

# Title and Icon
pygame.display.set_caption("FelippoDev Game")
icon = pygame.image.load(r"images\alien.png")
pygame.display.set_icon(icon)

# Effects sounds
""" For putting a background song i will let an example here:
mixer.load.music("NameOfTheFile")
mixer music.play(-1) - that minus is basically for putting the song in loop."""

# Gamer Over
textY_EndGame = 255
textX_EndGame = 155
font_endGame = pygame.font.Font(None, 100)


def game_over():
    endGame_text = font_endGame.render(" GAME OVER ", True, (0, 0, 0))
    screen.blit(endGame_text, (textX_EndGame, textY_EndGame))


# Player
playerImg = pygame.image.load(r"images\spaceship.png")
playerImg = pygame.transform.scale(playerImg, (45, 45))
playerX = 380
playerY = 500
playerMov = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXMov = []
enemyYMov = []

num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load(r"images\enemy.png"))
    enemyImg.append(pygame.transform.scale(enemyImg[i], (35, 35)))
    enemyX.append(random.randint(0, 580))
    enemyY.append(random.randint(5, 140))
    enemyXMov.append(0.3)
    enemyYMov.append(20)


def enemy(x, y):
    screen.blit(enemyImg[1], (x, y))


# Bullet
bulletImg = pygame.image.load(r"images\bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (15, 15))
bulletXMov = playerX
bulletYMov = playerY
bullet_shooting = 0.7
# ready = You can't see the bullet on the screen
# fire = The bullet is currently moving
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 15, y + 8))


def collision(enemyX, enemyY, bulletXMov, bulletYMov):
    distance = math.sqrt(math.pow(enemyX - bulletXMov, 2) + math.pow(enemyY - bulletYMov, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB - red green blue
    screen.fill((128, 0, 255))
    # Background on the screen
    screen.blit(background, (0, 0))
    # Score on game
    show_score(textX, textY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerMov -= 0.4

            if event.key == pygame.K_d:
                playerMov += 0.4

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound(r'song_effects\laser_beam.mp3')
                    bullet_sound.play()
                    bulletXMov = playerX
                    fire_bullet(bulletXMov, bulletYMov)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerMov = 0

    # Bullet movement
    if bulletYMov < 0:
        bulletYMov = playerY
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletXMov, bulletYMov)
        bulletYMov -= bullet_shooting

    playerX += playerMov
    # Border of the screen
    if playerX < 1:
        playerX = 1
    if playerX > 763:
        playerX = 763

    # Enemy movement
    for i in range(num_enemies):
        # Game over
        if enemyY[i] > 350:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()

        enemyX[i] += enemyXMov[i]

        if enemyX[i] < 1:
            enemyXMov[i] += 0.3
            enemyY[i] += enemyYMov[i]
        elif enemyX[i] > 763:
            enemyXMov[i] -= 0.3
            enemyY[i] += enemyYMov[i]

            # Collision
        collision_effect = collision(enemyX[i], enemyY[i], bulletXMov, bulletYMov)
        if collision_effect:
            bulletYMov = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 580)
            enemyY[i] = random.randint(5, 140)
            collision_sound = mixer.Sound(r'song_effects\explosion.mp3')
            collision_sound.play()
        enemy(enemyX[i], enemyY[i])

    player(playerX, playerY)
    pygame.display.update()
