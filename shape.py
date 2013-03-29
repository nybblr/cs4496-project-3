import pygame
from pygame.locals import *

from Box2D import *

class Shape:
	def __init__(self, game, body=None, color=(0,0,0,0), kind="box", position=(0, 0), params=(), density=1.0, friction=0.3, restitution=1.0):
		self.game = game
		self.color = color

		if not body:
			# Define the dynamic body. We set its position and call the body factory.
			bodyDef = b2BodyDef()
			bodyDef.position.Set(*position)
			bodyNew = game.world.CreateBody(bodyDef)

			# Define another shape for our dynamic body.
			shapeDef = b2PolygonDef()

			if kind is "box":
				shapeDef.SetAsBox(*params)
			elif kind is "polygon":
				shapeDef.setVertices(params)
			elif kind is "circle":
				shapeDef = b2CircleDef()
				shapeDef.radius = params
			else:
				pass

			# Set the density to be non-zero, so it will be dynamic.
			shapeDef.density = density

			# Override the default friction.
			shapeDef.friction = friction

			# Set the restitution constant for bounce
			shapeDef.restitution = restitution

			# Add the shape to the body.
			bodyNew.CreateShape(shapeDef)

			# Now tell the dynamic body to compute it's mass properties base on its shape.
			bodyNew.SetMassFromShapes()

			self.body = bodyNew

		else:
			self.body = body

	@classmethod
	def initWalls(klass, game):
		world = game.world

		walls = (
				((0.0, -1.0), (game.width/game.ppm, 1.0)),
				((0.0, game.height/game.ppm+1.0), (game.width/game.ppm, 1.0)),
				((-1.0, 0.0), (1.0, game.height/game.ppm)),
				((game.width/game.ppm+1.0, 0.0), (1.0, game.height/game.ppm)),
		)

		for wallParams in walls:
			# Define the wall.
			wallDef = b2BodyDef()
			wallDef.position.Set(*wallParams[0])
			wallDef.mass = 0

			wall = world.CreateBody(wallDef)

			# Define the box shape.
			wallShape = b2PolygonDef()

			# The extents are the half-widths of the box.
			wallShape.SetAsBox(*(wallParams[1]))

			# Add the shape to the body.
			wall.CreateShape(wallShape)


		# return klass(game, groundBody, (127,127,127,127))

	def draw(self):
		body = self.body
		game = self.game
		screen = self.game.screen

		for shape in body.shapeList:
			if type(shape) is b2CircleShape:
				pos = game.toScreenCoords(body.position)
				pos = tuple([int(x) for x in pos])
				pygame.draw.circle(screen, self.color, pos, int(shape.radius*game.ppm))
			else:
				vertices = [b2Mul(body.GetXForm(), v)*game.ppm for v in shape.vertices]
				vertices = [(v[0], game.height-v[1]) for v in vertices]
				pygame.draw.polygon(screen, self.color, vertices)
