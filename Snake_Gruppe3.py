import pygame
import sys
import random

# Window size
frame_size_x = 500
frame_size_y = 500

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Initialize Pygame font
pygame.font.init()
font = pygame.font.Font(None, 28)

fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [100, 50]
snake_body = [[100,90], [90,50], [80,50]]

food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True
direction = 'RIGHT'
change_to = direction

score = 0

# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # snake kann nicht gegengesetzte richtung laufen
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
        score += 10
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(0, (frame_size_x // 10)) * 10, random.randrange(0, (frame_size_y // 10)) * 10]
    food_spawn = True

    game_window.fill((0, 0, 0))
    for pos in snake_body:
        pygame.draw.rect(game_window, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

    if snake_pos in snake_body[1:]:
        sys.exit()

    # Snake food
    pygame.draw.rect(game_window, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Render the score
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    game_window.blit(score_text, (10, 10))

    pygame.display.update()
    fps_controller.tick(15)