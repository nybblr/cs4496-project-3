import pygame
from pygame.locals import *

from Box2D import *

import physics
import draw
from shape import *

class Game:
	def __init__(self):
		# --- constants ---
		self.ppm = 20.0 # pixels per meter
		self.fps = 60
		self.time_step = 1.0 / self.fps
		self.width, self.height = 640, 480

		# --- pygame setup ---
		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
		pygame.display.set_caption('Simple pygame example')
		self.clock = pygame.time.Clock()

		# Define the size of the world. Simulation will still work
		# if bodies reach the end of the world, but it will be slower.
		worldAABB=b2AABB()
		worldAABB.lowerBound.Set(-100.0, -100.0)
		worldAABB.upperBound.Set(100.0, 100.0)

		# Define the gravity vector.
		gravity = b2Vec2(0.0, -10.0)

		# Do we want to let bodies sleep?
		doSleep = True

		# Construct a world object, which will hold and simulate the rigid bodies.
		self.world = b2World(worldAABB, gravity, doSleep)

		self.shapes = []

	def run(self):
		world = self.world
		screen = self.screen
		shapes = self.shapes

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

		# Add shape
		shapes.append(Shape(self, groundBody, (255,127,127,127)))

		# Define the dynamic body. We set its position and call the body factory.
		bodyDef = b2BodyDef()
		bodyDef.position.Set(0.0, 4.0)
		body = world.CreateBody(bodyDef)

		# Define another box shape for our dynamic body.
		shapeDef = b2PolygonDef()
		shapeDef.SetAsBox(1.0, 1.0)

		# Set the box density to be non-zero, so it will be dynamic.
		shapeDef.density = 1.0

		# Override the default friction.
		shapeDef.friction = 0.3

		# Add the shape to the body.
		body.CreateShape(shapeDef)

		# Now tell the dynamic body to compute it's mass properties base on its shape.
		body.SetMassFromShapes()

		# Add shape
		shapes.append(Shape(self, body, (127,127,127,127)))

		# Prepare for simulation. Typically we use a time step of 1/60 of a
		# second (60Hz) and 10 iterations. This provides a high quality simulation
		# in most game scenarios.
		timeStep = 1.0 / 60.0
		iterations = 10

		# This is our little game loop.
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					running = False

			screen.fill((0, 0, 0, 0))

			for shape in shapes:
				shape.draw()

			# Instruct the world to perform a single step of simulation. It is
			# generally best to keep the time step and iterations fixed.
			world.Step(timeStep, iterations, iterations)

			# Now print the position and angle of the body.
			position = body.GetPosition()
			angle = body.GetAngle()

			pygame.display.flip()
			self.clock.tick(self.fps)

if __name__ == "__main__":
	game = Game()
	game.run()

	pygame.quit()
