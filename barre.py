import pygame
import random
import time

# Initialisation de pygame
pygame.init()  # initialise tous les modules de Pygame, comme la gestion des fenêtres et des événements


# Paramètres de la fenêtre
screen_width = 600  # Largeur de la fenêtre du jeu en pixels
screen_height = 400  # Hauteur de la fenêtre du jeu en pixels
screen = pygame.display.set_mode((screen_width, screen_height))  # Crée la fenêtre de jeu
pygame.display.set_caption("Jauge de Progression")  # titre de la fenêtre du jeu


# Couleurs
NOIRE = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)


# Police
font = pygame.font.SysFont("Arial", 24)  # police de caractères pour afficher le texte à l'écran


# Fonction pour afficher le texte
def draw_text(text, x, y, color):

    label = font.render(text, True, color)  # Crée une image de texte avec la police définie
    screen.blit(label, (x, y))  # Affiche cette image de texte à la position (x, y) sur l'écran


# Fonction pour obtenir la couleur de la barre en fonction du dépassement de l'objectif
def get_progress_color(progress, target):

    if progress < target / 100:
        return VERT  # Si la progression est inférieure à l'objectif, la barre est verte

    else:
        # Si la progression dépasse l'objectif, la couleur varie de vert à rouge.
        intensite = min(255, int((progress - target / 100) * 255 * 2))  # Calcul de l'intensité du rouge (plus la progression dépasse l'objectif, plus le rouge devient intense)
        return (255, 255 - intensite, 0)  # La couleur varie de vert (lorsque red_intensity est faible) à rouge (lorsque red_intensity est élevé)


# Fonction pour dessiner la barre de progression
def draw_progress_bar(progress, target):

    pygame.draw.rect(screen, BLANC, (50, 100, 500, 30))  # Dessine le fond de la barre de progression (rectangle blanc)
    pygame.draw.rect(screen, get_progress_color(progress, target), (50, 100, 500 * progress, 30))  # Dessine la barre de progression en fonction de la progression
    pygame.draw.line(screen, BLEU, (50 + 500 * (target / 100), 100), (50 + 500 * (target / 100), 130), 5)  # Dessine une ligne bleue à l'endroit de l'objectif (position de la barre de progression selon l'objectif)


# Fonction pour relancer une nouvelle partie
def start_new_game():

    return random.randint(20, 80)  # Détermine un objectif aléatoire entre 20% et 80% à atteindre


# Boucle principale
running = True

while running:

    progress = 0.0  # Initialisation de la progression à 0% au début de chaque partie
    target = start_new_game()  # Détermine un nouvel objectif aléatoire pour cette partie
    last_time = time.time()  # Enregistre le temps actuel (pour savoir quand la barre de progression doit diminuer)
    time_limit = 0.1  # Le temps (en secondes) pendant lequel la barre de progression continue d'augmenter si la touche Espace est pressée
    game_over = False  # Indicateur pour savoir si la partie est terminée

    while not game_over:
        screen.fill(NOIRE)  # Efface l'écran en remplissant la fenêtre avec la couleur noire

        # Gestion des événements
        for event in pygame.event.get():  # Vérifie les événements utilisateur (comme les frappes de touches)
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre, met fin à la partie
                running = False
                game_over = True
            if event.type == pygame.KEYDOWN:  # Si une touche est pressée
                if event.key == pygame.K_RETURN:  # Si la touche Entrée est pressée, la partie est terminée
                    game_over = True
                if event.key == pygame.K_SPACE:  # Si la barre d'espace est pressée, commence à augmenter la progression
                    last_time = time.time()  # Met à jour le temps lorsque la barre d'espace est pressée

        # Calcul de la progression
        if time.time() - last_time < time_limit:  # Si l'écart de temps depuis la dernière pression d'espace est inférieur à time_limit (0.1 seconde)
            progress += 0.005  # La progression augmente de 0.5% par frame
            if progress > 1.0:  # Si la progression dépasse 100%, on la limite à 100%
                progress = 1.0
        else:
            progress -= 0.001  # Si la barre d'espace n'est plus pressée, la progression diminue de 0.1% par frame
            if progress < 0:  # Si la progression devient inférieure à 0%, on la limite à 0%
                progress = 0.0

        # Dessin de la barre de progression et du texte
        draw_progress_bar(progress, target)  # Dessine la barre de progression avec la couleur et la taille appropriées
        draw_text(f"Objectif: {target}%", 20, 20, BLANC)  # Affiche l'objectif à atteindre (en %)
        draw_text(f"Progression: {progress * 100:.1f}%", 20, 50, BLANC)  # Affiche la progression actuelle en %

        # Vérification du succès ou de l'échec
        if abs(progress * 100 - target) <= 1:  # Si la différence entre la progression et l'objectif est inférieure ou égale à 1% (réussite à 1% près)
            draw_text(f"Réussi! ({progress*100:.1f}%)", 200, 200, VERT)  # Affiche "Réussi!" en vert
        elif progress > 0:  # Si la progression est inférieure à l'objectif et qu'elle est supérieure à 0
            draw_text(f"Echec! ({progress*100:.1f}%)", 200, 200, ROUGE)  # Affiche "Echec!" en rouge

        # Mise à jour de l'affichage
        pygame.display.flip()  # Met à jour l'écran pour afficher les nouvelles informations

        # Rafraîchissement de l'écran (limité à 60 frames par seconde)
        pygame.time.Clock().tick(60)

        # Vérifie si la progression atteint l'objectif ou est nulle (lorsque l'utilisateur doit appuyer sur "Entrée" pour recommencer)
        if abs(progress * 100 - target) <= 1:
            draw_text("Appuyez sur Entrée pour recommencer", 150, 250, BLANC)
            pygame.display.flip()

    # Attente que l'utilisateur appuie sur "Entrée" pour recommencer la partie
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Si la touche "Entrée" est pressée, recommence une nouvelle partie
                    game_over = False

# Fermeture de Pygame
pygame.quit()  # Ferme Pygame proprement lorsque la boucle principale est terminée
