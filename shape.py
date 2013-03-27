import pygame
from pygame.locals import *

from Box2D import *

class Shape:
	def __init__(self, game, body, color):
		self.game = game
		self.body = body
		self.color = color

	@classmethod
	def initGround(klass, game):
		world = game.world

		# Define the ground body.
		groundBodyDef = b2BodyDef()
		groundBodyDef.position.Set(0.0, -10.0)
		groundBodyDef.mass = 0

		# Call the body factory which allocates memory for the ground body
		# from a pool and creates the ground box shape (also from a pool).
		# The body is also added to the world.
		groundBody = world.CreateBody(groundBodyDef)

		# Define the ground box shape.
		groundShapeDef = b2PolygonDef()

		# The extents are the half-widths of the box.
		groundShapeDef.SetAsBox(50.0, 10.0)

		# Add the ground shape to the ground body.
		groundBody.CreateShape(groundShapeDef)

		return klass(game, groundBody, (127,127,127,127))

	def draw(self):
		body = self.body
		game = self.game
		screen = self.game.screen

		for shape in body.shapeList:
			vertices = [b2Mul(body.GetXForm(), v)*game.ppm for v in shape.vertices]

			vertices = [(v[0], game.height-v[1]) for v in vertices]

			pygame.draw.polygon(screen, self.color, vertices)
