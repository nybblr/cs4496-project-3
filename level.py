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

				if color[3] is not 0:
					blocks.append(Block(
						game,
						(x+offset[0], game.gheight-y-offset[1]),
						(color[0], color[1], color[2])
					))
