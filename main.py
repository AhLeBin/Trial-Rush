import pygame
import random
import time
import sqlite3
from block import Bloc
from trial import Trial

# Initialisation de Pygame
pygame.init()

# Connexion à la base de données SQLite
connexion = sqlite3.connect('data.db')
curseur = connexion.cursor()

# Paramètres de la fenêtre
longueur_fenetre = 600
largeur_fenetre = 400
fenetre = pygame.display.set_mode((longueur_fenetre, largeur_fenetre))
pygame.display.set_caption("Trial Rush") # Nom de la fenêtre

# Définition des couleurs
NOIRE = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
TRANSPARENT_NOIR = (0, 0, 0, 150) # Noir avec une certaine transparence

# Chargement de l'image de fond
fond = pygame.image.load('fond.png')

# Chargement de l'image de trial et mise à la bonne taille
trial_texture = pygame.transform.scale(pygame.image.load('trial.png'), (100, 100))
trial = Trial(largeur_fenetre - 119, trial_texture) # Liaison avec la classe Trial

# Variables principales
x_fond = 0  # Position du fond pour le défilement
score = 0  # Score initial
progression = 0.0  # Progression initiale
confirmation = False  # Variable pour valider la progression
animation = False  # Variable pour gérer l'animation
animation_timer = 0  # Timer pour l'animation
vitesse_animation = 4  # Vitesse de l'animation
duree_animation = 3.0  # Durée de l'animation

# Tailles de police
FONT_LARGE = 40
FONT_MEDIUM = 30

# Liste des blocs (initialisation avec un bloc de taille aléatoire)
blocs = [Bloc(random.randint(20, 80), 400)]

# Fonction pour dessiner un fond transparent (pour l'ui)
def dessiner_fond_transparent(x, y, longeure, hauteure, couleur):
    fond_transparent = pygame.Surface((longeure, hauteure), pygame.SRCALPHA) # Crée une surface avec transparence
    fond_transparent.fill(couleur)
    fenetre.blit(fond_transparent, (x, y))

# Fonction pour dessiner du texte à l'écran
def dessiner_texte(texte, x, y, couleure, size=24):
    police = pygame.font.Font("Police.ttf", 17)  # Police utilisée
    contenu = police.render(texte, True, couleure)  # Création du texte
    fenetre.blit(contenu, (x, y))  # Affichage du texte à la position (x, y)

# Fonction pour dessiner la barre de progression
def dessiner_barre_progression(progression, objectif):
    dessiner_fond_transparent(45, 95, 510, 40, TRANSPARENT_NOIR)  # Dessiner le fond de la barre de progression
    pygame.draw.rect(fenetre, VERT, (50, 100, 500 * progression, 30))  # Dessiner la barre verte de progression
    pygame.draw.line(fenetre, BLEU, (50 + 500 * (objectif / 100), 100), (50 + 500 * (objectif / 100), 130), 5)  # Indicateur de l'objectif

# Boucle principale du jeu
running = True
while running:
    fenetre.fill(NOIRE)  # Remplir l'écran avec la couleur noire
    fenetre.blit(fond, (x_fond, 0))  # Afficher le fond à la position x_fond
    fenetre.blit(fond, (x_fond + fond.get_width(), 0))  # Afficher une seconde image du fond pour créer un défilement

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Quitter le jeu si la fenêtre est fermée

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                confirmation = True  # Valider la progression lorsque la touche "Entrée" est appuyée
            if event.key == pygame.K_SPACE:
                progression += 0.02  # Augmenter la progression lorsque la barre d'espace est appuyée

    # Mettre à jour la progression (réduction progressive)
    progression -= 0.001
    progression = max(0.0, min(1.0, progression))  # Assurer que la progression est entre 0 et 1

    # Affichage de l'interface utilisateur
    dessiner_barre_progression(progression, blocs[-1].objectif)
    dessiner_fond_transparent(15, 15, 570, 77, TRANSPARENT_NOIR)
    dessiner_texte(f"OBJECTIF: {blocs[-1].objectif}", 20, 20, BLANC)
    dessiner_texte(f"PROGRESSION: {progression * 100:.1f}", 20, 50, BLANC)
    dessiner_texte(f"SCORE: {score}", 430, 20, BLANC)

    # Validation de la progression
    if confirmation:
        if abs(progression * 100 - blocs[-1].objectif) <= 1.5:  # Vérifie si la différence entre la progression et l'objectif est inférieure ou égale à 1.5
            dessiner_texte("VALIDE!", 200, 200, VERT)  # Affiche "VALIDE!" si la progression est proche de l'objectif
            score += 1  # Augmenter le score
            progression = 0.0  # Réinitialiser la progression de la barre
            pygame.display.flip()
            time.sleep(0.5)  # Attendre un peu avant de continuer

            blocs[-1].sortie = True  # Le bloc actuel sort
            new_block = Bloc(random.randint(20, 80), longueur_fenetre + 180)  # Créer un nouveau bloc de taille differente
            new_block.entree = True  # Le nouveau bloc entre dans la fenetre
            blocs.append(new_block)  # Ajouter le bloc à la liste

            trial.rotation()
            fond_rotation_x = x_fond  # garder la position actuelle du fond

            while trial.en_rotation:
                # 1. Redessiner le fond à la bonne position
                fenetre.blit(fond, (fond_rotation_x, 0))
                fenetre.blit(fond, (fond_rotation_x + fond.get_width(), 0))

                # 2. Redessiner les blocs
                for bloc in blocs:
                    bloc.dessine(fenetre)

                # 3. Mettre à jour et dessiner le trial
                trial.update()
                trial.dessine(fenetre, 200)

                # 4. Afficher
                pygame.display.flip()
                pygame.time.Clock().tick(60)
            pygame.display.flip()  # Forcer l'affichage de la rotation

            animation = True  # Ensuite seulement on lance l'animation
            animation_timer = time.time()

            # Lancer l'animation de transition du trialiste vers le bloc validé
            trial.depart_animation(blocs[-2])

            animation_timer = time.time()  # Enregistrer le temps de début de l'animation

            # Lancer l'animation de transition du trialiste vers le bloc validé
            trial.depart_animation(blocs[-2])

        elif abs(progression * 100 - blocs[-1].objectif) > 1.5:
            # Sauvegarder la position actuelle du fond
            current_x_fond = x_fond

            # Exécuter l'animation de crash
            trial.crash(fenetre, 200, fond, blocs, score, current_x_fond)

            # Afficher l'écran de game over par-dessus les autres éléments
            try:
                font_large = pygame.font.Font("Police.ttf", 40)
                font_small = pygame.font.Font("Police.ttf", 10)
            except:
                font_large = pygame.font.SysFont("Arial", 40)
                font_small = pygame.font.SysFont("Arial", 10)

            # Créer un fond semi-transparent pour le message
            overlay = pygame.Surface((longueur_fenetre, largeur_fenetre), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Noir semi-transparent
            fenetre.blit(overlay, (0, 0))

            # Afficher les textes
            game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
            restart_text = font_small.render("APPUYER SUR UNE TOUCHE POUR RECOMMENCER", True, (255, 255, 255))

            fenetre.blit(game_over_text, (longueur_fenetre//2 - game_over_text.get_width()//2 ,
                                         largeur_fenetre//2 - 50))
            fenetre.blit(restart_text, (longueur_fenetre//2 - restart_text.get_width()//2,
                                       largeur_fenetre//2 + 40))

            pygame.display.flip()

            # Attendre une touche
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        waiting = False

            # Réinitialisation du jeu
            score = 0
            blocs = [Bloc(random.randint(20, 80), 400)]
            progression = 0.0
            trial.y = trial.y_initial
            trial.etat_animation = "inactif"
            trial.bloc_vise = None
            trial.texture = pygame.transform.scale(pygame.image.load('trial.png'), (100, 100))
            trial.texture_originale = trial.texture.copy()

        confirmation = False  # Réinitialiser la confirmation

    # Défilement du fond et des blocs
    if animation:
        elapsed_time = time.time() - animation_timer  # Temps écoulé depuis le début de l'animation
        if elapsed_time <= duree_animation:  # Si l'animation n'est pas encore terminée
            x_fond -= vitesse_animation  # Déplacer le fond
            if x_fond <= -fond.get_width():  # Si le fond est complètement défilé
                x_fond = 0  # Réinitialiser la position du fond

            for block in blocs:
                if block.sortie:  # Si l'instruction de sortie est donnée
                    block.sort(vitesse_animation) # lancer l'annimation de sortie
                if block.entree:  # Si l'instruction d'entrée est donnée
                    block.entre(vitesse_animation) #lancer l'annimation d'entrée
        else:
            animation = False  # Terminer l'animation si la durée est écoulée

    # Mise à jour et affichage du trialiste
    trial.update()
    trial.dessine(fenetre, 200)

    # Affichage des blocs
    for block in blocs[:]:
        if block.sortie and block.x < -block.largeur:  # Si le bloc sort de l'écran
            blocs.remove(block)  # Supprimer le bloc
        block.dessine(fenetre)  # Dessiner le bloc

    # Rafraîchir l'écran
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limiter le nombre de frames par seconde à 60

# Quitter Pygame à la fin du jeu
pygame.quit()
