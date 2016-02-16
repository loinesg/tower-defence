

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
import random

class Collision:
    """ 
    Handles collision detection on a grid of tiles.
    Used for turret placement, projectiles and navigation.
    """

    def __init__(self, level, resolution, tile_size):
        """ 
        Constructor. 
        
        Args:
            game (Game): The game instance.
            resolution (int, int): The screen resolution.
            tile_size (int): The size (pixels) of each cached tile.

        """
        self.level = level
        self.tile_size = tile_size
        self.width = resolution[0] // tile_size
        self.height = resolution[1] // tile_size
        self.blocked_tiles = []
        self.overlay = None

    def point_to_index(self, x, y):
        """
        Converts a point on the screen to a tile index.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Returns:
            (int): The index for the tile at (x, y).

        """
        xIndex = x // self.tile_size
        yIndex = y // self.tile_size

        return (yIndex * 1000) + xIndex

    def point_blocked(self, x, y):
        """
        Checks if the given point is blocked.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Returns:
            True if blocked, otherwise False.

        """
        return self.point_to_index(x, y) in self.blocked_tiles

    def block_point(self, x, y):
        """
        Makes the given point blocked.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        """
        index = self.point_to_index(x, y)

        if index not in self.blocked_tiles:
            self.blocked_tiles.append(index)
            self.overlay = None
            self.level.pathfinding.repair((x - (x % self.tile_size), y - (y % self.tile_size)))

    def unblock_point(self, x, y):
        """
        Makes the given point unblocked.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        """
        index = self.point_to_index(x, y)

        if index in self.blocked_tiles:
            self.blocked_tiles.remove(index)
            self.overlay = None


    def rect_blocked(self, x, y, width, height):
        """
        Checks if the given rect is blocked.

        Args:
            x (int): The top left x coordinate.
            y (int): The top left y coordinate.
            width (int): The width of the rect.
            height (int): The height of the rect.

        Returns:
            True if any part in the rect is blocked, otherwise False.

        """
        xOffset = x % self.tile_size
        yOffset = y % self.tile_size

        for xPos in range(x - xOffset, x + width, self.tile_size):
            for yPos in range(y - yOffset, y + height, self.tile_size):
                
                if self.point_blocked(xPos, yPos):
                    return True

        return False

    def block_rect(self, x, y, width, height):
        """
        Makes the given rect area blocked.

        Args:
            x (int): The top left x coordinate.
            y (int): The top left y coordinate.
            width (int): The width of the rect.
            height (int): The height of the rect.

        """
        xOffset = x % self.tile_size
        yOffset = y % self.tile_size

        for xPos in range(x - xOffset, x + width - 2, self.tile_size):
            for yPos in range(y - yOffset, y + height - 2, self.tile_size):
                self.block_point(xPos, yPos)

    def unblock_rect(self, x, y, width, height):
        """
        Makes the given rect area unblocked.

        Args:
            x (int): The top left x coordinate.
            y (int): The top left y coordinate.
            width (int): The width of the rect.
            height (int): The height of the rect.

        """
        xOffset = x % self.tile_size
        yOffset = y % self.tile_size

        for xPos in range(x - xOffset, x + width, self.tile_size):
            for yPos in range(y - yOffset, y + height, self.tile_size):
                
                self.unblock_point(xPos, yPos)
