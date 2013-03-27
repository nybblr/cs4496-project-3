import pygame
from pygame.locals import *

from Box2D import *

""" This is a simple example of building and running a simulation
    using Box2D. Here we create a large ground box and a small dynamic box
"""

# --- constants ---
PPM = 20.0 # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

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
world = b2World(worldAABB, gravity, doSleep)

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

  for body in world.bodyList: # or: world.bodies
    # The body gives us the position and angle of its shapes
    for fixture in body.shapeList:
      # The fixture holds information like density and friction,
      # and also the shape.
      shape=fixture#.shape

      # Naively assume that this is a polygon shape. (not good normally!)
      # We take the body's transform and multiply it with each 
      # vertex, and then convert from meters to pixels with the scale
      # factor. 
      # vertices=[(body.GetXForm().R*v)*PPM for v in shape.vertices]
      vertices=[b2Mul(body.GetXForm(), v)*PPM for v in shape.vertices]

      # But wait! It's upside-down! Pygame and Box2D orient their
      # axes in different ways. Box2D is just like how you learned
      # in high school, with positive x and y directions going
      # right and up. Pygame, on the other hand, increases in the
      # right and downward directions. This means we must flip
      # the y components.
      vertices=[(v[0], SCREEN_HEIGHT-v[1]) for v in vertices]

      pygame.draw.polygon(screen, (127,127,127,127), vertices)


  # Instruct the world to perform a single step of simulation. It is
  # generally best to keep the time step and iterations fixed.
  world.Step(timeStep, iterations, iterations)

  # Now print the position and angle of the body.
  position = body.GetPosition()
  angle = body.GetAngle()

  pygame.display.flip()
  clock.tick(TARGET_FPS)

pygame.quit()
