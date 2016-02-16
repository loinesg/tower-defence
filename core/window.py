

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


class Window:
    """ 
    A wrapper class for the pygame window. 
    """

    def __init__(self, width, height):
        """ 
        Constructor. 
        
        Args:
            width (int): The window width, in pixels.
            height (int): The window height, in pixels.

        """
        self.resolution = (width, height)
        self.screen = pygame.display.set_mode(self.resolution)
        self.set_background(0, 0, 0)

    def set_title(self, title):
        """ 
        Sets the window title. 
        
        Args:
            title (str): The new title text.

        """
        pygame.display.set_caption(title)

    def set_background(self, r, g, b):
        """ 
        Sets the background colour 
        
        Args:
            r (float): The new r channel value.
            g (float): The new g channel value.
            b (float): The new b channel value.

        """
        self.background = pygame.Surface(self.resolution)
        self.background.fill(pygame.Color(r, g, b))
        self.background = self.background.convert()

    def clear(self):
        """ 
        Clears the window, using the background colour.
        """
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
