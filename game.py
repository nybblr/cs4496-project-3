import pygame
from pygame.locals import *

from Box2D import *

import physics
import draw
from contact import *

from level import *
from shape import *
from block import *
from paddle import *

class Game:
  def __init__(self):
    # --- constants ---
    self.ppm = 20.0 # pixels per meter
    self.grid = 1.0 / 1.5 # grid cell size in world coords
    self.fps = 60
    self.warp = 0.75 # simulation speed ratio
    self.timeStep = 1.0 / self.fps
    self.width, self.height = 640, 480

    self.mwidth = self.width / self.ppm
    self.mheight = self.height / self.ppm
    self.gwidth = self.mwidth / self.grid
    self.gheight = self.mheight / self.grid

    # --- pygame setup ---
    pygame.init()

    self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
    pygame.display.set_caption('Simple pygame example')
    self.clock = pygame.time.Clock()

    self.fonts = dict()
    self.fonts['title'] = pygame.font.Font('fonts/pushups.otf', 50)
    self.fonts['lives'] = pygame.font.Font('fonts/pushups.otf', 30)

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

    self.contact = Contact(self)
    self.world.SetContactListener(self.contact)

    self.shapes = []
    self.blocks = []
    self.walls = []
    self.levels = []
    # self.paddle = None
    self.lives = 5
    self.points = 0

    self.isRunning = True

    # Define the walls.
    self.initWalls()

    # Define the paddle.
    self.paddle = PaddleKey(self, 1, 0.5)

  def initWalls(self):
    world = self.world

    walls = (
        # ((0.0, -1.0), (self.mwidth, 1.0)),
        ((0.0, self.mheight+1.0), (self.mwidth, 1.0)),
        ((-1.0, 0.0), (1.0, self.mheight)),
        ((self.mwidth+1.0, 0.0), (1.0, self.mheight)),
    )

    # walls = (
    #               ((0,0), (game.width/game.ppm,0)),
    #               ((0,0), (0,game.height/game.ppm)),
    #               ((game.width/game.ppm,0), (game.width/game.ppm,game.height/game.ppm)),
    # )

    for wallParams in walls:
      # wall = Shape(game,
      #               kind = "line",
      #               params = wallParams,
      # )

      wall = Shape(self,
          kind = 'box',
          position = wallParams[0],
          params = wallParams[1],
          density = 0,
      )

      self.walls.append(wall)

  def startScreen(self):
    screen = self.screen
    colors = self.colors
    world = self.world

    startBlock = Shape(self, position = (self.mwidth/2, 5.0), params = (10, 10))

    title1 = self.fonts['title'].render('WELCOME TO BREAKDOWN', True, (0,0,0))
    title2 = self.fonts['title'].render('Press any key', True, (255,255,255))
    title1Size = self.fonts['title'].size('WELCOME TO BREAKDOWN')
    title2Size = self.fonts['title'].size('Press any key')

    running = True
    while running:
      screen.fill(colors['background'])

      screen.blit(title1, (self.width/2 - title1Size[0]/2, 20))
      startBlock.draw()
      screen.blit(title2, (self.width/2 - title2Size[0]/2, 325))
      startBlock.body.setAngle(0.01+startBlock.body.GetAngle())
      if (startBlock.body.GetAngle() >= 360):
        startBlock.body.setAngle(startBlock.body.GetAngle() - 360)

      pygame.display.flip()

      for event in pygame.event.get():
        if event.type == KEYDOWN:
          world.DestroyBody(startBlock.body)
          running = False

  def gameScreen(self):
    world = self.world
    screen = self.screen
    shapes = self.shapes
    blocks = self.blocks
    colors = self.colors
    paddle = self.paddle

    self.level = Level(self)
    level = self.level
    level.initFromFile('sprites/mario-stable.png', (12, 4))

    # Define another body
    self.ball = Shape(self,
        kind = "circle",
        position = (18, 5.0),
        params = self.grid,
        restitution = 0.8
    )

    ball = self.ball

    # Add shape
    shapes.append(ball)

    # Prepare for simulation. Typically we use a time step of 1/60 of a
    # second (60Hz) and 10 iterations. This provides a high quality simulation
    # in most game scenarios.
    iterations = 10

    # This is our little game loop.
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
          self.isRunning = False
          running = False

      Shape.updatePending()

      screen.fill(colors['background'])

      if ball.body.position[1] < -5:
        ball.body.SetLinearVelocity((0, 0))
        ball.body.position = (18, 5.0)
        self.lives -= 1
        if self.lives <= 0:
          self.loseScreen()
          running = False
          break

      title = self.fonts['lives'].render('Lives left: ' + str(self.lives), True, (0,0,0))
      screen.blit(title, (20, 20))

      for shape in shapes:
        shape.draw()

      for block in blocks:
        block.draw()

      for block in level.blocks:
        block.draw()

      linMove = 0
      angMove = 0
      pressedKeys = pygame.key.get_pressed()
      if pressedKeys[K_LEFT]:
        linMove = -1
      elif pressedKeys[K_RIGHT]:
        linMove = 1

      if pressedKeys[K_s]:
        angMove = 1
      elif pressedKeys[K_d]:
        angMove = -1

      if pressedKeys[K_c]:
        angMove *= 2

      self.paddle.move(linMove, angMove)
      paddle.draw()

      # Instruct the world to perform a single step of simulation. It is
      # generally best to keep the time step and iterations fixed.
      world.Step(self.timeStep * self.warp, iterations, iterations)

      pygame.display.flip()
      self.clock.tick(self.fps)

  def loseScreen(self):
    screen = self.screen
    colors = self.colors
    world = self.world

    title1 = self.fonts['title'].render('YOU LOSE', True, (0,0,0))
    title2 = self.fonts['title'].render('Press any key', True, (0,0,0))
    title1Size = self.fonts['title'].size('YOU LOSE')
    title2Size = self.fonts['title'].size('Press any key')

    running = True
    while running:
      screen.blit(title1, (self.width/2 - title1Size[0]/2, 205))
      screen.blit(title2, (self.width/2 - title2Size[0]/2, 240))

      pygame.display.flip()

      for event in pygame.event.get():
        if event.type == QUIT:
          self.isRunning = False
          running = False
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.isRunning = False
          running = False

  def reset(self):
    world = self.world
    shapes = self.shapes
    blocks = self.blocks
    level = self.level

    for shape in shapes:
      shape.destroy(True)

    for block in blocks:
      block.destroy(True)

    for block in level.blocks:
      block.destroy(True)

    self.shapes = []
    self.blocks = []
    self.walls = []
    self.levels = []
    self.lives = 5
    self.points = 0

  def toScreenCoords(self, coords):
    # Scale and flip
    return coords[0]*self.ppm, game.height-(coords[1]*self.ppm)

  def toWorldCoords(self, coords):
    # Scale and flip
    return coords[0]/self.ppm, (game.height-coords[1])/self.ppm

if __name__ == "__main__":
  game = Game()
  game.startScreen()
  while(game.isRunning):
    game.gameScreen()
    game.reset()

  pygame.quit()
