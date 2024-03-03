import pygame
import sys

#Initialize Pygame
pygame.init()

#Set the dimensions of the window
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30
clock = pygame.time.Clock()

#Load the sprite sheet
sprite_sheet = pygame.image.load("tooth.png")

#Define the dimensions of each frame in the sprite sheet
FRAME_WIDTH = sprite_sheet.get_width() // 3
FRAME_HEIGHT = sprite_sheet.get_height() // 4

def main():
    # Initialize variables for animation
    frame_index = 0
    frame_counter = 0
    animation_speed = 5  # Adjust this to change animation speed

#Game loop
    while True:
        SCREEN.fill((0, 0, 0))  # Clear the screen

#Calculate the position of the current frame in the sprite sheet
        frame_x = (frame_index % 3) * FRAME_WIDTH
        frame_y = (frame_index // 3) * FRAME_HEIGHT

#Extract the current frame from the sprite sheet
        frame = sprite_sheet.subsurface(pygame.Rect(frame_x, frame_y, FRAME_WIDTH, FRAME_HEIGHT))

#Display the current frame
        SCREEN.blit(frame, (WIDTH // 2 - FRAME_WIDTH // 2, HEIGHT // 2 - FRAME_HEIGHT // 2))

#Update the display
        pygame.display.flip()

#Increment frame counter
        frame_counter += 1

#If enough time has passed, move to the next frame
        if frame_counter >= animation_speed:
            frame_index = (frame_index + 1) % 12
            frame_counter = 0

#Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #sys.exit()

        # Control the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()