import pygame

# Paramètres de la fenêtre
screen_height = 400
texture_size = 50

# Chargement et redimensionnement de la texture roche
rock_texture = pygame.image.load('roche.jpg')
rock_texture = pygame.transform.scale(rock_texture, (texture_size, texture_size))

class Block:
    def __init__(self, target, x_pos=400):
        self.target = target
        self.width = 100
        self.height = target * 2
        self.y = screen_height - self.height - 19
        self.x = x_pos
        self.moving_out = False
        self.moving_in = False

    def move_out(self, speed):
        self.x -= speed
        return self.x < -self.width

    def move_in(self, speed):
        if self.x > 400:
            self.x -= speed

    def draw(self, screen):
        for i in range(0, self.width, texture_size):
            for j in range(0, self.height, texture_size):
                if j + texture_size > self.height:
                    height_remainder = self.height - j
                    cropped_texture = rock_texture.subsurface((0, 0, texture_size, height_remainder))
                    screen.blit(cropped_texture, (self.x + i, self.y + j))
                else:
                    screen.blit(rock_texture, (self.x + i, self.y + j))
