# exp_mapper
Python script for generating World of Exploration DOS game random maps

1. Set the number of continents you want using the variable "continents". This sets the number of land spawn seeds.
2. Set the percentage of landmass you want using the variable "land_perc". This limits the number of land tiles created.
3. Run the script using "python generate_map.py".
4. In the same folder as the script an "out.txt" file containing hexidemical code will be created.
5. Copy the entire contents of out.txt.
6. Open your favorite hex code editor and open a saved game.
7. Overwrite the first 64000 bytes with the copied contents of out.txt. Adding any bytes to the file could corrupt the file.

Todos

1. Fix coastal tiles, corners are not rendering correctly
2. Add support for remaining land tiles - mountains, deserts, tundra, and ice
3. Set indian villages and incan cities to spawn on land
4. Set homeports to spawn on appropriate coastal regions
5. Set ships to spawn in homeports
5. Support for setting beginning variables such as money, items, ships, starting settlements, etc.
6. Support for beginning percentage of map discovered by all players - currently setting the map discovery region to hex code 1F for all bytes reveals the entire world to all players
7. Command line prompt for all continents and land mass
8. Write to full saved file and write straight to hex code
