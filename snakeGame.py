import pygame
import sys
import random

pygame.init()

#logo = pygame.image.load("logo.png")
#logo = pygame.transform.scale(logo, (40, 30))

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
GAME_HEIGHT = 600
HEADER_HEIGHT = 50
FPS = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

BLOCK_SIZE = 15

snake = [
    [WINDOW_WIDTH // 2, HEADER_HEIGHT + GAME_HEIGHT // 2],
    [WINDOW_WIDTH // 2 - BLOCK_SIZE, HEADER_HEIGHT + GAME_HEIGHT // 2],
    [WINDOW_WIDTH // 2 - (2 * BLOCK_SIZE), HEADER_HEIGHT + GAME_HEIGHT // 2]
]

def spawn_food():
    while True:
        x = random.randint(0, (WINDOW_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (GAME_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE + HEADER_HEIGHT
        if [x, y] not in snake:
            return [x, y]

food_pos = spawn_food()

direction = "RIGHT"
change_to = direction
game_started = False
game_over = False
score = 0
high_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started:
                game_started = True
            elif game_over:
                game_over = False
                snake = [
                    [WINDOW_WIDTH // 2, HEADER_HEIGHT + GAME_HEIGHT // 2],
                    [WINDOW_WIDTH // 2 - BLOCK_SIZE, HEADER_HEIGHT + GAME_HEIGHT // 2],
                    [WINDOW_WIDTH // 2 - (2 * BLOCK_SIZE), HEADER_HEIGHT + GAME_HEIGHT // 2]
                ]
                direction = "RIGHT"
                change_to = "RIGHT"
                food_pos = spawn_food()
                score = 0
            elif event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"
    
    if game_started and not game_over:
        direction = change_to
        
        head = snake[0].copy()
        
        if direction == "UP":
            head[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            head[1] += BLOCK_SIZE
        elif direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif direction == "RIGHT":
            head[0] += BLOCK_SIZE
        
        if (head[0] < 0 or head[0] >= WINDOW_WIDTH or 
            head[1] < HEADER_HEIGHT or head[1] >= WINDOW_HEIGHT):
            game_over = True
        
        for segment in snake:
            if head == segment:
                game_over = True
        
        if not game_over:
            snake.insert(0, head)
        
        if snake[0] == food_pos:
            food_pos = spawn_food()
            score += 10
        else:
            snake.pop()
    
    screen.fill(BLACK)
    
    if not game_started:
        pygame.draw.rect(screen, WHITE, [WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 120, 400, 160])
        
        #screen.blit(logo, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 100))
        
        title_font = pygame.font.Font(None, 48)
        start_font = pygame.font.Font(None, 28)
        
        title = title_font.render("SNAKE GAME", True, BLACK)
        start_text = start_font.render("Press any key to start", True, BLACK)
        
        screen.blit(title, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 80))
        screen.blit(start_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20))
    else:
        pygame.draw.rect(screen, WHITE, [0, 0, WINDOW_WIDTH, HEADER_HEIGHT])
        
        #screen.blit(logo, (10, 10))
        
        title_font = pygame.font.Font(None, 36)
        score_font = pygame.font.Font(None, 24)
        
        title_text = title_font.render("Snake Game", True, BLACK)
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        high_score_text = score_font.render(f"HighScore: {high_score}", True, BLACK)
        
        screen.blit(title_text, (60, 10))
        screen.blit(score_text, (300, 15))
        screen.blit(high_score_text, (450, 15))
        
        pygame.draw.rect(screen, RED, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(screen, DARK_RED, [food_pos[0] + 6, food_pos[1], 3, 4])
        
        for i, segment in enumerate(snake):
            if i == 0:
                pygame.draw.rect(screen, DARK_GREEN, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.circle(screen, WHITE, (segment[0] + 4, segment[1] + 4), 2)
                pygame.draw.circle(screen, WHITE, (segment[0] + 11, segment[1] + 4), 2)
                pygame.draw.circle(screen, BLACK, (segment[0] + 4, segment[1] + 4), 1)
                pygame.draw.circle(screen, BLACK, (segment[0] + 11, segment[1] + 4), 1)
            else:
                pygame.draw.rect(screen, GREEN, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])
    
        if game_over:
            if score > high_score:
                high_score = score
            
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", True, WHITE)
            retry_text = pygame.font.Font(None, 36).render("Press any key to retry", True, WHITE)
            screen.blit(text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
            screen.blit(retry_text, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 20))
    
    pygame.display.flip()
    
    current_fps = FPS + (score // 50)
    clock.tick(current_fps)

pygame.quit()
sys.exit()