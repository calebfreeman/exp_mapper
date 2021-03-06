# Exploration Random Map Generator
Python script for generating and previewing World of Exploration DOS game random maps on MacOSX.

Screenshots of random map previews and their in-game experience:

Mix of ocean and land (60% land, 100 continent spawn points):

![map preview](https://raw.githubusercontent.com/calebfreeman/exp_mapper/master/screenshots/map_preview.png)
![map preview in exploration](https://raw.githubusercontent.com/calebfreeman/exp_mapper/master/screenshots/map_preview_exp.png)

Small central ocean, large landmass (95% land, 5 continent spawn points):

![map preview](https://raw.githubusercontent.com/calebfreeman/exp_mapper/master/screenshots/small_ocean_preview.png)
![map preview in exploration](https://raw.githubusercontent.com/calebfreeman/exp_mapper/master/screenshots/small_ocean_game.png)

Big ocean, tiny islands (20% land, 1000 continent spawn points):

![map preview](https://raw.githubusercontent.com/calebfreeman/exp_mapper/master/screenshots/islands_preview.png)
![map preview in exploration](https://raw.githubusercontent.com/calebfreeman/exp_mapper/master/screenshots/small_islands_game.png)


How to use this repository:

1. Download repository
2. Edit config.py, set save_dir to the path your Exploration saved games directory
2. Run "python generate_map.py"
3. Follow the prompts to choose a filename and set random map variables:

![settings](https://raw.githubusercontent.com/calebfreeman/exp_mapper/master/screenshots/settings.png)


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

* Set initial doubloons
* Set computer/human players
* Create ice spawn points & function to set ice coastlines
* Support for setting beginning variables such as money, items, ships, starting settlements, etc.
* Optimize preformance and organize code
* Prompt with list of preset options - small islands, large islands, single continent, etc
* More consistent support for Windows
* Python3 support

How it works:

1. The script starts by creating an 80x80 ocean. There are 4 ocean tiles with hex codes: 01, 02, 03, 04.
2. It then chooses continent spawn points depending on how many you set and creates generic land tiles in those spawn points. The more spawn points the more scattered the landmass. The less spawn points the more consolidated the landmass. Values between 1 and 1000 are recommended.
3. From the continent spawn points the script randomly chooses tiles adjacent to existing land tiles to build continents, this uses a virtual universal land tile: FF. It's a virtual tile because it does not exist in the game. It shows up as a black spot, but it's set in the script to act as a universal land tile that accepts any other type of land type: rivers, mountains, etc.
4. Continents build until the number of land tiles hits the set threshold using univeral virtual land tiles.
5. The script then iterates through each land tile to set coastlines. If a coastline configuration cannot be tiled then that tile is set to ocean. This process is run until it reaches an inaccuracy threshold of 2 tiles or less out of 6400. A threshold of 2 or less is set because in rare cases there are configurations that are too expensive to correct causing the script to hang. On the last run inland tiles are added to a seperate list.
6. For each inland tile all 8 adjacent tiles (up, down, left, right, and diagonals) are identified, each adjacent tile contributes a set of acceptable tiles based on the position of the adjacent tile in respect to the tile in question, an intersection of all acceptable adjacent tile sets is run, a tile is randomly chosen from the resulting set.
7. If no intersection can be found then the tile is set to a generic land tile - not mountains, rivers, prairie, or desert. Doing so allows the algorithm to iterate to a solution within about 5 iterations with only 0-2 inaccuracies out of 6400 tiles. Other options were explored such as using the universal land tile and randomly selecting inland tiles. Using those options the algorithm would iterate infinitely without ever finding an accurate solution.
8. Random map data is written to a saved game file in the directory defined within config.py using the user defined filename.

Why?

* I loved playing this game when I was a kid
* I hated how the built-in random map generator simply shuffled a few pre-made continents around an ocean, it wasn't a truly random map.
* I wanted to really learn hexadecimal code and hacking the .SAV file in this game was a great way to learn.
* Playing this game using a truly random map is a lot of fun.
