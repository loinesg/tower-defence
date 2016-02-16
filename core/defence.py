

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


import pygame
import math
from pygame import Rect
from core.prefab import Prefab
from core.bullet import Bullet
from core.explosion import Explosion


class Defence(Prefab):
    """
    A base class for user-placed turrets.
    """
    
    def __init__(self, game, name, x, y):
        """
        Constructor.

        Args:
            game (Game): The game instance.
            name (str): The name of the type of turret.
            x (int): The x coordinate.
            y (int): The y coordinate.

        """
        super().__init__(name, x, y)

        self.game = game
        self.fire_time = 0
        self.target = None

        if hasattr(self, "images"):
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        if hasattr(self, "block"):
            self.game.level.collision.block_rect(x, y, self.rect.width, self.rect.height)

    def update(self, delta):
        """
        Called once each frame.
        Updates targeting and launches attacks.

        Args:
            delta (float): The time (seconds) since the last update.

        """
        # Defences such as walls have no attack,
        if self.attack == "none":
            return

        target = self.get_target()

        self.fire_time += delta
        while self.fire_time >= self.attack_rate:
            self.fire_time -= self.attack_rate
        
            if target is not None and target != self.rect.center: # Prevents divide by 0 errors when positions are the same.
            
                # Spawn the attack.
                if self.attack == "bullet":
                    self.game.bullets.add(Bullet(self.game, self.rect.center, target))
                elif self.attack == "explosion":
                    self.game.explosions.add(Explosion(self.game, target, self.explosion_radius, self.explosion_damage))

                # Create the flash (if specified).
                if hasattr(self, "flash_offset"):
                    self.game.explosions.add(DefenceFlash(self.rect.center, target, self.flash_offset))

                # Used for one-time defences e.g. mines.
                if self.attack_rate <= 0:
                    self.kill()

            if self.attack_rate <= 0:
                break

        # Rotate the defence to face its target.
        if self.rotate:
            center = self.rect.center

            if self.target is None:
                self.image = self.images[0]
            else:
                dx = self.target.rect.center[0] - center[0]
                dy = self.target.rect.center[1] - center[1]
                angle = math.degrees(math.atan2(-dy, dx))
                if angle < 0:
                    angle += 360

                self.image = self.images[int(angle // 5)]

            self.rect = self.image.get_rect()
            self.rect.center = center

    def get_target(self):
        """
        Attempts to find a suitable target.

        Returns:
            (int, int) The position of the target, if found.
            Otherwise returns None.

        """
        if self.target is not None and self.is_target_suitable(self.target):
            return self.target.rect.center

        for t in self.game.wave.enemies:
            if self.is_target_suitable(t):
                self.target = t
                return t.rect.center

        return None

    def is_target_suitable(self, target):
        """
        Calculates if a target can be shot at.

        Args:
            target (Enemy): The target being tried.

        Returns 
            True if the target can be hit, otherwise false.

        """
        if target not in self.game.wave.enemies:
            return False

        a = target.rect.center
        b = self.rect.center
        sqrdist = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

        return sqrdist <= self.attack_range ** 2


class DefenceFlash(Prefab):
    """
    A flash effect displayed when some defences attack.
    """

    def __init__(self, defence_position, target, offset):
        """
        Constructor.
        
        Args:
            defence_position (int, int): The centre of the defence.
            target (int, int): The centre of the target.
            offset (float): The distance from the defence_position to the flash.

        """
        dx = target[0] - defence_position[0]
        dy = target[1] - defence_position[1]
        magnitude = math.sqrt(dx * dx + dy * dy)
        dx *= (offset / magnitude)
        dy *= (offset / magnitude)

        super().__init__("defence_flash", defence_position[0] + dx - 16, defence_position[1] + dy - 16)

    def update(self, delta):
        """
        Called each frame. Updates the graphic.

        Args:
            delta (float): The time since the last update.

        """
        super().update_animation(delta)
