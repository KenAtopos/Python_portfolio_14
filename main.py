import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Invaders")

# Set up the game clock
clock = pygame.time.Clock()

# Load the images
player_image = pygame.image.load("player.png")
enemy_image = pygame.image.load("enemy.png")
bullet_image = pygame.image.load("bullet.png")

# Resize the images
player_size = (50, 50)
player_image = pygame.transform.scale(player_image, player_size)

enemy_size = (40, 40)
enemy_image = pygame.transform.scale(enemy_image, enemy_size)

bullet_size = (10, 20)
bullet_image = pygame.transform.scale(bullet_image, bullet_size)

# Set up the font
font = pygame.font.SysFont(None, 50)


# Set up the player
class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.move_left_flag = False
        self.move_right_flag = False

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.x > window_width - self.rect.width:
            self.rect.x = window_width - self.rect.width

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_left_flag = True
            self.move_right_flag = False
        elif keys[pygame.K_RIGHT]:
            self.move_right_flag = True
            self.move_left_flag = False
        else:
            self.move_left_flag = False
            self.move_right_flag = False

    def update(self):
        if self.move_left_flag:
            self.move_left()
        elif self.move_right_flag:
            self.move_right()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.append(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Set up the enemy
class Enemy:
    def __init__(self, y):
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, window_width - self.rect.width)
        self.rect.y = y
        self.speed = 1

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Set up the bullet
class Bullet:
    def __init__(self, x, y):
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Create the player
player = Player(window_width // 2, window_height - 50)

# Create the enemies
enemies = []
for i in range(10):
    enemy = Enemy(random.randint(0, window_height // 2))
    enemies.append(enemy)

# Create the bullets
bullets = []

# Set up the score and level
score = 0
level = 1
font = pygame.font.SysFont("comicsansms", 30)

# Set up the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Handle player movement
    player.handle_keys()
    player.update()

    # Update game state
    for enemy in enemies:
        enemy.move()
        if enemy.rect.bottom > window_height:
            enemies.remove(enemy)
            score -= 1
        if enemy.rect.colliderect(player.rect):
            pygame.quit()
            sys.exit()

    for bullet in bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                if score >= 10 * level:
                    level += 1
                    for i in range(10):
                        enemy = Enemy(random.randint(0, window_height // 2))
                        enemies.append(enemy)

    # Draw the game
    screen.fill((0, 0, 0))
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    # Draw the score and level
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(text, (10, 40))

    pygame.display.flip()

    # Set the game speed
    clock.tick(30)
