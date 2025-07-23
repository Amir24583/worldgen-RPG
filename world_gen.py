import random
import sys
import csv
from configuration import *


def procedural_map_generator():
	width = chunkWidth
	height = chunkHeight

	drunk = {
		'waterCountdown': 40,
		'wallCountdown': 2500,
		'padding': 2,
		'x': width // 2 ,
		'y': height // 2 
	}

	def getLevelRow():
		return ['B'] * width

	level = [getLevelRow() for _ in range(height)]

	# carve walkable paths using drunkard's walk algorithm
	while drunk['wallCountdown'] > 0:
		x , y = drunk['x'], drunk['y']
		
		if level[y][x] == 'B':
			level[y][x] = ' '  # walkable tile
			drunk['wallCountdown'] -= 1
		
		roll = random.randint(1, 4)
		
		if roll == 1 and x > drunk['padding']:
			drunk['x'] -= 1
		
		if roll == 2 and x < width - 1 - drunk['padding']:
			drunk['x'] += 1
		
		if roll == 3 and y > drunk['padding']:
			drunk['y'] -= 1
		
		if roll == 4 and y < height - 1 - drunk['padding']:
			drunk['y'] += 1



	# Helper fn get all walkable (empty) tiles
	def find_empty_tiles():
		return [(x, y) for y in range(height) for x in range(width) if level[y][x] == ' ']


	# Place player
	# empty_tiles = find_empty_tiles()
	# player_x, player_y = random.choice(empty_tiles)
	# level[player_y][player_x] = 'P'

	# Place some weapons
	for _ in range(3):
		empty_tiles = find_empty_tiles()
		x, y = random.choice(empty_tiles)
		level[y][x] = 'W'

	# Place some enemies
	for _ in range(5):
		empty_tiles = find_empty_tiles()
		x, y = random.choice(empty_tiles)
		level[y][x] = 'E'

	# Place some water tiles
	# for _ in range(30):
	# 	empty_tiles = find_empty_tiles()
	# 	x, y = random.choice(empty_tiles)
	# 	level[y][x] = 'R'
	for i in range(random.randint(5, 10)):
		drunk['waterCountdown'] = random.randint(10, 20)
		drunk['x'] = random.randint(drunk['padding'], width - 1 - drunk['padding'])
		drunk['y'] = random.randint(drunk['padding'], height - 1 - drunk['padding'])
		while drunk['waterCountdown'] > 0:
			x , y = drunk['x'], drunk['y']
			
			if level[y][x] == ' ':
				level[y][x] = 'R'  # walkable tile
				drunk['waterCountdown'] -= 1
			
			roll = random.randint(1, 4)
			
			if roll == 1 and x > drunk['padding']:
				drunk['x'] -= 1
			
			if roll == 2 and x < width - 1 - drunk['padding']:
				drunk['x'] += 1
			
			if roll == 3 and y > drunk['padding']:
				drunk['y'] -= 1
			
			if roll == 4 and y < height - 1 - drunk['padding']:
				drunk['y'] += 1

	ensure_player_spawn(level)


	# make all 4 borders blank as of now only top is borderless
	level[0] = (['B'] * 2) + ([' '] * (width - 4)) + (['B'] * 2)
	level[1] = (['B'] * 2) + ([' '] * (width - 4)) + (['B'] * 2) 
	level[33] = (['B'] * 2) + ([' '] * (width - 4)) + (['B'] * 2)
	level[34] = (['B'] * 2) + ([' '] * (width - 4)) + (['B'] * 2)

	for i in range(len(level)):
		level[i][0] = ' '
		level[i][1] = ' '
		level[i][-1] = ' '
		level[i][-2] = ' '
	for row in level:
		print( ''.join(row).replace(' ', '.') )


def load_tilemap_from_csv(path):
    with open(path, newline='') as csvfile:
        tilemap = [row for row in csv.reader(csvfile)]
        tilemap2 = []
        for line in tilemap:
            tilemap2.append(line[0])

        return tilemap2
    


def find_empty_tiles(level, width, height):
		return [(x, y) for y in range(height) for x in range(width) if level[y][x] == ' ']

executed = False   
def ensure_player_spawn(tilemap):

	global executed
	if not executed:
		executed = True
	else:
		return

	has_player = any('P' in row for row in tilemap)
	if not has_player:
		empty_tiles = find_empty_tiles(tilemap, chunkWidth, chunkHeight)
		player_x, player_y = random.choice(empty_tiles)
		tilemap[player_y][player_x] = 'P'


def world_output():
	original_stdout = sys.stdout
	with open('map.csv', 'w') as file:
		sys.stdout = file
		procedural_map_generator()
		sys.stdout = original_stdout

