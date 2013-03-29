from shape import *

class Block:
	def __init__(self, game, position=(0,0), color=(0,0,0)):
		self.game = game
		self.position = position
		self.color = color
		self.shape = Shape(game, kind="box", color=color, position=position, params=(game.grid, game.grid))

	def draw(self):
		self.shape.draw()
