*Work in Progress!*

# exp_mapper
Python script for generating World of Exploration DOS game random maps.

1. Set the number of continents you want using the variable "continents". This sets the number of land spawn seeds.
2. Set the percentage of landmass you want using the variable "land_perc". This limits the number of land tiles created.
3. Run the script using "python generate_map.py".
4. In the same folder as the script an "out.txt" file containing hexidemical code will be created.
5. Copy the entire contents of out.txt.
6. Open your favorite hex code editor and open a saved game.
7. Overwrite the first 64000 bytes with the copied contents of out.txt. Adding any bytes to the file could corrupt the file.

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

1. Fix coastal tiles, corners are not rendering correctly
2. Add support for remaining land tiles - mountains, deserts, tundra, and ice
3. Add support for modulating the probability that tiles will appear, ice < grass
4. Set indian villages and incan cities to spawn on land
5. Set homeports to spawn on appropriate coastal regions
6. Set ships to spawn in homeports
7. Support for setting beginning variables such as money, items, ships, starting settlements, etc.
8. Support for beginning percentage of map discovered by all players - currently setting the map discovery region to hex code 1F for all bytes reveals the entire world to all players
9. Command line prompt for all continents and land mass
10. Write to full saved file and write straight to hex code

Why?

I started this because I loved this game as a kid and I am currently trying to learn hex code. Hacking the saved files created by this game seemed like a fun way to learn. Also while playing as a kid I hated the random maps that the game generated. The built-in random map generator simply shuffles a few pre-created continents around the board. The game would be a lot more interesting if landmass and other variables could be adjusted.

How it works:

1. The script starts by creatuing an 80x80 ocean. There are 4 ocean tiles with hex codes: 01, 02, 03, 04
2. It then chooses continent spawn points depending on how many you set and creates generic land tiles in those spawn points
3. From the continent spawn points the script randomly chooses tiles adjacent to existing land tiles to build continents
4. Continents build until the number of land tiles hits the set threshold
5. Iterate through each land tile
6. For each land tile look at all adjacent tiles, figure out what the tile in question should be by doing an intersection of what the adjacent tiles require (sea, land, etc.), randomly choose a tile from the intersection
7. If no intersection can be found then a tile may not exist (game didn't account for such a land/sea configuration in their tileset), set the tile to a sea tile. This normalizes the landmasses so that each tile can be appropriately accounted for.
8. Run step 6 again to account for the fact that sea tiles may have been written after land tiles were chosen. 
9. Write to out.txt and exit
