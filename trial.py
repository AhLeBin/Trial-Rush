import pygame
import time

class Trial:
    def __init__(self, initial_y, texture):
        """
        Constructeur de la classe Trial.
        
        :param initial_y: Position verticale initiale du trialiste (en pixels).
        :param texture: Texture à afficher pour ce trialiste
        """
        self.texture = texture  # Texture du trialiste
        self.y_initial = initial_y  # Position Y initiale du trialiste
        self.y = initial_y  # Position Y actuelle du trialiste (initialisée à la même valeur que y_initial)

        # État de l'animation
        self.etat_animation = "inactif"  # L'animation commence dans un état inactif (pas de mouvement)
        self.depart_anim = 0  # Temps de départ de l'animation (temps auquel l'animation a commencé)
        self.bloc_vise = None  # Bloc que le trialiste vise

        # Durées des différentes phases de l'animation
        self.duree_montee = 1.3  # Durée de la phase de montée (en secondes)
        self.duree_immobile = 1.1  # Durée de la phase où l'objet reste immobile
        self.duree_descente = 0.6  # Durée de la phase de descente (en secondes)

    def depart_animation(self, bloc_vise):
        """
        Démarre l'animation en visant un bloc spécifique.
        
        :param bloc_vise: Le bloc que l'animation doit atteindre.
        """
        self.etat_animation = "montee"  # L'animation commence par la montée
        self.depart_anim = time.time()  # Enregistre le moment où l'animation commence
        self.bloc_vise = bloc_vise  # Le bloc visé est défini ici

    def update(self):
        """
        Met à jour l'état de l'animation en fonction du temps écoulé et de l'état actuel.
        """
        if self.etat_animation == "inactif" or not self.bloc_vise:
            # Si l'animation est inactive ou si aucun bloc n'est visé, on ne fait rien
            return

        temps_ecoule = time.time() - self.depart_anim  # Calcule le temps écoulé depuis le début de l'animation
        y_vise = self.bloc_vise.y - self.texture.get_height()  # Position Y du bloc visé moins la hauteur du trialiste pour aligner roue arriere

        # Si l'animation est en phase de montée
        if self.etat_animation == "montee":
            if temps_ecoule < self.duree_montee:
                progression = temps_ecoule / self.duree_montee  # Progression de l'animation de montée
                self.y = self.y_initial + (y_vise - self.y_initial) * progression  # Calcule la nouvelle position Y pendant la montée
            else:
                self.y = y_vise  # L'animation atteint la position cible
                self.etat_animation = "immobile"  # L'animation passe à l'état immobile
                self.depart_anim = time.time()  # Redémarre le chronomètre pour la phase immobile

        # Si l'animation est en phase immobile
        elif self.etat_animation == "immobile":
            if temps_ecoule < self.duree_immobile:
                self.y = y_vise  # L'objet reste immobile à la position visée
            else:
                self.etat_animation = "descente"  # L'animation passe à la descente
                self.depart_anim = time.time()  # Redémarre le chronomètre pour la phase de descente

        # Si l'animation est en phase de descente
        elif self.etat_animation == "descente":
            if temps_ecoule < self.duree_descente:
                progression = temps_ecoule / self.duree_descente  # Progression de l'animation de descente
                self.y = y_vise + (self.y_initial - y_vise) * progression  # Calcule la nouvelle position Y pendant la descente
            else:
                self.y = self.y_initial  # L'animation termine la descente et revient à la position initiale
                self.etat_animation = "inactif"  # L'animation est maintenant inactive
                self.bloc_vise = None  # Aucun bloc n'est visé, l'animation est terminée

    def dessine(self, screen, x):
        """
        Dessine l'objet sur l'écran à la position spécifiée.
        
        :param screen: L'écran (surface pygame) sur lequel dessiner l'objet.
        :param x: Position horizontale (X) où l'objet doit être dessiné.
        """
        screen.blit(self.texture, (x, self.y))  # Affiche la texture à la position (x, y)
