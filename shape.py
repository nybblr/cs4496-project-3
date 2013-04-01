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
			shapeDef = None

			if kind is "box":
				shapeDef = b2PolygonDef()
				shapeDef.SetAsBox(*params)
			elif kind is "polygon":
				shapeDef = b2PolygonDef()
				shapeDef.setVertices(params)
			elif kind is "line":
				shapeDef = b2PolygonDef()
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
				((0.0, -1.0), (game.mwidth, 1.0)),
				((0.0, game.mheight+1.0), (game.mwidth, 1.0)),
				((-1.0, 0.0), (1.0, game.mheight)),
				((game.mwidth+1.0, 0.0), (1.0, game.mheight)),
		)

		# walls = (
		# 		((0,0), (game.width/game.ppm,0)),
		# 		((0,0), (0,game.height/game.ppm)),
		# 		((game.width/game.ppm,0), (game.width/game.ppm,game.height/game.ppm)),
		# )

		for wallParams in walls:
			# wall = Shape(game,
			# 		kind = "line",
			# 		params = wallParams,
			# )

			wall = Shape(game,
					kind = 'box',
					position = wallParams[0],
					params = wallParams[1],
					density = 0,
			)

			game.walls.append(wall)

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

