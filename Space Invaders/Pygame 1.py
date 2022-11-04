#Importing pygame library
import pygame
import random
import math
from pygame import mixer

#initializaton of game
pygame.init()

#Making of screen for display
screen  = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('bg.jpg')

#Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

#Caption and icon
pygame.display.set_caption("Abdullah's Game")
icon = pygame.image.load('launch.png') 
pygame.display.set_icon(icon)

# player
playerimage = pygame.image.load('spaceship22.png')
playerX = 370
playerY  = 480
PlayerX_Change = 0

# Enemy
enemyimage = []                   
enemyX = []
enemyY  = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimage.append(pygame.image.load('santelmo.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_Change.append(0.1)
    enemyY_Change.append(40)

# Bullet
bulletimage = pygame.image.load('bullet.png')
bulletX = 0
bulletY  = 480
bulletX_Change = 0
bulletY_Change = 0.7 
bullet_state = "ready"   # "ready" - you can't see it on the screen
                         # "fire" - the bullet is currently moving

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf" , 32)
textX = 10
textY = 10

#Game over text
gameOverText = pygame.font.Font("freesansbold.ttf" , 64)

def show_score(x , y):
    score = font.render("Score: " + str(score_value), True, (0, 234, 1))
    screen.blit(score, (x ,y))
    
def game_OverText():
    OverText = gameOverText.render("Game Over ", True, (0, 234, 1))
    screen.blit(OverText, (200 , 250))

def player(x ,y):
    screen.blit(playerimage, (x ,y))

def enemy(x ,y, i):
    screen.blit(enemyimage[i], (x ,y))

def fire_bullet(x ,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimage, (x + 16, y + 10))

def isCollided(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Making a infinite loop
Running = True
while Running:
    screen.fill((198,198,198))
    #background
    screen.blit(background ,(0 , 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        # checking for keystroke whether it be left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    #get the current x-coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                PlayerX_Change = -0.2
            if event.key == pygame.K_RIGHT:
                PlayerX_Change = 0.2

    #Checking for boundaries for spaceship
    playerX +=  PlayerX_Change

    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    
    #movement for enemy
    for i in range(num_of_enemies):

        # Game Over 
        if enemyY[i] > 440:
            for j  in range(num_of_enemies):
                enemyY[j] = 2000
            game_OverText()
            break

        enemyX[i] +=  enemyX_Change[i]

        if enemyX[i] < 0:
           enemyX_Change[i] = 0.2
           enemyY[i] += enemyY_Change[i]
        elif enemyX[i] > 736: 
            enemyX_Change[i] = -0.2
            enemyY[i] += enemyY_Change[i]

        #collision
        collision = isCollided(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i]  = random.randint(50,150)
        
        enemy(enemyX[i], enemyY[i], i)


    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change
    

    player(playerX, playerY)
    show_score(textX , textY)
    pygame.display.update()
