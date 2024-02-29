import pygame
import random

# Open a file in write mode ('w')
with open('new_file.txt', 'w') as f:
    # Write content to the file
    f.write('Hello, this is a new file created using Python!')

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 5

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

    def move_up(self):
        self.y -= self.speed
        self.rect.y = self.y

    def move_down(self):
        self.y += self.speed
        self.rect.y = self.y

# Define the ball class
class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 10
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.speed_x = 5 * random.choice((1, -1))
        self.speed_y = 5 * random.choice((1, -1))

    def draw(self):
        pygame.draw.ellipse(WIN, WHITE, self.rect)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off the top and bottom
        if self.y <= 0 or self.y >= HEIGHT - self.size:
            self.speed_y *= -1

        self.rect.x = self.x
        self.rect.y = self.y

    def bounce(self):
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(ai_paddle.rect):
            self.speed_x *= -1

# AI opponent with a 10% chance of winning
def ai_move():
    if random.random() < 0.1:
        return random.choice(["up", "down"])
    else:
        if ball.rect.y < ai_paddle.rect.y + ai_paddle.height // 2:
            return "up"
        elif ball.rect.y > ai_paddle.rect.y + ai_paddle.height // 2:
            return "down"
        else:
            return "stay"

# Create paddles and ball
player_paddle = Paddle(20, HEIGHT // 2 - 50)
ai_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - 50)
ball = Ball()

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.rect.y > 0:
        player_paddle.move_up()
    if keys[pygame.K_s] and player_paddle.rect.y < HEIGHT - player_paddle.height:
        player_paddle.move_down()

    # AI opponent
    ai_decision = ai_move()
    if ai_decision == "up" and ai_paddle.rect.y > 0:
        ai_paddle.move_up()
    elif ai_decision == "down" and ai_paddle.rect.y < HEIGHT - ai_paddle.height:
        ai_paddle.move_down()

    # Move ball
    ball.move()
    ball.bounce()

    # Check for scoring
    if ball.rect.x < 0 or ball.rect.x > WIDTH:
        ball.reset()

    # Draw everything
    WIN.fill(BLACK)
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()
    pygame.draw.aaline(WIN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))  # Center line
    pygame.display.update()

    clock.tick(60)

pygame.quit()
