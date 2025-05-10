import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Warship Defender")
icon = pygame.image.load('spaceship.png')  # You'll need a spaceship.png file
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.jpg')  # You'll need a space background
background = pygame.transform.scale(background, (screen_width, screen_height))

# Background sound
mixer.music.load('background.mp3')  # You'll need a sound file
mixer.music.play(-1)  # -1 makes it loop

# Player
player_img = pygame.image.load('player.png')  # Player ship image
player_width = 64
player_height = 64
player_img = pygame.transform.scale(player_img, (player_width, player_height))
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 20
player_speed = 5
player_x_change = 0

# Bullet
bullet_img = pygame.image.load('bullet.jpg')  # Bullet image
bullet_width = 32
bullet_height = 32
bullet_img = pygame.transform.scale(bullet_img, (bullet_width, bullet_height))
bullet_x = 0
bullet_y = player_y
bullet_speed = 10
bullet_state = "ready"  # "ready" - not visible, "fire" - moving

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6
enemy_speed = 2

for i in range(num_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))  # Enemy image
    enemy_width = 64
    enemy_height = 64
    enemy_img[i] = pygame.transform.scale(enemy_img[i], (enemy_width, enemy_height))
    enemy_x.append(random.randint(0, screen_width - enemy_width))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(enemy_speed)
    enemy_y_change.append(40)  # How much they move down when hitting edge

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# Explosion
explosion_img = pygame.image.load('explosion.jpg')  # Explosion image
explosion_width = 64
explosion_height = 64
explosion_img = pygame.transform.scale(explosion_img, (explosion_width, explosion_height))
explosion_timer = 0
explosion_duration = 30  # frames
show_explosion = False
explosion_x = 0
explosion_y = 0

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + player_width//2 - bullet_width//2, y - bullet_height))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    return distance < 27  # Collision threshold

def show_explosion_effect(x, y):
    screen.blit(explosion_img, (x, y))

def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over, (screen_width//2 - 200, screen_height//2 - 50))

# Game Loop
running = True
while running:
    # RGB background
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound('laser.mp3')  # Laser sound
                bullet_sound.play()
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    
    # Player movement
    player_x += player_x_change
    
    # Boundary checking
    if player_x <= 0:
        player_x = 0
    elif player_x >= screen_width - player_width:
        player_x = screen_width - player_width
    
    # Enemy movement
    for i in range(num_enemies):
        # Game Over condition
        if enemy_y[i] > player_y - 50:
            for j in range(num_enemies):
                enemy_y[j] = 2000  # Move all enemies off screen
            game_over_text()
            break
        
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = enemy_speed
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= screen_width - enemy_width:
            enemy_x_change[i] = -enemy_speed
            enemy_y[i] += enemy_y_change[i]
        
        # Collision detection
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.mp3')  # Explosion sound
            explosion_sound.play()
            explosion_x = enemy_x[i]
            explosion_y = enemy_y[i]
            show_explosion = True
            explosion_timer = explosion_duration
            bullet_y = player_y
            bullet_state = "ready"
            score_value += 10
            enemy_x[i] = random.randint(0, screen_width - enemy_width)
            enemy_y[i] = random.randint(50, 200)
        
        enemy(enemy_x[i], enemy_y[i], i)
    
    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
    
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"
    
    # Show explosion effect
    if show_explosion:
        show_explosion_effect(explosion_x, explosion_y)
        explosion_timer -= 1
        if explosion_timer <= 0:
            show_explosion = False
    
    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()

pygame.quit()