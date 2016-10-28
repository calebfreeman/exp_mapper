# exp_mapper
Python script for generating World of Exploration DOS game random maps.

How to use:

1. Download repository
2. Edit config.py, set save_dir to the path your Exploration saved games directory
2. Run "python generate_map.py"
3. Follow the prompts to choose a filename and set random map variables
4. A saved game will be created or overwrite an existing saved game depending on your filename input
5. If you have Exploration open and the file is a new saved game file (not overwriting an existing saved game) then you will need to unmount the C drive in DOSBox "MOUNT -u C:" then remount the drive. Otherwise the saved file will not appear.
6. Open Exploration and load the new saved game

Also included is a zip file (expcd) that can be installed on DOSBox using the following commands. Create a "dos" folder somewhere on you computer before starting DOSBox:

1. "MOUNT D /path/to/expcd"
2. "MOUNT C /path/to/dos"
3. "D:"
4. "INSTALL.EXE"
5. Follow the prompts to install
6. "C:"
7. "cd EXPLORE"
8. "exp.exe"
9. The intro screen for the game should appear, click to continue.

Todos

* Add multi-tile land tiles - mountains, deserts, tundra, and ice
* Add support for modulating the probability that tiles will appear, ice < grass
* Set homeports to spawn on appropriate coastal regions
* Set ships to spawn in homeports
* Support for setting beginning variables such as money, items, ships, starting settlements, etc.
* Command line prompt for variables
* Write to full saved file and write straight to hex code
* Optimize preformance and organize code
* End river with appropriate tile if nowhere to go
* Set indian and incan village variables

Why?

I started this because I loved this game as a kid and I am currently trying to learn hex code. Hacking the saved files created by this game seemed like a fun way to learn. Also while playing as a kid I hated the random maps that the game generated. The built-in random map generator simply shuffles a few pre-created continents around the board. The game would be a lot more interesting if landmass and other variables could be adjusted.

How it works:

1. The script starts by creating an 80x80 ocean. There are 4 ocean tiles with hex codes: 01, 02, 03, 04
2. It then chooses continent spawn points depending on how many you set and creates generic land tiles in those spawn points
3. From the continent spawn points the script randomly chooses tiles adjacent to existing land tiles to build continents
4. Continents build until the number of land tiles hits the set threshold
5. The script then iterates through each land tile
6. For each land tile all 8 adjacent tiles (up, down, and diagonal) are identified, each adjacent tile contributes a set of acceptable tiles based on the position of the adjacent tile in respect to the tile in question, an intersection of all acceptable adjacent tile sets is run, a tile is randomly chosen from the resulting set.
7. If no intersection can be found then a tile may not exist. The game doesn't account for certain coastal configurations. In this case the land tile is set to a sea tile. Setting tiles with unknown configurations to sea tiles allows for the normalization of coastal configurations, thus decreasing the number of coastal tile errors.
8. Run step 6 two more times to account for the fact that sea tiles may have been written after adjacent land tiles were chosen. 
9. Write to out.txt and exit
