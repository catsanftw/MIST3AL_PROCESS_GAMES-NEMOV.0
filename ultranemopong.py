 
import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH = 800
HEIGHT = 400
BALL_RADIUS = 10
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 100
FPS = 60

# Create the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

class Ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = random.choice([-5, 5])
        self.vy = random.choice([-5, 5])

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (int(self.x), int(self.y)), BALL_RADIUS)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

def main():
    clock = pygame.time.Clock()
    ball = Ball()
    paddle1 = Paddle(PADDLE_WIDTH + 10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(WIDTH - PADDLE_WIDTH * 2 - 10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    score1 = 0
    score2 = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # Move paddles based on user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.y -= 5
        elif keys[pygame.K_s]:
            paddle1.y += 5
        elif keys[pygame.K_UP]:
            paddle2.y -= 5
        elif keys[pygame.K_DOWN]:
            paddle2.y += 5

        # Keep paddles within screen bounds
        if paddle1.y < 0:
            paddle1.y = 0
        elif paddle1.y + PADDLE_HEIGHT > HEIGHT:
            paddle1.y = HEIGHT - PADDLE_HEIGHT
        if paddle2.y < 0:
            paddle2.y = 0
        elif paddle2.y + PADDLE_HEIGHT > HEIGHT:
            paddle2.y = HEIGHT - PADDLE_HEIGHT

        # Update ball position and check for collisions with paddles or screen edges
        ball.x += ball.vx
        ball.y += ball.vy

        if ball.y < BALL_RADIUS or ball.y > HEIGHT - BALL_RADIUS:
            ball.vy *= -1

        collided_left = (ball.x - BALL_RADIUS <= paddle1.x + PADDLE_WIDTH) and \
                          (paddle1.y <= ball.y <= paddle1.y + PADDLE_HEIGHT)
        collided_right = (ball.x + BALL_RADIUS >= paddle2.x) and \
                           (paddle2.y <= ball.y <= paddle2.y + PADDLE_HEIGHT)

        if collided_left or collided_right:
            ball.vx *= -1
        elif ball.x < 0:  # Scored for player 2
            score2 += 1
            ball = Ball()
        elif ball.x > WIDTH:  # Scored for player 1
            score1 += 1
            ball = Ball()

        # Draw everything on the screen
        win.fill((0, 0, 0))
        paddle1.draw(win)
        paddle2.draw(win)
        ball.draw(win)

        # Update scores and display them on the screen
        font = pygame.font.Font(None, 36)
        text_surface1 = font.render(str(score1), True, (255, 255, 255))
        text_surface2 = font.render(str(score2), True, (255, 255, 255))
        win.blit(text_surface1, (WIDTH // 2 - 50, 10))
        win.blit(text_surface2, (WIDTH // 2 + 10, 10))

        # Flip the display and update the clock
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
