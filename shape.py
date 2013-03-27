import pygame
from pygame.locals import *

from Box2D import *

class Shape:
	def __init__(self, game, body=None, color=(255,255,255,255), kind="box", position=(0, 0), params=(), density=1.0, friction=0.3, restitution=1.0):
		self.game = game
		self.color = color

		if not body:
			# Define the dynamic body. We set its position and call the body factory.
			bodyDef = b2BodyDef()
			bodyDef.position.Set(*position)
			bodyNew = game.world.CreateBody(bodyDef)

			# Define another box shape for our dynamic body.
			shapeDef = b2PolygonDef()

			# Set the density to be non-zero, so it will be dynamic.
			shapeDef.density = density

			# Override the default friction.
			shapeDef.friction = friction

			# Set the restitution constant for bounce
			shapeDef.restitution = restitution

			if kind is "box":
				shapeDef.SetAsBox(*params)
			elif kind is "polygon":
				shapeDef.setVertices(params)
			else:
				pass

			# Add the shape to the body.
			bodyNew.CreateShape(shapeDef)

			# Now tell the dynamic body to compute it's mass properties base on its shape.
			bodyNew.SetMassFromShapes()

			self.body = bodyNew

		else:
			self.body = body

	@classmethod
	def initGround(klass, game):
		world = game.world

		# Define the ground body.
		groundBodyDef = b2BodyDef()
		groundBodyDef.position.Set(0.0, -5.0)
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
