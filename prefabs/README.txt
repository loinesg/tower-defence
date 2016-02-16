





This folder contains .prefab files used in the game.
.prefab files are used throughout the game to store values and load in textures etc.







Each row in the file consists of:
(blank lines and lines starting with # are ignored)

<variable name>  :  <variable type>  :  <value>








Classes inheriting from Prefab specify a .prefab file in their constructor. The file
is then loaded and variables added to the new class instance.







Variable types:
These are hard-coded into prefab.py (lines 110-128).

img: An image file
aimg: An image file with transparency (uses .convert_alpha())
font: A pygame.font.Font loaded by looking up its name
spritesheet: Looks up a set of textures matching the value name and stores them in a list
rotimg: Loads the specified texture and creates 365 / 5 copies in a list, for different rotations





Performance:
As well as making development of eg. multiple defence types faster, the loaded textures and other
objects are automatically cached by the prefab system, rather than loaded again for each new object
that inherits from Prefab.