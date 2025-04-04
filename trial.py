import pygame
import time

class Trial:
    def __init__(self, initial_y, texture):
        self.texture = texture
        self.y_initial = initial_y
        self.y = initial_y

        self.anim_state = "idle"
        self.anim_start = 0
        self.target_block = None

        self.duration_up = 1.3
        self.duration_hold = 1.1
        self.duration_down = 0.6

    def start_animation(self, target_block):
        self.anim_state = "up"
        self.anim_start = time.time()
        self.target_block = target_block

    def update(self):
        if self.anim_state == "idle" or not self.target_block:
            return

        elapsed = time.time() - self.anim_start
        target_y = self.target_block.y - self.texture.get_height()

        if self.anim_state == "up":
            if elapsed < self.duration_up:
                progress = elapsed / self.duration_up
                self.y = self.y_initial + (target_y - self.y_initial) * progress
            else:
                self.y = target_y
                self.anim_state = "hold"
                self.anim_start = time.time()

        elif self.anim_state == "hold":
            if elapsed < self.duration_hold:
                self.y = target_y
            else:
                self.anim_state = "down"
                self.anim_start = time.time()

        elif self.anim_state == "down":
            if elapsed < self.duration_down:
                progress = elapsed / self.duration_down
                self.y = target_y + (self.y_initial - target_y) * progress
            else:
                self.y = self.y_initial
                self.anim_state = "idle"
                self.target_block = None

    def draw(self, screen, x):
        screen.blit(self.texture, (x, self.y))
