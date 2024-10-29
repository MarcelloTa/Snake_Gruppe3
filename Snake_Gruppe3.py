import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Einfaches Snake-Spiel')

snake_size = 20
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'

apple_size = 20
apple_pos = [random.randint(0, (screen_width // apple_size) - 1) * apple_size,
             random.randint(0, (screen_height // apple_size) - 1) * apple_size]

# Variable für das Wachstum
wachsen = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        direction = 'RIGHT'
    elif keys[pygame.K_LEFT]:
        direction = 'LEFT'
    elif keys[pygame.K_DOWN]:
        direction = 'DOWN'
    elif keys[pygame.K_UP]:
        direction = 'UP'

    # Snake bewegen
    if direction == 'RIGHT':
        snake_pos[0] += snake_size
    elif direction == 'LEFT':
        snake_pos[0] -= snake_size
    elif direction == 'DOWN':
        snake_pos[1] += snake_size
    elif direction == 'UP':
        snake_pos[1] -= snake_size

    # Snake-Körper aktualisieren
    snake_body.insert(0, list(snake_pos))

    # Überprüfen, ob die Snake einen Apfel gesammelt hat
    if snake_pos == apple_pos:
        wachsen += 1

        apple_pos = [random.randint(0, (screen_width // apple_size) - 1) * apple_size,
                     random.randint(0, (screen_height // apple_size) - 1) * apple_size]
    else:
        # Letztes Segment entfernen, wenn kein Wachstum
        snake_body.pop()

    # Snake zeichnen
    screen.fill((0, 0, 0))
    for pos in snake_body:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    # Apfel zeichnen
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(apple_pos[0], apple_pos[1], apple_size, apple_size))

    pygame.display.flip()
    pygame.time.delay(100)