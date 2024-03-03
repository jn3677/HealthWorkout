import pygame

class Fighter():
    def __init__(self, x,y):
        super().__init__()
        self.rect = pygame.Rect((x,y,80,180))
        self.health = 200
        self.load_images()  # Load sprite sheet images
        self.frame_index = 0
        self.animation_speed = 5
        self.image = self.frames[self.frame_index]

    def attack(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0 

    

    def load_images(self):
        sprite_sheet = pygame.image.load("tooth.png")
        frame_width = sprite_sheet.get_width() // 3
        frame_height = sprite_sheet.get_height() // 4
        self.frames = []

        for row in range(4):
            for col in range(3):
                frame_x = col * frame_width
                frame_y = row * frame_height
                frame = sprite_sheet.subsurface(pygame.Rect(frame_x, frame_y, frame_width, frame_height))
                self.frames.append(frame)

    def update_animation(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.image = self.frames[self.frame_index]



    #def draw(self, surface):
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


