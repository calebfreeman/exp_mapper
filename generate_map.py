import random
from itertools import *

land_tiles = []
land_tile_options = []

def get_rand_loc():
	loc = 1
	while not loc == '01':
		x_coord = random.randint(0,x_len-1)
		y_coord = random.randint(0,y_len-1)
		loc = new_map[y_coord][x_coord]
	return {'x':x_coord,'y':y_coord}

def shift(coord,i,shift):
	ret = None
	if shift == 'b' or shift == 'r':
		if coord == i:
			ret = 0
		else:
			ret = coord + 1
	if shift == 't' or shift == 'l':
		if coord == 0:
			ret = i
		else:
			ret = coord - 1
	return ret

def get_adjacent(x,y):
	ret = []
	for d in ['l','r']:
		new_x = shift(x,x_len-1,d)
		ret.append({'d':d,'x':new_x,'y':y,'i':str(new_x)+','+str(y)})

	for d in ['t','b']:
		new_y = shift(y,y_len-1,d)
		ret.append({'d':d,'y':new_y,'x':x,'i':str(x)+','+str(new_y)})
		for corner in ['l','r']:
			new_x = shift(x,x_len-1,corner)
			new_y = shift(y,y_len-1,d)
			ret.append({'d':d+corner,'x':new_x,'y':new_y,'i':str(new_x)+','+str(new_y)})

	return ret

def get_adjacent_no_diagonal(x,y):
	ret = []
	for d in ['l','r']:
		new_x = shift(x,x_len-1,d)
		ret.append({'d':d,'x':new_x,'y':y,'i':str(new_x)+','+str(y)})

	for d in ['t','b']:
		new_y = shift(y,y_len-1,d)
		ret.append({'d':d,'y':new_y,'x':x,'i':str(x)+','+str(new_y)})

	return ret

x_len = 80
y_len = 80
land_perc = .75
land_num_tiles = land_perc * x_len * y_len
continents = 20
rivers = 20

new_map = []


row = 0
for y in range(y_len):
	new_map.append([])
	col = 0
	for x in range(x_len):
		new_map[row].append('0' + str(random.randint(1,4)))
		col += 1
	row += 1
all_tiles = ['01','02','03','04','05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','19','1A','1B','1C','1D','1E','1F','20','21','22','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F','30','31','32','33','34','35','36','37','38','39','3A','3B','3C','3D','3E','3F','40','41','42','43','44','45','46','47','48','49','4A','4B','4C','4D','4E','4F','50','51','52','53','54','55','56','57','58','59','5A','5B','5C','5D','5E','5F','60','61','62','63','64','65','66','67','68','69','6A','6B','6C','6D','6E','6F','70','71','72','73','74']
sea_all = ['01','02','03','04']
land_all = []

opposing = {
	't':'b',
	'tr':'bl',
	'r':'l',
	'br':'tl',
	'b':'t',
	'bl':'tr',
	'l':'r',
	'tl':'br'
}

tiles = {
	'01':{'t':'S','r':'S','b':'S','l':'S','tr':'S','br':'S','tl':'S','bl':'S'},
	'02':{'t':'S','r':'S','b':'S','l':'S','tr':'S','br':'S','tl':'S','bl':'S'},
	'03':{'t':'S','r':'S','b':'S','l':'S','tr':'S','br':'S','tl':'S','bl':'S'},
	'04':{'t':'S','r':'S','b':'S','l':'S','tr':'S','br':'S','tl':'S','bl':'S'},
	'05':{'t':'L','r':'L','b':'S','l':'S','tr':'L','br':'?','tl':'?','bl':'?'},
	'06':{'t':'L','r':'S','b':'S','l':'L','tr':'?','br':'?','tl':'L','bl':'?'},
	'07':{'t':'S','r':'S','b':'L','l':'L','tr':'?','br':'?','tl':'?','bl':'L'},
	'08':{'t':'S','r':'L','b':'L','l':'S','tr':'?','br':'L','tl':'?','bl':'?'},
	'09':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'S','l':'L','tl':'L'},
	'0A':{'t':'L','tr':'L','r':'L','br':'S','b':'L','bl':'L','l':'L','tl':'L'},
	'0B':{'t':'L','tr':'S','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'0C':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'S'},
	'0D':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'?','l':'S','tl':'?'},
	'0E':{'t':'L','tr':'L','r':'L','br':'?','b':'S','bl':'?','l':'L','tl':'L'},
	'0F':{'t':'L','tr':'?','r':'S','br':'?','b':'L','bl':'L','l':'L','tl':'L'},
	'10':{'t':'S','tr':'?','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'?'},
	'11':{'t':'L','tr':'S','r':'L','br':'L','b':'L','bl':'S','l':'L','tl':'L'},
	'12':{'t':'L','tr':'L','r':'L','br':'S','b':'L','bl':'L','l':'L','tl':'S'},
	'13':{'t':'L','tr':'L','r':'L','br':'?','b':'S','bl':'?','l':'S','tl':'?'},
	'14':{'t':'L','tr':'?','r':'S','br':'?','b':'S','bl':'?','l':'L','tl':'L'},
	'15':{'t':'S','tr':'?','r':'S','br':'?','b':'L','bl':'L','l':'L','tl':'?'},
	'16':{'t':'S','tr':'?','r':'L','br':'L','b':'L','bl':'?','l':'S','tl':'?'},
	'17':{'t':'L','tr':'?','r':'S','br':'?','b':'L','bl':'L','l':'L','tl':'L'},
	'18':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'?','l':'S','tl':'?'},
	'19':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'1A':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'1B':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'1C':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'1D':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'1E':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'1F':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'20':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'21':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'22':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'23':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'24':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'25':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'26':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'27':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'28':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'29':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'2A':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'2B':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'2C':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'2D':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'2E':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'2F':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'30':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'31':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'32':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'33':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'34':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'35':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'36':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'37':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'38':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'39':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'3A':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'3B':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'3C':{'t':'R','tr':'L','r':'L','br':'L','b':'R','bl':'L','l':'L','tl':'L'},
	'3D':{'t':'R','tr':'L','r':'R','br':'L','b':'R','bl':'L','l':'L','tl':'L'},
	'3E':{'t':'L','tr':'L','r':'R','br':'L','b':'L','bl':'L','l':'R','tl':'L'},
	'3F':{'t':'L','tr':'L','r':'R','br':'L','b':'R','bl':'L','l':'L','tl':'L'},
	'40':{'t':'R','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'R','tl':'L'},
	'41':{'t':'R','tr':'L','r':'R','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'42':{'t':'L','tr':'L','r':'L','br':'L','b':'R','bl':'L','l':'R','tl':'L'},
	'43':{'t':'L','tr':'L','r':'L','br':'L','b':'R','bl':'L','l':'L','tl':'L'},
	'44':{'t':'L','tr':'L','r':'R','br':'L','b':'L','bl':'?','l':'S','tl':'?'},
	'45':{'t':'S','tr':'?','r':'L','br':'L','b':'R','bl':'L','l':'L','tl':'?'},
	'46':{'t':'R','tr':'L','r':'L','br':'?','b':'S','bl':'?','l':'L','tl':'L'},
	'47':{'t':'L','tr':'?','r':'S','br':'?','b':'L','bl':'L','l':'R','tl':'L'},
	'48':{'t':'L','tr':'L','r':'L','br':'L','b':'R','bl':'L','l':'L','tl':'L'},
	'49':{'t':'R','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'4A':{'t':'L','tr':'L','r':'R','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'4B':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'R','tl':'L'},
	'4C':{'t':'L','tr':'L','r':'P','br':'P','b':'P','bl':'L','l':'L','tl':'L'},
	'4D':{'t':'L','tr':'L','r':'P','br':'P','b':'P','bl':'P','l':'P','tl':'L'},
	'4E':{'t':'L','tr':'L','r':'L','br':'L','b':'P','bl':'P','l':'P','tl':'L'},
	'4F':{'t':'P','tr':'P','r':'P','br':'P','b':'P','bl':'L','l':'L','tl':'L'},
	'50':{'t':'P','tr':'P','r':'P','br':'P','b':'P','bl':'P','l':'P','tl':'P'},
	'51':{'t':'P','tr':'L','r':'L','br':'L','b':'P','bl':'P','l':'P','tl':'P'},
	'52':{'t':'P','tr':'P','r':'P','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'53':{'t':'P','tr':'P','r':'P','br':'L','b':'L','bl':'L','l':'P','tl':'P'},
	'54':{'t':'P','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'P','tl':'P'},
	'55':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'56':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'57':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'58':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'59':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'5A':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'5B':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'5C':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'5D':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'5E':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'5F':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'60':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'61':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'62':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'63':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'64':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'65':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'66':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'67':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'68':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'69':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'6A':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'6B':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'6C':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'6D':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'6E':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'6F':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'70':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'71':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'72':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'73':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'74':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
}

for key, value in tiles.iteritems():
	if not value['t'] == '':
		land_all.append(key)

tile_sets = {}

for tile in tiles:
	if not tiles[tile]['t'] == '':
		tile_sets[tile] = {'t':[],'r':[],'b':[],'l':[],'tr':[],'br':[],'tl':[],'bl':[]}
		for adjacent_tile in tiles:
			if not tiles[adjacent_tile]['t'] == '':
				for key, value in opposing.iteritems():				
					if tiles[tile][key] == tiles[adjacent_tile][value] or tiles[tile][key] == '?' or tiles[adjacent_tile][value] == '?':
						tile_sets[tile][key].append(adjacent_tile)

chosen_land_tiles = []

for i in range(continents):
	c = get_rand_loc()
	c['i'] = str(c['x'])+','+str(c['y'])
	chosen_land_tiles.append(c['i'])
	land_tile_options += get_adjacent_no_diagonal(c['x'],c['y'])
	land_tiles.append(c)
	new_map[c['y']][c['x']] = '19' #land_all[random.randint(0,len(land_all)-1)]


cid = c['i']

while len(land_tiles) < land_num_tiles:
	while cid in chosen_land_tiles:
		idx = random.randint(0,len(land_tile_options)-1)
		c = land_tile_options[idx]
		cid = land_tile_options[idx]['i']
	del land_tile_options[idx]
	chosen_land_tiles.append(cid)
	new_map[c['y']][c['x']] = '19' #land_all[random.randint(0,len(land_all)-1)]
	land_tiles.append(c)
	for opt in get_adjacent_no_diagonal(c['x'],c['y']):
		if opt not in land_tiles:
			land_tile_options.append(opt)

for l_tile in land_tiles:
	sets = []
	#print l_tile
	for adj in get_adjacent(l_tile['x'],l_tile['y']):
		sets.append(set(tile_sets[new_map[adj['y']][adj['x']]][opposing[adj['d']]])) 
	intersect = set(all_tiles).intersection(*sets)
	if len(intersect) > 0:
		new_map[l_tile['y']][l_tile['x']] = list(intersect)[random.randint(0,len(intersect)-1)]
	else:
		new_map[l_tile['y']][l_tile['x']] = '0' + str(random.randint(1,4))

for l_tile in land_tiles:
	sets = []
	#print l_tile
	for adj in get_adjacent(l_tile['x'],l_tile['y']):
		sets.append(set(tile_sets[new_map[adj['y']][adj['x']]][opposing[adj['d']]])) 
	intersect = set(all_tiles).intersection(*sets)
	if len(intersect) > 0:
		new_map[l_tile['y']][l_tile['x']] = list(intersect)[random.randint(0,len(intersect)-1)]
	else:
		new_map[l_tile['y']][l_tile['x']] = '0' + str(random.randint(1,4))

river_spawn_points = []

for l_tile in land_tiles:
	sets = []
	#print l_tile
	for adj in get_adjacent(l_tile['x'],l_tile['y']):
		sets.append(set(tile_sets[new_map[adj['y']][adj['x']]][opposing[adj['d']]])) 
	intersect = set(all_tiles).intersection(*sets)
	if len(intersect) > 0:
		t = list(intersect)[random.randint(0,len(intersect)-1)]
		new_map[l_tile['y']][l_tile['x']] = t
		if t == '10':
			river_spawn_points.append(l_tile)

#print river_spawn_points
#print len(river_spawn_points)

# Homeport spawn


f = open("out.txt", "w")
f.seek(0)
for map_row in new_map:
	for map_col in map_row:
		f.write(map_col)
f.truncate()
f.close()

