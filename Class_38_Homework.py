import pygame
import random
import math

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("Background_Music.mp3")  # Replace with your music file path
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders!")
icon = pygame.image.load('UFO.png')
pygame.display.set_icon(icon)
background = pygame.image.load('Background.png')

# Sound effect
bullet_sound = pygame.mixer.Sound("Bullet_Sound.mp3")

# Player
player_image = pygame.image.load('Player.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(player_image, (x, y))

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_alive = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)
    enemy_alive.append(True)

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

# Bullet
bullet_image = pygame.image.load('Bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = 'ready'  # 'ready' = can shoot, 'fire' = in motion

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX-bulletX)**2+(enemyY-bulletY)**2)
    return distance<27

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 0, 0))  # Fallback background color
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    bulletY = 480
                    bullet_sound.play()
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    playerX += playerX_change
    playerX = max(0, min(playerX, 736))

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY=480
            bullet_state = 'ready'
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 480
            bullet_state = 'ready'

    player(playerX, playerY)

    pygame.display.update()
    clock.tick(60)