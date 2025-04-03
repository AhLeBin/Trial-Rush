import pygame
import random
import time

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

# Chargement de l'image de fond
background = pygame.image.load('fond.png')
x_background = 0  # Conserver la position du fond entre les manches

# Score
score = 0

class Block:
    def __init__(self, target, x_pos=400):
        self.target = target
        self.height = target * 2
        self.y = screen_height - self.height - 19
        self.x = x_pos  # Position initiale
        self.moving_out = False
        self.moving_in = False

    def move_out(self, speed):
        self.x -= speed  # Déplace le bloc vers la gauche
        return self.x < -100  # Disparaît une fois hors de l'écran

    def move_in(self, speed):
        if self.x > 400:
            self.x -= speed

    def draw(self):
        pygame.draw.rect(screen, ROUGE, (self.x, self.y, 100, self.height))


def draw_text(text, x, y, color, size=24):
    font = pygame.font.Font("Police.ttf", 17)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def get_progress_color(progress, target):
    if progress < target / 100:
        return VERT
    else:
        intensite = min(255, int((progress - target / 100) * 255 * 2))
        return (255, 255 - intensite, 0)


def draw_progress_bar(progress, target):
    pygame.draw.rect(screen, NOIRE, (50, 100, 500, 30))  # Fond noir
    pygame.draw.rect(screen, get_progress_color(progress, target), (50, 100, 500 * progress, 30))
    pygame.draw.line(screen, BLEU, (50 + 500 * (target / 100), 100), (50 + 500 * (target / 100), 130), 5)


def start_new_game():
    return random.randint(20, 80)


running = True
blocks = [Block(start_new_game(), 400)]  # Premier bloc déjà en place
progress = 0.0
confirmation = False
scrolling = False
scrolling_timer = 0
scroll_speed = 4  # Augmentation de la vitesse
scroll_duration = 3.0  # Passage à 3 secondes

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
                progress += 0.02  # Augmente uniquement lorsqu'on appuie sur espace

    progress -= 0.001  # Descend lentement en permanence si on n'appuie pas
    progress = max(0.0, min(1.0, progress))

    draw_progress_bar(progress, blocks[-1].target)
    draw_text(f"OBJECTIF: {blocks[-1].target}", 20, 20, NOIRE)
    draw_text(f"PROGRESSION: {progress * 100:.1f}", 20, 50, NOIRE)
    draw_text(f"SCORE: {score}", 430, 20, NOIRE)

    if confirmation:
        if abs(progress * 100 - blocks[-1].target) <= 1.5:
            draw_text("VALIDE!", 200, 200, VERT)
            score += 1
            pygame.display.flip()
            time.sleep(0.5)
            blocks[-1].moving_out = True  # Ancien bloc part vers la gauche
            new_block = Block(start_new_game(), (screen_width+180))

            new_block.moving_in = True  # Nouveau bloc entre depuis la droite
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

        confirmation = False

    # Gérer le défilement du fond et des blocs pendant 3 secondes
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

    # Affichage des blocs
    for block in blocks[:]:
        if block.moving_out and block.x < -100:
            blocks.remove(block)
        block.draw()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
