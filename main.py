import pygame
import random
import time
from block import Block  # Import de la classe Block

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
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
TRANSPARENT_NOIR = (0, 0, 0, 150)  # Noir semi-transparent

# Chargement des images
background = pygame.image.load('fond.png')
original_trial = pygame.image.load('trial.png')
trial_texture = pygame.transform.scale(original_trial, (100, 100))

x_background = 0
score = 0

# Fonction pour dessiner un rectangle semi-transparent
def draw_transparent_rect(x, y, width, height, color):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill(color)
    screen.blit(overlay, (x, y))

# Fonction pour afficher le texte
def draw_text(text, x, y, color, size=24):
    font = pygame.font.Font("Police.ttf", 17)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Fonction pour la barre de progression
def draw_progress_bar(progress, target):
    draw_transparent_rect(45, 95, 510, 40, TRANSPARENT_NOIR)  # Fond noir transparent
    pygame.draw.rect(screen, VERT, (50, 100, 500 * progress, 30))
    pygame.draw.line(screen, BLEU, (50 + 500 * (target / 100), 100), (50 + 500 * (target / 100), 130), 5)

def start_new_game():
    return random.randint(20, 80)

running = True
blocks = [Block(start_new_game(), 400)]
progress = 0.0
confirmation = False
scrolling = False
scrolling_timer = 0
scroll_speed = 4
scroll_duration = 3.0

while running:
    screen.fill(NOIRE)
    screen.blit(background, (x_background, 0))
    screen.blit(trial_texture, (200, screen_height - 119))
    screen.blit(background, (x_background + background.get_width(), 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                confirmation = True
            if event.key == pygame.K_SPACE:
                progress += 0.02

    progress -= 0.001
    progress = max(0.0, min(1.0, progress))

    draw_progress_bar(progress, blocks[-1].target)
    draw_transparent_rect(15, 15, 570, 77, TRANSPARENT_NOIR)  # Fond pour le texte
    draw_text(f"OBJECTIF: {blocks[-1].target}", 20, 20, BLANC)
    draw_text(f"PROGRESSION: {progress * 100:.1f}", 20, 50, BLANC)
    draw_text(f"SCORE: {score}", 430, 20, BLANC)

    if confirmation:
        if abs(progress * 100 - blocks[-1].target) <= 1.5:
            draw_text("VALIDE!", 200, 200, VERT)
            score += 1
            progress = 0.0
            pygame.display.flip()
            time.sleep(0.5)
            blocks[-1].moving_out = True
            new_block = Block(start_new_game(), (screen_width + 180))
            new_block.moving_in = True
            blocks.append(new_block)
            scrolling = True
            scrolling_timer = time.time()
        else:
            draw_text("GAME OVER", 200, 200, ROUGE, 50)
            pygame.display.flip()
            score = 0
            time.sleep(2)
            blocks = [Block(start_new_game(), 400)]
            x_background = 0
            progress = 0.0
        confirmation = False

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

    for block in blocks[:]:
        if block.moving_out and block.x < -block.width:
            blocks.remove(block)
        block.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
