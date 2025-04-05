import pygame
import random
import time
import sqlite3
from block import Block
from trial import Trial

# Initialisation
pygame.init()

#base de donnée
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Fenêtre
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Barre et Défilement Fond")

# Couleurs
NOIRE = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
TRANSPARENT_NOIR = (0, 0, 0, 150)

# Fond & Trialiste
background = pygame.image.load('fond.png')
trial_texture = pygame.transform.scale(pygame.image.load('trial.png'), (100, 100))
trial = Trial(screen_height - 119, trial_texture)

# Variables principales
x_background = 0
score = 0
progress = 0.0
confirmation = False
scrolling = False
scrolling_timer = 0
scroll_speed = 4
scroll_duration = 3.0

blocks = [Block(random.randint(20, 80), 400)]

# Fonctions utilitaires
def draw_transparent_rect(x, y, width, height, color):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill(color)
    screen.blit(overlay, (x, y))

def draw_text(text, x, y, color, size=24):
    font = pygame.font.Font("Police.ttf", 17)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_progress_bar(progress, target):
    draw_transparent_rect(45, 95, 510, 40, TRANSPARENT_NOIR)
    pygame.draw.rect(screen, VERT, (50, 100, 500 * progress, 30))
    pygame.draw.line(screen, BLEU, (50 + 500 * (target / 100), 100), (50 + 500 * (target / 100), 130), 5)

# Boucle principale
running = True
while running:
    screen.fill(NOIRE)
    screen.blit(background, (x_background, 0))
    screen.blit(background, (x_background + background.get_width(), 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                confirmation = True
            if event.key == pygame.K_SPACE:
                progress += 0.02

    # Progression
    progress -= 0.001
    progress = max(0.0, min(1.0, progress))

    # Affichage de l'UI
    draw_progress_bar(progress, blocks[-1].target)
    draw_transparent_rect(15, 15, 570, 77, TRANSPARENT_NOIR)
    draw_text(f"OBJECTIF: {blocks[-1].target}", 20, 20, BLANC)
    draw_text(f"PROGRESSION: {progress * 100:.1f}", 20, 50, BLANC)
    draw_text(f"SCORE: {score}", 430, 20, BLANC)

    # Validation
    if confirmation:
        if abs(progress * 100 - blocks[-1].target) <= 1.5:
            draw_text("VALIDE!", 200, 200, VERT)
            score += 1
            progress = 0.0
            pygame.display.flip()
            time.sleep(0.5)

            blocks[-1].moving_out = True
            new_block = Block(random.randint(20, 80), screen_width + 180)
            new_block.moving_in = True
            blocks.append(new_block)

            scrolling = True
            scrolling_timer = time.time()

            # Animation trialiste vers bloc validé
            trial.start_animation(blocks[-2])
        else:
            draw_text("GAME OVER", 200, 200, ROUGE, 50)
            pygame.display.flip()
            score = 0
            time.sleep(2)

            blocks = [Block(random.randint(20, 80), 400)]
            x_background = 0
            progress = 0.0
            trial.y = trial.y_initial
            trial.anim_state = "idle"
            trial.target_block = None

        confirmation = False

    # Scroll fond et blocs
    if scrolling:
        elapsed_time = time.time() - scrolling_timer
        if elapsed_time <= scroll_duration:
            x_background -= scroll_speed
            if x_background <= -background.get_width():
                x_background = 0

            for block in blocks:
                if block.moving_out:
                    block.move_out(scroll_speed)
                if block.moving_in:
                    block.move_in(scroll_speed)
        else:
            scrolling = False

    # Animation & affichage trialiste
    trial.update()
    trial.draw(screen, 200)

    # Affichage des blocs
    for block in blocks[:]:
        if block.moving_out and block.x < -block.width:
            blocks.remove(block)
        block.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
