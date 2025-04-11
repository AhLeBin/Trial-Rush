import pygame
import time

class Trial:
    def __init__(self, initial_y, texture):
        # Texture d'origine (non modifiée)
        self.texture_originale = texture

        # Texture actuelle affichée (peut être une version tournée)
        self.texture = texture.copy()

        # Position verticale initiale et actuelle
        self.y_initial = initial_y
        self.y = initial_y

        # État de l'animation ("montee", "immobile", "descente", ou "inactif")
        self.etat_animation = "inactif"

        # Temps de début de l'animation
        self.depart_anim = 0

        # Bloc ciblé par l'animation
        self.bloc_vise = None

        # Durées des différentes phases d'animation verticale
        self.duree_montee = 1.3
        self.duree_immobile = 1.1
        self.duree_descente = 0.6

        # État de la rotation (active ou non)
        self.en_rotation = False

        # Temps de début de la rotation
        self.debut_rotation = 0

        # Angle ciblé
        self.angle_rotation = 0

    def depart_animation(self, bloc_vise):
        """
        Lance l'animation verticale vers un bloc donné.
        """
        self.etat_animation = "montee"
        self.depart_anim = time.time()
        self.bloc_vise = bloc_vise

    def update(self):
        """
        Met à jour l'état (position et rotation) à chaque frame.
        """
        if self.etat_animation == "inactif":
            # Si aucune animation verticale en cours, on peut faire une rotation
            if self.en_rotation:
                temps_rotation = time.time() - self.debut_rotation

                if temps_rotation < 0.4:
                    # Rotation vers l'avant : de 0° à 20° sur 0.4s
                    progression = temps_rotation / 0.4
                    angle = 20 * progression
                    self.texture = self.rotate_around_bottom_left(self.texture_originale, angle)

                elif temps_rotation < 0.55:
                    # Rotation retour : de 20° à 0° sur 0.15s
                    progression = (temps_rotation - 0.4) / 0.15
                    angle = 20 * (1 - progression)
                    self.texture = self.rotate_around_bottom_left(self.texture_originale, angle)

                else:
                    # Fin de la rotation : on remet la texture d'origine
                    self.texture = self.texture_originale.copy()
                    self.en_rotation = False
            return  # On sort ici si la rotation était en cours

        # Calcul du temps écoulé depuis le début de l’animation
        temps_ecoule = time.time() - self.depart_anim

        # Position cible au-dessus du bloc visé
        y_vise = self.bloc_vise.y - self.texture.get_height()

        if self.etat_animation == "montee":
            if temps_ecoule < self.duree_montee:
                # Animation de montée (linéaire ou easing)
                progression = temps_ecoule / self.duree_montee
                self.y = self.y_initial + (y_vise - self.y_initial) * progression
            else:
                # Fin de la montée, on passe à l’état immobile
                self.y = y_vise
                self.etat_animation = "immobile"
                self.depart_anim = time.time()

        elif self.etat_animation == "immobile":
            if temps_ecoule < self.duree_immobile:
                # On reste immobile pendant un certain temps
                self.y = y_vise
            else:
                # Début de la descente
                self.etat_animation = "descente"
                self.depart_anim = time.time()

        elif self.etat_animation == "descente":
            if temps_ecoule < self.duree_descente:
                # Animation de descente (linéaire ou easing)
                progression = temps_ecoule / self.duree_descente
                self.y = y_vise + (self.y_initial - y_vise) * progression
            else:
                # Fin de l'animation, retour à l’état inactif
                self.y = self.y_initial
                self.etat_animation = "inactif"
                self.bloc_vise = None

    def dessine(self, screen, x):
        """
        Affiche le trial sur l'écran à la position (x, y).
        """
        screen.blit(self.texture, (x, self.y))

    def rotation(self):
        """
        Démarre l'animation de rotation.
        """
        self.en_rotation = True
        self.debut_rotation = time.time()

    def rotate_around_bottom_left(self, image, angle):
        """
        Fait tourner l'image autour de son coin inférieur gauche,
        en préservant la transparence (pas de fond noir).
        """
        # Taille et centre de l’image d’origine
        orig_rect = image.get_rect()

        # Pivot = coin inférieur gauche
        pivot = pygame.math.Vector2(0, orig_rect.height)

        # Calcul du décalage du pivot au centre
        offset_center_to_pivot = pivot - pygame.math.Vector2(orig_rect.center)

        # Applique la rotation à l’offset
        rotated_offset = offset_center_to_pivot.rotate(angle)

        # Rotation de l’image autour de son centre
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_rect = rotated_image.get_rect()

        # Nouveau centre basé sur le pivot
        new_center = pivot - rotated_offset

        # Surface vide avec transparence
        surface = pygame.Surface(rotated_rect.size, pygame.SRCALPHA)
        surface = surface.convert_alpha()

        # Position où blitter l’image tournée dans la surface
        blit_pos = new_center - pygame.math.Vector2(rotated_rect.width // 2, rotated_rect.height // 2)
        surface.blit(rotated_image, (-blit_pos.x, -blit_pos.y))

        return surface

    def crash(self, screen, x_depart, background, liste_blocs, manche=0, x_fond=0):
        """
        Animation de crash avec fond et blocs visibles.
        Le trialiste glisse vers la droite pendant que tout le décor reste affiché.
        Si c'est la première manche (manche=0), la distance est plus petite.
        """
        clock = pygame.time.Clock()

        # Détermine la distance de déplacement en fonction de la manche
        distance = 115 if manche == 0 else 146  # 115 pixels pour la première manche, 146 sinon
        step = 3 if manche == 0 else 5  # Pas plus petit pour la première manche

        for x in range(x_depart, x_depart + distance, step):
            # Affiche le fond avec la position actuelle
            screen.blit(background, (x_fond, 0))
            screen.blit(background, (x_fond + background.get_width(), 0))

            # Dessine tous les blocs
            for bloc in liste_blocs:
                bloc.dessine(screen)

            # Dessine le trialiste
            screen.blit(self.texture, (x, self.y))

            # Rafraîchit l'écran
            pygame.display.flip()
            clock.tick(60)

        # Après l'animation, basculer sur la texture crash
        self.texture = pygame.transform.scale(pygame.image.load('crash.png'), (100, 100))
        self.texture_originale = self.texture.copy()

        # Afficher une dernière fois avec la texture crash
        screen.blit(background, (x_fond, 0))
        screen.blit(background, (x_fond + background.get_width(), 0))
        for bloc in liste_blocs:
            bloc.dessine(screen)
        screen.blit(self.texture, (x_depart + distance, self.y))
        pygame.display.flip()