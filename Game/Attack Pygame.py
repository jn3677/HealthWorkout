import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Health Bar Example")

# Set up player
player_x, player_y = 100, 100
player_width, player_height = 50, 50
player_color = (255, 0, 0)

# Set up health bar
health = 100
health_bar_width, health_bar_height = 200, 20
health_bar_color = (0, 255, 0)

# Set up victory text
font = pygame.font.Font(None, 36)
victory_text = font.render("Victory!", True, (0, 0, 255))
text_rect = victory_text.get_rect(center=(width // 2, height // 2))

# Set up clock
clock = pygame.time.Clock()

# Define attack function
def attack():
    global health
    health -= 10
    if health < 0:
        health = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Check if the 'K' key is pressed
    if keys[pygame.K_k]:
        attack()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # Draw the health bar background
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, health_bar_width, health_bar_height))
    
    # Draw the filled portion of the health bar based on the current health
    pygame.draw.rect(screen, health_bar_color, (50, 50, health * (health_bar_width / 100), health_bar_height))

    # Check if the player has won (health is zero)
    if health == 0:
        screen.blit(victory_text, text_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
