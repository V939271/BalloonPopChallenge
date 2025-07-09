import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TIMER = 120  # seconds
BALLOON_SPEED = 1.5  # Balanced speed
POP_REWARD = 2
BALLOON_SPAWN_DELAY = 1500  # Increased delay to 1.5 seconds

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Pop Challenge")

# Font
font = pygame.font.Font(None, 36)

# Timer setup
timer = TIMER * 1000  # milliseconds
pygame.time.set_timer(pygame.USEREVENT, 1000)  # fire every 1 second

# Clock to control FPS
clock = pygame.time.Clock()

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, RED, [0, 0, 50, 70])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = SCREEN_HEIGHT

    def update(self):
        self.rect.y -= BALLOON_SPEED
        if self.rect.y + self.rect.height < 0:
            self.kill()

# Balloon group
balloons = pygame.sprite.Group()

# Game variables
score = 0
next_balloon_spawn_time = pygame.time.get_ticks() + BALLOON_SPAWN_DELAY

# Main game loop
running = True
while running:
    clock.tick(60)  # Cap the frame rate to 60 FPS
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.USEREVENT:
            timer -= 1000
            if timer <= 0:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for balloon in balloons:
                if balloon.rect.collidepoint(event.pos):
                    balloon.kill()
                    score += POP_REWARD

    screen.fill(WHITE)

    # Spawn balloons
    if current_time >= next_balloon_spawn_time:
        balloon = Balloon()
        balloons.add(balloon)
        next_balloon_spawn_time = current_time + BALLOON_SPAWN_DELAY

    # Update and draw balloons
    balloons.update()
    balloons.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    # Draw timer
    timer_text = font.render(f"Time: {timer // 1000}", True, RED)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
