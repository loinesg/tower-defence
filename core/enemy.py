

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


from pygame.sprite import Sprite
from core.prefab import Prefab
import pygame
import math
import random


class Enemy(Prefab):
    """ 
    A spawned enemy in the game. AI controlled. 
    """

    def __init__(self, game, name, x, y):
        """ 
        Constructor. 
        
        Args:
            game (Game): The game instance.
            name (str): The name of the enemy type.
            x (int): The starting x position.
            y (int): The starting y position.
        
        """
        super().__init__(name, x, y)

        self.game = game
        self.path = game.level.pathfinding.get_path()
        self.target = self.path.start
        self.rect.topleft = self.target
        self.x = self.target[0]
        self.y = self.target[1]
        self.speed += random.randint(-25, 25)

        # Make the enemies tougher each round
        self.speed += random.randint(0, self.game.wave.number * 2)
        self.health = self.health ** (1 + (self.game.wave.number / 35))

    def update(self, delta):
        """ 
        Called once per frame. 
        
        Args:
            delta (float): The time since the last update().
        
        """
        self.update_position(delta)

    def update_position(self, delta):
        """
        Moves towards the current target.

        Args:
            delta (float): The time (in seconds) since the last Update().

        """
        current = self.rect.topleft
        target = self.target

        dx = target[0] - current[0]
        dy = target[1] - current[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        max = delta * self.speed

        # Snap to the target.
        if distance < max:
            self.x = target[0]
            self.y = target[1]
            self.reached_target()
        else:
            proportion = max / distance
            self.x += dx * proportion
            self.y += dy * proportion

        self.rect.x = self.x
        self.rect.y = self.y

    def reached_target(self):
        """
        Called when the enemy reaches their current target.

        Either changes target or kills the enemy.
        """
        if not self.path.done:

            # Check if the path was invalidated.
            if self.target[0] < self.game.window.resolution[0] and self.path.points is not None and self.target in self.path.points:
                self.path, self.target = self.game.level.pathfinding.get_partial_path(self.target)

            return

        self.target = self.path.next(self.target)
        if not self.target:
            self.game.level.lives -= 1
            if(self.game.level.lives == 0):
                self.game.menu.show_lose_screen()
                
            self.kill()

    def take_damage(self, damage):
        """ 
        Takes damage. The enemy will die if their health drops below 0.
        
        Args:
            damage (int): The amount of health to deduct.
        
        """
        self.health -= damage

        if self.health <= 0:
            self.kill()

    def kill(self):
        """
        Called when the enemy dies or escapes.
        """
        super().kill()

        self.game.wave.enemy_killed()  
        
        # True if the enemy died on the map
        # and did not escape.
        if self.rect.x > 1:       
            self.game.level.money += self.money
