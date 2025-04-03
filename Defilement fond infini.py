import pygame

# Initialisation de pygame
pygame.init()

# Paramètres de la fenêtre
screen_width = 600  # Largeur de la fenêtre du jeu en pixels
screen_height = 400  # Hauteur de la fenêtre du jeu en pixels
screen = pygame.display.set_mode((screen_width, screen_height))  # Crée la fenêtre de jeu
pygame.display.set_caption("Fond qui défile")  # Titre de la fenêtre du jeu

# Chargement de l'image de fond
background = pygame.image.load('fond.png')

# Position initiale du fond
x_background = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Vérifie si l'utilisateur ferme la fenêtre
            running = False

    # Défilement du fond
    x_background -= 3  # Déplace le fond vers la gauche
    if x_background <= -background.get_width():  # Si le fond est complètement à gauche
        x_background = 0  # Réinitialise la position du fond

    # Affichage du fond (deux fois pour créer l'effet de défilement)
    screen.blit(background, (x_background, 0))  # Affiche la première partie du fond
    screen.blit(background, (x_background + background.get_width(), 0))  # Affiche la deuxième partie à droite

    pygame.display.update()  # Met à jour l'affichage

    # Limite la vitesse du défilement (en FPS)
    pygame.time.Clock().tick(60)

pygame.quit()  # Ferme pygame correctement lorsque la boucle se termine
