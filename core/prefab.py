

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
from pygame.rect import Rect
import pygame


class Prefab(Sprite):
    """ 
    A prefab object.
    Each prefab has a .prefab file containing variables loaded into the new prefab instance.   
    """

    # Used to cache config files { name, config }
    Cache = { }

    def __init__(self, name, x, y):
        """ 
        Constructor. 
        
        Args:
            name (str): The config file name.
            x (int): The top left x coordinate.
            y (int): The top left y coordinate.

        """
        super().__init__()

        self.name = name
        self.config = self.load_config(name)
        self.apply_config(self.config)

        # Handle animations
        if hasattr(self, "anim_source"):
            self.anim_change_time = self.anim_rate
            self.anim_index = 0
            self.image = self.anim_source[0]

        # Handle sprite images
        if hasattr(self, "image"):
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = Rect(x, y, 32, 32)

    def update_animation(self, delta):
        """
        Updates any spritesheet animation on the prefab.

        Args:
            delta (float): The time since last frame.

        """
        if hasattr(self, "anim_source"):
            self.anim_change_time -= delta

            if self.anim_change_time < 0:
                self.anim_change_time += self.anim_rate
                
                self.anim_index += 1
                if self.anim_index == len(self.anim_source):
                    self.anim_index = 0

                    if not hasattr(self, "anim_loop") or not self.anim_loop:
                        self.kill()

                self.image = self.anim_source[self.anim_index]


    def load_config(self, name):
        """ 
        Gets the config dictionary for the named prefab.

        Args:
            name (str): The name of the .prefab file to load.

        Returns:
            A name -> value dictionary of config variables.
       
        """
        # Try cached version first.
        if name in Prefab.Cache.keys():
            return Prefab.Cache[name]

        entries = { }

        try:
            with open("prefabs\\" + name + ".prefab", "r") as file:
                for line in [f.split(":") for f in file.readlines() if f[0] != "#" and len(f.strip()) != 0]:
                    key = line[0].strip()
                    type = line[1].strip()
                    value = line[2].strip()

                    if type == "str":
                        entries[key] = value
                    elif type == "int":
                        entries[key] = int(value)
                    elif type == "float":
                        entries[key] = float(value)
                    elif type == "bool":
                        entries[key] = (value == "1")
                    elif type == "img":
                        entries[key] = pygame.image.load(value).convert()
                    elif type == "aimg":
                        entries[key] = pygame.image.load(value).convert_alpha()
                    elif type == "font":
                        entries[key] = pygame.font.Font(pygame.font.match_font(value, "font_bold" in entries.keys()), entries["font_size"])
                    elif type == "spritesheet":
                        entries[key] = [pygame.image.load(value + str(i) + ".png").convert_alpha() for i in range(entries["anim_count"])]
                    elif type == "rotimg":
                        original = pygame.image.load(value).convert_alpha()
                        entries[key] = [original] + [pygame.transform.rotate(original, angle) for angle in range(5, 361, 5)]

        except OSError:
            print("Could not read prefab " + name)

        Prefab.Cache[name] = entries
        return entries

    def apply_config(self, config):
        """ 
        Applies all config settings to the prefab instance.
       
        Args:
            config (dict): A name:value list of variables to apply.

        """
        for name in config.keys():
            setattr(self, name, config[name])
