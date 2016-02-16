

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


import random
import pygame
from core.level import Level
from core.collision import Collision
from core.defence import Defence
from core.enemy import Enemy
from core.wave import Wave
from core.menu import Menu
from core.prefab import Prefab


class Game:
    """ 
    Contains the main control code and the game loop.
    """

    def __init__(self, window):
        """ 
        Constructor. 
        
        Args:
            window (Window): The window instance to render to.

        """
        self.window = window
        self.clock = pygame.time.Clock()
        self.defences = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.load_level("path")
        self.defence_type = 0
        self.defence_prototypes = [Defence(self, "defence_" + name, -100, -100) for name in ["pillbox", "wall", "mines", "artillery"]]

    def load_level(self, name):
        """
        Loads a new level.

        Args:
            name (str): The name of the level (case sensitive).

        """
        self.defences.empty()
        self.bullets.empty()
        self.explosions.empty()
        self.level = Level(self, name)
        self.wave = Wave(self, 1)
        self.menu = Menu(self)

    def run(self):
        """ 
        Runs the main game loop. 
        """
        self.running = True

        while self.running:
            delta = self.clock.tick(60) / 1000.0

            # Look for a quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.menu.visible:
                        self.place_defence(pygame.mouse.get_pos())
                    self.menu.clicked()
                elif event.type == pygame.KEYDOWN:
                    self.menu.key_pressed(event.key)

            # Call update functions
            self.menu.update()
            self.level.pathfinding.update()

            if not self.menu.visible:
                self.level.time += delta
                self.defences.update(delta)
                self.bullets.update(delta)
                self.explosions.update(delta)

                self.wave.update(delta)
                if self.wave.done:
                    self.wave = Wave(self, self.wave.number + 1)

            # Redraw graphics
            self.window.clear()
            self.level.prefabs.draw(self.window.screen)
            self.defences.draw(self.window.screen)
            self.bullets.draw(self.window.screen)
            self.wave.enemies.draw(self.window.screen)
            self.explosions.draw(self.window.screen)
            self.menu.draw(self.window.screen)

    def quit(self):
        """
        Quits and closes the game.
        """
        self.running = False

    def select_defence(self, type):
        """
        Picks a defence type for placement.

        Args:
            type (int): The index of the selcted defence type.

        """
        self.defence_type = type

    def place_defence(self, position):
        """
        Attempts to place a defence at the given position.

        Args:
            position (int, int): The intended coordinates of the defence.

        """
        if self.defence_type < 0:
            return

        defence = self.defence_prototypes[self.defence_type]

        if self.level.money < defence.cost:
            return

        x = position[0] - position[0] % 32
        y = position[1] - position[1] % 32

        # Stop if the defence would intersect with the level.
        if self.level.collision.rect_blocked(x, y, defence.rect.width - 2, defence.rect.height - 2):
            return

        # Stop if the defence may lead no path for enemies.
        if hasattr(defence, "block") and self.level.pathfinding.is_critical((x, y)):
            return

        self.defences.add(Defence(self, defence.name, x, y))
        self.level.money -= defence.cost
