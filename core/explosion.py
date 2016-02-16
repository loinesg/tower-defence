

###########################################
#
# COMP 1551
# Core Programming
#
# Coursework 2 - Mini Project
#
# George Loines
# 200836065
#
# 02 Feb 2015
#
###########################################


import math
import random
import pygame
from core.prefab import Prefab


class Explosion(Prefab):
    """
    Represents an explosion in the level.
    Contains an animated graphic.
    """

    def  __init__(self, game, position, radius, damage):
       """
       Constructor.

       Args:
            game (Game): The game instance.
            position (int, int): The coordinates of the explosion.
            radius (float): The damage radius of the explosion.
            damage (float): The damage at the centre of the explosion.

       """
       super().__init__("attack_explosion", position[0], position[1])
       self.rect.center = position

       max_magnitude = radius ** 2

       for enemy in game.wave.enemies:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            magnitude = (dx ** 2) + (dy ** 2)

            if magnitude < max_magnitude:
                enemy.take_damage(damage * (1 - (magnitude / max_magnitude)))

    def update(self, delta):
        """
        Called each frame the explosion is active.
        Updates the graphics.

        Args:
            delta (float): The time since the last update.

        """
        super().update_animation(delta)
