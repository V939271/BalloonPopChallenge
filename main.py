import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TIMER = 120  # 2 minutes
BALLOON_SPEED = 0.3  # Slow but visible
POP_REWARD = 2
BALLOON_SPAWN_DELAY = 1000  # spawn every 1 second

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Pop Challenge")

# Fonts
font = pygame.font.Font(None, 36)

# Timer setup
timer = TIMER * 1000  # convert to milliseconds
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, RED, [0, 0, 50, 70])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.y = SCREEN_HEIGHT  # float for accurate movement
        self.rect.y = int(self.y)

    def update(self):
        self.y -= BALLOON_SPEED
        self.rect.y = int(self.y)
        if self.rect.y < -self.rect.height:
            self.kill()

# Balloon group
balloons = pygame.sprite.Group()

# Game variables
score = 0
next_balloon_spawn_time = pygame.time.get_ticks() + BALLOON_SPAWN_DELAY
running = True

# Game loop
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            timer -= 1000
            if timer <= 0:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for balloon in balloons:
                    if balloon.rect.collidepoint(event.pos):
                        balloon.kill()
                        score += POP_REWARD

    # Fill background
    screen.fill(WHITE)

    # Spawn balloon
    if current_time >= next_balloon_spawn_time:
        new_balloon = Balloon()
        balloons.add(new_balloon)
        next_balloon_spawn_time = current_time + BALLOON_SPAWN_DELAY

    # Update and draw
    balloons.update()
    balloons.draw(screen)

    # Score
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    # Timer
    timer_text = font.render(f"Time: {timer // 1000}", True, RED)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    pygame.display.flip()

# Final score screen
screen.fill(WHITE)
final_text = font.render("Time's Up!", True, RED)
score_result = font.render(f"Your Total Score: {score}", True, RED)
screen.blit(final_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 40))
screen.blit(score_result, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 10))
pygame.display.flip()

pygame.time.wait(3000)  # 3 sec pause before exit

pygame.quit()
sys.exit()
