import pygame
from pygame.locals import *

from Box2D import *

class Shape:
	def __init__(self, world, body, color):
		self.world = world
		self.body = body
		self.color = color

	def draw(self):
		body = self.body
		world = self.world
		screen = self.world.screen

		for shape in body.shapeList:
			vertices = [b2Mul(body.GetXForm(), v)*world.ppm for v in shape.vertices]

			vertices = [(v[0], world.height-v[1]) for v in vertices]

			pygame.draw.polygon(screen, self.color, vertices)
