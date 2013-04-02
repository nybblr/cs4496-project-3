from shape import *

class Block:
	def __init__(self, game, position=(0,0), color=(0,0,0), density=1.0):
		self.game = game
		self.position = position
		self.color = color
		self.shape = Shape(game,
				kind = 'box',
				color = color,
				position = (position[0]*game.grid, position[1]*game.grid),
				params = (game.grid/2.0, game.grid/2.0),
				density = density,
				pointer = self,
		)

	def draw(self):
		self.shape.draw()
