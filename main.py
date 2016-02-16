

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
from core.game import Game
from core.window import Window

# Init pygame
pygame.init()

# Create a window
window = Window(1280, 768)
window.set_title("Tower Defence")
window.set_background(148, 168, 176)

# Create the game instance
game = Game(window)
game.run()

# Quit pygame
pygame.quit()
