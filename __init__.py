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
		pygame.init()

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
		pygame.display.set_caption('Simple pygame example')
		self.clock = pygame.time.Clock()

		self.fonts = dict()
		self.fonts['title'] = pygame.font.Font('fonts/pushups.otf', 50)

		self.colors = dict()
		self.colors['background'] = (255,255,255)

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
		colors = self.colors

		# Define the walls.
		Shape.initWalls(self)

		# Define the dynamic body.
		body1 = Shape(self,
				kind = "box",
				position = (15.0, 20.0),
				params = (1.0, 1.0),
				restitution = 0.5
		)

		# Add shape
		shapes.append(body1)

		# Define another body
		body2 = Shape(self,
				kind = "box",
				position = (15.5, 23.0),
				params = (1.0, 1.0),
				restitution = 0.8
		)

		# Add shape
		shapes.append(body2)

		# Define another body
		body3 = Shape(self,
				kind = "circle",
				position = (16, 15.0),
				params = 1.0,
				restitution = 0.8
		)

		# Add shape
		shapes.append(body3)

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

			screen.fill(colors['background'])

			title = self.fonts['title'].render('Hello there!', True, (0,0,0))
			screen.blit(title, (20, 20))

			for shape in shapes:
				shape.draw()

			# Instruct the world to perform a single step of simulation. It is
			# generally best to keep the time step and iterations fixed.
			world.Step(timeStep, iterations, iterations)

			pygame.display.flip()
			self.clock.tick(self.fps)

	def toScreenCoords(self, coords):
		# Scale and flip
		return coords[0]*self.ppm, game.height-(coords[1]*self.ppm)

	def toWorldCoords(self, coords):
		# Scale and flip
		return coords[0]/self.ppm, (game.height-coords[1])/self.ppm

if __name__ == "__main__":
	game = Game()
	game.run()

	pygame.quit()
