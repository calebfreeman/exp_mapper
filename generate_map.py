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
land_perc = .4
land_num_tiles = land_perc * x_len * y_len
continents = 20

new_map = []
up = []
rt = []
lt = []
dn = []


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
land_all = ['05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','19','1A','1B','1C','1D','1E','1F','20','21','22','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F','30','31','32','33','34','35','36','37','38','39','3A','3B','3C','3D','3E','3F','40','41','42','43','44','45','46','47','48','49','4A','4B','4C','4D','4E','4F','50','51','52','53','54','55','56','57','58','59','5A','5B','5C','5D','5E','5F','60','61','62','63','64','65','66','67','68','69','6A','6B','6C','6D','6E','6F','70','71','72','73','74']


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
	'05':{'t':'L','r':'L','b':'S','l':'S','tr':'L','br':'S','tl':'S','bl':'S'},
	'06':{'t':'L','r':'S','b':'S','l':'L','tr':'S','br':'S','tl':'L','bl':'S'},
	'07':{'t':'S','r':'S','b':'L','l':'L','tr':'S','br':'S','tl':'S','bl':'L'},
	'08':{'t':'S','r':'L','b':'L','l':'S','tr':'L','br':'L','tl':'S','bl':'S'},
	'09':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'S','l':'L','tl':'L'},
	'0A':{'t':'L','tr':'L','r':'L','br':'S','b':'L','bl':'L','l':'L','tl':'L'},
	'0B':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
	'0C':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'S'},
	'0D':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'S','l':'S','tl':'S'},
	'0E':{'t':'L','tr':'L','r':'L','br':'S','b':'S','bl':'S','l':'L','tl':'L'},
	'0F':{'t':'L','tr':'S','r':'S','br':'S','b':'L','bl':'L','l':'L','tl':'L'},
	'10':{'t':'S','tr':'S','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'S'},
	'11':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'S','l':'L','tl':'L'},
	'12':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'S'},
	'13':{'t':'L','tr':'L','r':'L','br':'S','b':'S','bl':'S','l':'S','tl':'S'},
	'14':{'t':'L','tr':'S','r':'S','br':'S','b':'S','bl':'L','l':'L','tl':'L'},
	'15':{'t':'S','tr':'S','r':'S','br':'S','b':'L','bl':'L','l':'L','tl':'S'},
	'16':{'t':'S','tr':'S','r':'L','br':'L','b':'L','bl':'S','l':'S','tl':'S'},
	'17':{'t':'L','tr':'S','r':'S','br':'S','b':'L','bl':'L','l':'L','tl':'L'},
	'18':{'t':'L','tr':'L','r':'L','br':'L','b':'L','bl':'S','l':'S','tl':'S'},
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
	'27':{'t':'L','tr':'S','r':'L','br':'L','b':'L','bl':'L','l':'L','tl':'L'},
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
	'3C':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'3D':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'3E':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'3F':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'40':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'41':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'42':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'43':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'44':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'45':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'46':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'47':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'48':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'49':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'4A':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'4B':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'4C':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'4D':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'4E':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'4F':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'50':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'51':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'52':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'53':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
	'54':{'t':'','tr':'','r':'','br':'','b':'','bl':'','l':'','tl':''},
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

tile_sets = {}

for tile in tiles:
	if not tiles[tile]['t'] == '':
		tile_sets[tile] = {'t':[],'r':[],'b':[],'l':[],'tr':[],'br':[],'tl':[],'bl':[]}
		for adjacent_tile in tiles:
			if not tiles[adjacent_tile]['t'] == '':
				if tiles[tile]['t'] == tiles[adjacent_tile]['b'] or tiles[tile]['t'] == 'SL':
					tile_sets[tile]['t'].append(adjacent_tile)
				if tiles[tile]['tr'] == tiles[adjacent_tile]['bl'] or tiles[tile]['tr'] == 'SL':
					tile_sets[tile]['tr'].append(adjacent_tile)
				if tiles[tile]['r'] == tiles[adjacent_tile]['l'] or tiles[tile]['r'] == 'SL':
					tile_sets[tile]['r'].append(adjacent_tile)
				if tiles[tile]['br'] == tiles[adjacent_tile]['tl'] or tiles[tile]['br'] == 'SL':
					tile_sets[tile]['br'].append(adjacent_tile)
				if tiles[tile]['b'] == tiles[adjacent_tile]['t'] or tiles[tile]['b'] == 'SL':
					tile_sets[tile]['b'].append(adjacent_tile)
				if tiles[tile]['bl'] == tiles[adjacent_tile]['tr'] or tiles[tile]['bl'] == 'SL':
					tile_sets[tile]['bl'].append(adjacent_tile)
				if tiles[tile]['l'] == tiles[adjacent_tile]['r'] or tiles[tile]['l'] == 'SL':
					tile_sets[tile]['l'].append(adjacent_tile)
				if tiles[tile]['tl'] == tiles[adjacent_tile]['br'] or tiles[tile]['tl'] == 'SL':
					tile_sets[tile]['tl'].append(adjacent_tile)

chosen_land_tiles = []

for i in range(continents):
	c = get_rand_loc()
	c['i'] = str(c['x'])+','+str(c['y'])
	chosen_land_tiles.append(c['i'])
	land_tile_options += get_adjacent_no_diagonal(c['x'],c['y'])
	land_tiles.append(c)
	new_map[c['y']][c['x']] = '19'


cid = c['i']

while len(land_tiles) < land_num_tiles:
	while cid in chosen_land_tiles:
		idx = random.randint(0,len(land_tile_options)-1)
		c = land_tile_options[idx]
		cid = land_tile_options[idx]['i']
	del land_tile_options[idx]
	chosen_land_tiles.append(cid)
	new_map[c['y']][c['x']] = '19'
	land_tiles.append(c)
	for opt in get_adjacent_no_diagonal(c['x'],c['y']):
		if opt not in land_tiles:
			land_tile_options.append(opt)

for l_tile in land_tiles:
	sets = []
	#print l_tile
	for adj in get_adjacent_no_diagonal(l_tile['x'],l_tile['y']):
		sets.append(set(tile_sets[new_map[adj['y']][adj['x']]][opposing[adj['d']]])) 
	intersect = set(all_tiles).intersection(*sets)
	if len(intersect) > 0:
		new_map[l_tile['y']][l_tile['x']] = list(intersect)[random.randint(0,len(intersect)-1)]
	else:
		new_map[l_tile['y']][l_tile['x']] = '0' + str(random.randint(1,4))

for l_tile in land_tiles:
	sets = []
	#print l_tile
	for adj in get_adjacent_no_diagonal(l_tile['x'],l_tile['y']):
		sets.append(set(tile_sets[new_map[adj['y']][adj['x']]][opposing[adj['d']]])) 
	intersect = set(all_tiles).intersection(*sets)
	if len(intersect) > 0:
		new_map[l_tile['y']][l_tile['x']] = list(intersect)[random.randint(0,len(intersect)-1)]
	else:
		pass


f = open("out.txt", "w")
f.seek(0)
for map_row in new_map:
	for map_col in map_row:
		f.write(map_col)
f.truncate()
f.close()

