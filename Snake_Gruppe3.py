import pygame
import random
import sys

# Initialisiere Pygame
pygame.init()

# Bildschirmgröße festlegen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Einfaches Snake-Spiel')

# Farben definieren
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)
COLORS = [GREEN, RED, GRAY, WHITE, BLACK]

# Snake-Eigenschaften
snake_size = 20
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
snake_color = GREEN

# Apfel-Eigenschaften
apple_size = 20
# Initiale Platzierung des Apfels
apple_pos = [random.randint(0, (screen_width // apple_size) - 1) * apple_size, 
             random.randint(0, (screen_height // apple_size) - 1) * apple_size]

# Spielgeschwindigkeit
speed = 15
clock = pygame.time.Clock()

# Punktestand
score = 0

# Rauchpartikel
smoke_particles = []

# Schriftart für Text
font = pygame.font.SysFont('times new roman', 20)

def move_snake():
    global direction, change_to, snake_pos, snake_body

    direction = change_to

    if direction == 'UP':
        snake_pos[1] -= snake_size
    if direction == 'DOWN':
        snake_pos[1] += snake_size
    if direction == 'LEFT':
        snake_pos[0] -= snake_size
    if direction == 'RIGHT':
        snake_pos[0] += snake_size

    # Die Schlange bewegt sich
    snake_body.insert(0, list(snake_pos))
    snake_body.pop()

def eat_apple():
    global apple_pos, score, snake_body

    if abs(snake_pos[0] - apple_pos[0]) < snake_size and abs(snake_pos[1] - apple_pos[1]) < snake_size:
        # Neue Platzierung des Apfels
        while True:
            new_apple_pos = [random.randint(0, (screen_width // apple_size) - 1) * apple_size,
                             random.randint(0, (screen_height // apple_size) - 1) * apple_size]
            if new_apple_pos not in snake_body:
                apple_pos[0] = new_apple_pos[0]
                apple_pos[1] = new_apple_pos[1]
                break
        score += 10
        snake_body.append(snake_body[-1])  # Die Schlange wächst

# Hauptspielschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    move_snake()
    eat_apple()

    screen.fill(BLACK)

    pygame.draw.rect(screen, RED, pygame.Rect(apple_pos[0], apple_pos[1], apple_size, apple_size))
    
    for pos in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (screen_width / 2, 10)
    screen.blit(score_surface, score_rect)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
