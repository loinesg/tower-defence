

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


from core.prefab import Prefab
from core.collision import Collision
from core.wave import Wave
from core.pathfinding import Pathfinding
from pygame.sprite import OrderedUpdates


class Level:
    """
    Represents a level loaded from a text based .level file.

    Contains level prefabs, cached paths and collision data.
    """

    def __init__(self, game, name):
        """ 
        Constructor. 
        
        Args:
            game (Game): The game instance.
            name (str): The name of the level being loaded (case sensitive).

        """
        self.game = game
        self.name = name
        self.load_data()
        self.start()

    def load_data(self):
        """ 
        Loads the level by its name. 

        Level data is saved in a text based .level file, containing prefab types 
        and their corresponding positions. This data is used by Level.restart()
        to position level components.

        Returns:
            list[list[string]]: A list of data entries for the level.

        """
        try:
            with open("levels\\" + self.name + ".level", "r") as file:
                self.data = [line.strip().split(" ") for line in file.readlines() if len(line.strip()) > 0 and line[0] != "#"]

        except IOError:
            print("Error loading level")

    def start(self):
        """ 
        Sets up and starts the level.
        """
        self.collision = Collision(self, self.game.window.resolution, 32)
        self.prefabs = OrderedUpdates()
        self.pathfinding = Pathfinding(self.game, self.collision)

        for args in self.data:
            name = args[0]
            x = int(args[1])
            y = int(args[2])

            prefab = Prefab(name, x, y)
            self.prefabs.add(prefab)

            if hasattr(prefab, "block"):
                # Block textures are 1 pixel wider to make a full border
                self.collision.block_rect(x, y, prefab.rect.width - 1, prefab.rect.height - 1)

        self.pathfinding.precompute(30)
        self.wave = Wave(self.game, 1)
        self.lives = 20
        self.money = 600
        self.time = 0

    def get_score(self):
        return int((self.time / 5) ** 1.4 + (self.game.wave.number - 1) ** 3)
