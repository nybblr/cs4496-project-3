import pygame
from pygame.locals import *

from block import *

class Level:
	def __init__(self, game):
		self.blocks = list()
		self.game = game

	def initFromFile(self, filename, offset=(0,0)):
		game = self.game
		blocks = self.blocks

		sprite = pygame.image.load(filename)

		for x in range(sprite.get_width()):
			for y in range(sprite.get_height()):
				color = sprite.get_at((x, y))

				rgb = (color[0], color[1], color[2])
				density = 0 if color[3] is 255 else color[3]/50.0

				if color[3] is not 0:
					blocks.append(Block(
						game,
						position = (x+offset[0]+game.grid/2.0, game.gheight-y-offset[1]-game.grid/2.0),
						color = rgb,
						density = density,
					))
