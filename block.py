import pygame

# Paramètres de la fenêtre
largeur_fenetre = 400  # Largeur de la fenêtre de jeu
taille_texture = 50  # Taille de chaque tuile de texture (ici, chaque "brique" de roche)

# Chargement et redimensionnement de la texture roche
texture_roche = pygame.image.load('roche.jpg')  # Chargement de l'image de la texture de roche
texture_roche = pygame.transform.scale(texture_roche, (taille_texture, taille_texture))  # Redimensionner la texture pour qu'elle ait la taille spécifiée

class Bloc:
    def __init__(self, objectif, x_pos=400):
        """
        Initialise un objet Bloc avec un objectif et une position sur l'axe X.

        :param objectif: La longueur du bloc est proportionnelle à cet objectif
        :param x_pos: Position initiale du bloc sur l'axe X (défaut à 400)
        """
        self.objectif = objectif  # L'objectif (nombre entre 20 et 80)
        self.largeur = 100  # Largeur fixe du bloc
        self.longueur = objectif * 2  # La longueur du bloc est calculée en fonction de l'objectif
        self.y = largeur_fenetre - self.longueur - 19  # Position verticale du bloc en fonction de la fenêtre
        self.x = x_pos  # Position horizontale du bloc (par défaut 400)
        self.sortie = False  # autorisation d'annimation de sortie
        self.entree = False # autorisation d'annimation d'entrée

    def sort(self, vitesse):
        """
        Gère le déplacement du bloc lorsqu'il sort de la fenêtre.

        :param vitesse: La vitesse à laquelle le bloc se déplace
        :return: True si le bloc a quitté la fenêtre, sinon False
        """
        self.x -= vitesse  # Déplacer le bloc vers la gauche (diminue la position X)
        return self.x < -self.largeur  # Si le bloc dépasse le bord gauche de l'écran, il est considéré comme sorti

    def entre(self, vitesse):
        """
        Gère le déplacement du bloc lorsqu'il entre dans la fenêtre.

        :param vitesse: La vitesse à laquelle le bloc se déplace
        """
        if self.x > 400:  # Si le bloc est toujours à droite de la fenêtre (au-delà de 400)
            self.x -= vitesse  # Déplace le bloc vers la gauche (diminue la position X)

    def dessine(self, fenetre):
        """
        Dessine le bloc à l'écran en utilisant des textures de roche.

        :param fenetre: La fenêtre sur laquelle dessiner le bloc
        """
        # Dessine le bloc en plusieurs petites textures de roche (en fonction de la largeur et de la longueur)
        for i in range(0, self.largeur, taille_texture):  # Boucle sur la largeur du bloc
            for j in range(0, self.longueur, taille_texture):  # Boucle sur la longueur du bloc
                if j + taille_texture > self.longueur:  # Si la texture dépasse la fin du bloc
                    reste_a_parcourir = self.longueur - j  # Calcule combien il reste à dessiner sur la dernière ligne
                    texture_rognee = texture_roche.subsurface((0, 0, taille_texture, reste_a_parcourir))  # Récupère la partie restante de la texture
                    fenetre.blit(texture_rognee, (self.x + i, self.y + j))  # Dessine cette partie de la texture
                else:  # Si la texture peut être entièrement dessinée
                    fenetre.blit(texture_roche, (self.x + i, self.y + j))  # Dessine la texture entière
