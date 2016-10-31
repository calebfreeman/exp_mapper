import random
from itertools import *
import binascii
import sys
from config import save_dir, cities


# Initial variables
testing = False

filepath = save_dir + str(raw_input("Path & filename for saved game ('RANDOM'): ") or "RANDOM")
reveal_map = str(raw_input('Reveal map for all players? (Yn):') or 'Y')
reveal = False
if reveal_map == 'Y' or reveal_map =='Yes' or reveal_map == 'yes' or reveal_map == 'y':
	reveal = True
x_len = 80
y_len = 80
land_perc = float(raw_input('Land percentage (60): ') or 60)/100
land_num_tiles = land_perc * x_len * y_len
continents = int(raw_input('Continent Seeds (50): ') or 50)
rivers = int(raw_input('River Seeds (30): ') or 30)
river_length = 2
new_map = []
reset_coastline_num = 4
land_tiles = []
inland_regions = []
land_tile_options = []
chosen_land_tiles = []
river_spawn_points = []
river_ext_pts = []
all_tiles = ['01','02','03','04','05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','19','1A','1B','1C','1D','1E','1F','20','21','22','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F','30','31','32','33','34','35','36','37','38','39','3A','3B','3C','3D','3E','3F','40','41','42','43','44','45','46','47','48','49','4A','4B','4C','4D','4E','4F','50','51','52','53','54','55','56','57','58','59','5A','5B','5C','5D','5E','5F','60','61','62','63','64','65','66','67','68','69','6A','6B','6C','6D','6E','6F','70','71','72','73','74']
sea_all = ['01','02','03','04']
features = ['19','1A','1B','1C','1D','1E','1F','22','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F','30','31','32','33','34','35','36','37','38','39','3A','3B','3C','3D','3E','3F','40','41','42','43','48','49','4A','4B','4C','4D','4E','4F','50','51','52','53','54','55','56','57','58','59','5A','5B','5C','5D','5E']
ls = ['19','1A','1B','1C','1D','1E','1F']

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

river_spawn_tiles = {
	'0D': '44', #sea on left
	'0E' : '46', #sea on bottom
	'0F' : '47', #sea on right
	'10' : '45', #sea on top
	'1B' : '43',
	'1C' : '48',
	'1D' : '49',
	'1E' : '4A',
	'1F' : '4B',
	'17' : '47'
	
}

homeport_tiles = {
	'0D': '10', #sea on left
	'0E' : '0A', #sea on bottom
	'0F' : '0B', #sea on right
	'10' : '0C', #sea on top
}

coastal_tiles = ['01','02','03','04','05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','44','45','46','47']
inland_tiles = ['19','1A','1B','1C','1D','1E','1F','26','27','28','29','2A','2F','30','3B']
river_tiles = ['3D','3C','3E','3F','40','41','43','48','49','4A','4B'] 

for each in range(river_length):
	river_tiles = ['3C','3E','3F','40','41'] + river_tiles

#river_tiles = ['3C','3E','3F','40','41','43','48','49','4A','4B'] # Even probability, 42 & 3D removed

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
	'22':{'t':'L','tr':'L','r':'H','br':'H','b':'H','bl':'L','l':'L','tl':'L'},
	'23':{'t':'L','tr':'L','r':'L','br':'L','b':'H','bl':'H','l':'H','tl':'L'},
	'24':{'t':'H','tr':'H','r':'H','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'25':{'t':'H','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'H','tl':'H'},
	'26':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'27':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'28':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'29':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'2A':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'2B':{'t':'L','tr':'L','r':'M','br':'M','b':'M','bl':'L','l':'L','tl':'L'},
	'2C':{'t':'L','tr':'L','r':'L','br':'L','b':'M','bl':'M','l':'M','tl':'L'},
	'2D':{'t':'M','tr':'M','r':'M','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'2E':{'t':'M','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'M','tl':'M'},
	'2F':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'30':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'31':{'t':'F','tr':'F','r':'F','br':'F','b':'F','bl':'L','l':'L','tl':'L'},
	'32':{'t':'F','tr':'F','r':'F','br':'F','b':'F','bl':'F','l':'F','tl':'F'},
	'33':{'t':'F','tr':'L','r':'L','br':'L','b':'F','bl':'F','l':'F','tl':'F'},
	'34':{'t':'L','tr':'L','r':'L','br':'L','b':'F','bl':'F','l':'F','tl':'L'},
	'35':{'t':'L','tr':'L','r':'F','br':'F','b':'F','bl':'L','l':'L','tl':'L'},
	'36':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'37':{'t':'L','tr':'L','r':'F','br':'F','b':'F','bl':'F','l':'F','tl':'L'},
	'38':{'t':'F','tr':'F','r':'F','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'39':{'t':'F','tr':'F','r':'F','br':'L','b':'L','bl':'L','l':'F','tl':'F'},
	'3A':{'t':'F','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'F','tl':'F'},
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
	'55':{'t':'L','tr':'L','r':'D','br':'D','b':'D','bl':'L','l':'L','tl':'L'},
	'56':{'t':'L','tr':'L','r':'D','br':'D','b':'D','bl':'D','l':'D','tl':'L'},
	'57':{'t':'L','tr':'L','r':'L','br':'L','b':'D','bl':'D','l':'D','tl':'L'},
	'58':{'t':'D','tr':'D','r':'D','br':'D','b':'D','bl':'L','l':'L','tl':'L'},
	'59':{'t':'D','tr':'D','r':'D','br':'D','b':'D','bl':'D','l':'D','tl':'D'},
	'5A':{'t':'D','tr':'D','r':'D','br':'D','b':'D','bl':'D','l':'D','tl':'D'},
	'5B':{'t':'D','tr':'L','r':'L','br':'L','b':'D','bl':'D','l':'D','tl':'D'},
	'5C':{'t':'D','tr':'D','r':'D','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'5D':{'t':'D','tr':'D','r':'D','br':'L','b':'L','bl':'L','l':'D','tl':'D'},
	'5E':{'t':'D','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'D','tl':'D'},
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
	'FF':{'t':'LHRMFPD','tr':'LHRMFPD','r':'LHRMFPD','br':'LHRMFPD','b':'LHRMFPD','bl':'LHRMFPD','l':'LHRMFPD','tl':'LHRMFPD'},
}

# Dynamically set tile_sets, can be replaced with static variable or separated from code
tile_sets = {}

for tile in tiles:
	if not tiles[tile]['t'] == '':
		tile_sets[tile] = {'t':[],'r':[],'b':[],'l':[],'tr':[],'br':[],'tl':[],'bl':[]}
		for adjacent_tile in tiles:
			if not tiles[adjacent_tile]['t'] == '':
				for key, value in opposing.iteritems():				
					for left in tiles[tile][key]:
						for right in tiles[adjacent_tile][value]:
							if left == right or tiles[tile][key] == '?' or tiles[adjacent_tile][value] == '?':
								tile_sets[tile][key].append(adjacent_tile)

# Dynamically set land_all, can be replaced with static variable once all tiles are set or separated from code
land_all = []

for key, value in tiles.iteritems():
	if not value['t'] == '':
		land_all.append(key)


# Find random continent seed location on map that has not already been written

def get_rand_unique_loc():
	loc = 'FF'
	while loc == 'FF':
		x_coord = random.randint(0,x_len-1)
		y_coord = random.randint(0,y_len-1)
		loc = new_map[y_coord][x_coord]
	return {'x':x_coord,'y':y_coord}

# Given coordinate on single axis, axis_length, and direction to shift, return new coordinate
def shift(coord,axis_length,direction):
	ret = None
	if direction == 'b' or direction == 'r':
		if coord == axis_length:
			ret = 0
		else:
			ret = coord + 1
	if direction == 't' or direction == 'l':
		if coord == 0:
			ret = axis_length
		else:
			ret = coord - 1
	return ret

# Given a coordinate, return 8 adjacent coordinates
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

# Given a coordinate, return 4 adjacent coordinates excluding diagonals
def get_adjacent_no_diagonal(x,y):
	ret = []
	for d in ['l','r']:
		new_x = shift(x,x_len-1,d)
		ret.append({'d':d,'x':new_x,'y':y,'i':str(new_x)+','+str(y)})

	for d in ['t','b']:
		new_y = shift(y,y_len-1,d)
		ret.append({'d':d,'y':new_y,'x':x,'i':str(x)+','+str(new_y)})

	return ret

#Create a map of random sea tiles
def create_sea():
	ret = []
	row = 0
	for y in range(y_len):
		ret.append([])
		col = 0
		for x in range(x_len):
			ret[row].append('0' + str(random.randint(1,4)))
			col += 1
		row += 1
	return ret


# Choose
def seed_continents():
	for i in range(continents):
		c = get_rand_unique_loc()
		c['i'] = str(c['x'])+','+str(c['y'])
		chosen_land_tiles.append(c['i'])
		land_tile_options.extend(get_adjacent_no_diagonal(c['x'],c['y']))
		land_tiles.append(c)
		new_map[c['y']][c['x']] = 'FF' #land_all[random.randint(0,len(land_all)-1)]



def build_continents():
	cid = chosen_land_tiles[0]
	while len(land_tiles) < land_num_tiles:
		while cid in chosen_land_tiles:
			idx = random.randint(0,len(land_tile_options)-1)
			c = land_tile_options[idx]
			cid = land_tile_options[idx]['i']
		del land_tile_options[idx]
		chosen_land_tiles.append(cid)
		new_map[c['y']][c['x']] = 'FF' #land_all[random.randint(0,len(land_all)-1)]
		land_tiles.append(c)
		#TODO: Optimize below for loop, objects cannot be compared using and if/in statement
		for opt in get_adjacent_no_diagonal(c['x'],c['y']):
			in_land_tiles = False
			for tile in land_tiles:
				if tile['x'] == opt['x'] and tile['y'] == opt['y']:
					in_land_tiles = True
					break
			if not in_land_tiles:
				land_tile_options.append(opt)
			#if opt not in land_tiles:
			#	land_tile_options.append(opt)

hp_spawn_points = []

def set_coastlines(last):
	set_to_sea = 0
	#random.shuffle(land_tiles)
	for l_tile in land_tiles:
		sets = []
		#print l_tile
		for adj in get_adjacent(l_tile['x'],l_tile['y']):
			sets.append(set(tile_sets[new_map[adj['y']][adj['x']]][opposing[adj['d']]])) 
		intersect = set(coastal_tiles + ['FF'] + sea_all).intersection(*sets)
		if len(intersect) > 0:
			t = list(intersect)[random.randint(0,len(intersect)-1)]
			new_map[l_tile['y']][l_tile['x']] = t
			#if t in ['0D','0E','0F','10','1B','1C','1D','1E','1F'] and last:
			#	river_spawn_points.append(l_tile)
			if t in ['0D','0E','0F','10'] and last:
				l_tile['hex'] = t
				hp_spawn_points.append(l_tile)
		elif not last:
			new_map[l_tile['y']][l_tile['x']] = '0' + str(random.randint(1,4))
			set_to_sea += 1
		if last and new_map[l_tile['y']][l_tile['x']] == 'FF':
			inland_regions.append(l_tile)
	return set_to_sea


def set_inland_features():
	for l_tile in inland_regions:
		new_map[l_tile['y']][l_tile['x']] = 'FF'



def form_inland_features():
	random.shuffle(inland_regions)
	ret = 0
	for l_tile in inland_regions:
		sets = []
		#print l_tile
		for adj in get_adjacent(l_tile['x'],l_tile['y']):
			sets.append(set(tile_sets[new_map[adj['y']][adj['x']]][opposing[adj['d']]])) 
		intersect = set(features).intersection(*sets)
		if len(intersect) > 0:
			t = list(intersect)[random.randint(0,len(intersect)-1)]
			new_map[l_tile['y']][l_tile['x']] = t
		else:
			new_map[l_tile['y']][l_tile['x']] = ls[random.randint(0,len(ls)-1)]
			ret += 1
	return ret


def spawn_rivers():
	rivers_spawned = 0
	while rivers_spawned < rivers:
		spawn_point_idx = random.randint(0,len(river_spawn_points)-1)
		spawn_point = river_spawn_points[spawn_point_idx]
		new_map[spawn_point['y']][spawn_point['x']] = river_spawn_tiles[new_map[spawn_point['y']][spawn_point['x']]]
		river_ext_pts.append(river_spawn_points[spawn_point_idx])
		del river_spawn_points[spawn_point_idx]
		rivers_spawned += 1

def extend_rivers():
	i = 0
	while len(river_ext_pts) > 0:
		river_ext_pt_idx = random.randint(0,len(river_ext_pts)-1)
		river_ext_pt = river_ext_pts[river_ext_pt_idx]
		adjacents = get_adjacent_no_diagonal(river_ext_pt['x'],river_ext_pt['y'])
		for adjacent in adjacents:
			if not new_map[adjacent['y']][adjacent['x']] in ['01','02','03','04'] and tiles[new_map[river_ext_pt['y']][river_ext_pt['x']]][adjacent['d']] == 'R':
				if not new_map[adjacent['y']][adjacent['x']] in coastal_tiles:
					if not new_map[adjacent['y']][adjacent['x']] in river_tiles:
						bag_of_rivers = []
						for river_tile in river_tiles:
							if tiles[river_tile][opposing[adjacent['d']]] == 'R':
								bag_of_rivers.append(river_tile)
						new_map[adjacent['y']][adjacent['x']] = bag_of_rivers[random.randint(0,len(bag_of_rivers)-1)]
						ext_adjacents = get_adjacent_no_diagonal(river_ext_pt['x'],river_ext_pt['y'])
						for ext_adjacent in ext_adjacents:
							if tiles[new_map[adjacent['y']][adjacent['x']]][opposing[ext_adjacent['d']]] == 'R':
								river_ext_pts.append(ext_adjacent)
					else:
						pass
				else:
					if new_map[adjacent['y']][adjacent['x']] in river_spawn_tiles:
						new_map[adjacent['y']][adjacent['x']] = river_spawn_tiles[new_map[adjacent['y']][adjacent['x']]]

		del river_ext_pts[river_ext_pt_idx]
		i += 1

inland_rectangles = []
def get_area():
	random.randint(2,)

inland_up_cols = []

def find_inland_rows():
	row = 0
	inland_right_rows = []
	for y in range(y_len):
		col = 0
		inland_right_rows.append([])
		for x in range(x_len):
			inland_right_rows[row].append(0)
			if new_map[y][x] in inland_tiles:
				inland_right_rows[row][col] = 1
				valid = True
				trace_x = x
				while valid == True:
					if trace_x == x_len-1:
						trace_x = 0
					else:
						trace_x += 1
					if new_map[y][trace_x] in inland_tiles:
						inland_right_rows[row][col] += 1
					else:
						valid = False
			col += 1
		row += 1
	#for r in inland_right_rows:
	#	print r

def find_inland_cols():
	col = x_len-1
	inland_up_cols = [[0 for x in xrange(x_len)] for x in xrange(y_len)]
	while col >= 0:
		row = y_len-1
		while row >= 0:
			if new_map[row][col] in inland_tiles:
				inland_up_cols[row][col] = 1
				valid = True
				trace_y = row
				while valid == True:
					if trace_y == 0:
						trace_y = y_len-1
					else:
						trace_y = trace_y-1
					if new_map[trace_y][col] in inland_tiles:
						inland_up_cols[row][col] += 1
					else:
						valid = False
			row -= 1
		col -= 1
	#for r in inland_up_cols:
	#	print r	
incan_cities = []
native_villages = []

def set_native_villages():
	villages_layer = ''
	villages = ['00','0D']
	for y in range(y_len):
		for x in range(x_len):
			if new_map[y][x] in ['09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','19','1A','1B']:
				skip = False
				if new_map[y][x] in ['0D','0E','0F','10']:
					for hp_tile in hp_tiles:
						if hp_tile['x'] == x and hp_tile['y'] == y:
							print 'added HP', x, y
							villages_layer += hp_tile['hex']
							skip = True
				if not skip:
					num = random.randint(0,1000)
					if num < 100:
						if num < 15:
							villages_layer += '0D'
							incan_cities.append({'x':x,'y':y})
						else:
							villages_layer += '00'
							native_villages.append({'x':x,'y':y})
					else:
						villages_layer += 'FF'
			else:
				villages_layer += 'FF'
	if testing:
		test_string = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'
		villages_layer = test_string + villages_layer[512:]
	return villages_layer



def write_file():
	homeports = set_hps()
	villages = set_native_villages()
	f = open(filepath, "w+")
	f.seek(0)
	test_list = ['01','02','03','04','05','06','07','08','09','0a','0b','0c','0d','0e','0f','10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f','20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f','30','31','32','33','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f','40','41','42','43','44','45','46','47','48','49','4a','4b','4c','4d','4e','4f','50','51','52','53','54','55','56','57','58','59','5a','5b','5c','5d','5e','5f','60','61','62','63','64','65','66','67','68','69','6a','6b','6c','6d','6e','6f','70','71','72','73','74','75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
	out = ''
	r = 0
	for map_row in new_map:
		if r < 63 and testing:
			map_row[0:4] = test_list[0:4]
			del test_list[0:4]
		for map_col in map_row:
			out += map_col
		r += 1

	f.write(binascii.unhexlify(out))
	if reveal:
		f.write(binascii.unhexlify('1F'*6400))
	else:
		f.write(binascii.unhexlify('00'*6400))
	f.write(binascii.unhexlify('FF'*6400))
	f.write(binascii.unhexlify(villages))
	f.write(binascii.unhexlify('FF'*6400))
	f.write(binascii.unhexlify('FF'*6400))
	f.write(binascii.unhexlify('FF'*6400))
	f.write(open('PLAYER_VARS.SAV', "r").read())
	f.write(open('SHIPS.SAV', "r").read())
	f.write(binascii.unhexlify(homeports))
	f.write(open('CITIES.SAV', "r").read())
	#f.truncate()
	f.close()

hp_tiles = []

def set_hps():
	string = ''
	p = 0
	for hp in ['Sevilla','Lisbon','Amsterdam','London','Nantes']:
		idx = random.randint(0,len(hp_spawn_points)-1)
		y = hp_spawn_points[idx]['y']
		x = hp_spawn_points[idx]['x']
		print hp_spawn_points[idx]
		print new_map[y][x]
		hp_tiles.append({'hex':homeport_tiles[new_map[y][x]],'x':x,'y':y})
		new_map[y][x] = homeport_tiles[new_map[y][x]]
		del hp_spawn_points[idx]
		spaces = 16 - len(hp)
		string += hp.encode('hex') + ('0'*spaces*2)
		string += '0900' + '0' + str(p) + '00'
		string += hex(x)[2:] + ('0' * (8-len(hex(x)[2:])))
		string += hex(y)[2:] + ('0' * (8-len(hex(y)[2:])))
		pop = random.randint(5000,20000)
		string += hex(pop)[2:] + ('0' * (8-len(hex(pop)[2:])))
		string += '0000F0038B038B01BB013C00B5002800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000D430000064000000'
		p += 1
	return string

def set_cities():

	pass




print 'Creating map'
new_map = create_sea()
print 'Seeding continents'
seed_continents()
print 'Building continents'
build_continents()
print 'Shaping coastlines'
sea = 6400 - len(land_tiles)
while sea > 2:
	#print sea
	sea = set_coastlines(False)
set_coastlines(True)
#print sea

print "Creating inland features"
#set_inland_features()
ff = len(inland_regions)
while ff > 2:
	#print ff
	ff = form_inland_features()
#print ff
print 
#set_coastlines(True)
#print "Spawning rivers"
#spawn_rivers()
#print "Extending rivers"
#extend_rivers()
#print "Creating mountains & valleys"
#find_inland_rows()
#find_inland_cols()
print "Building native villages & incan cities"

print "Writing to file"
write_file()
print 'Done.'
