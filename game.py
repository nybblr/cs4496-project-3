import pygame
from pygame.locals import *

from Box2D import *

import physics
import draw
from contact import *
from boundary import *

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
    self.iterations = 10
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
    pygame.display.set_caption('BREAKDOWN')
    self.clock = pygame.time.Clock()

    self.wimage = pygame.image.load('images/trophy.png')
    self.wimagerect = self.wimage.get_rect()
    self.wimagerect = self.wimagerect.move(self.width/2 - self.wimage.get_width()/2, self.height/2 - self.wimage.get_height()/2)

    self.fonts = dict()
    self.fonts['title'] = pygame.font.Font('fonts/pushups.otf', 50)
    self.fonts['controls'] = pygame.font.Font('fonts/pushups.otf', 32)
    self.fonts['inGame'] = pygame.font.Font('fonts/pushups.otf', 30)

    self.colors = dict()
    self.colors['background'] = (255,255,255)

    self.awards = dict()
    self.awards['obliterate'] = 5
    self.awards['blast'] = 2

    # Define the size of the world. Simulation will still work
    # if bodies reach the end of the world, but it will be slower.
    margin = 5.0
    worldAABB=b2AABB()
    worldAABB.lowerBound.Set(-margin, -margin)
    worldAABB.upperBound.Set(self.mwidth+margin, self.mheight+margin)

    # Define the gravity vector.
    gravity = b2Vec2(0.0, -10.0)

    # Do we want to let bodies sleep?
    doSleep = True

    # Construct a world object, which will hold and simulate the rigid bodies.
    self.world = b2World(worldAABB, gravity, doSleep)

    self.contact = Contact(self)
    self.world.SetContactListener(self.contact)

    self.boundary = Boundary(self)
    self.world.SetBoundaryListener(self.boundary)

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
          self.controlScreen()
          running = False

  def controlScreen(self):
    screen = self.screen
    colors = self.colors

    text1 = self.fonts['title'].render('CONTROLS', True, (0,0,0))
    text2 = self.fonts['controls'].render('Use the left and right arrow keys to move.', True, (0,0,0))
    text31 = self.fonts['controls'].render('Hold \'s\' and \'d\' to rotate the', True, (0,0,0))
    text32 = self.fonts['controls'].render('paddle slightly left and right.', True, (0,0,0))
    text41 = self.fonts['controls'].render('Hold \'c\' at the same time to', True, (0,0,0))
    text42 = self.fonts['controls'].render('rotate the paddle further.', True, (0,0,0))
    text51 = self.fonts['controls'].render('Press \'p\' at any time to', True, (0,0,0))
    text52 = self.fonts['controls'].render('pause and see this info again.', True, (0,0,0))
    text6 = self.fonts['controls'].render('Press any key to resume.', True, (0,0,0))
    text1Size = self.fonts['title'].size('CONTROLS')
    text2Size = self.fonts['controls'].size('Use the left and right arrow keys to move.')
    text31Size = self.fonts['controls'].size('Hold \'s\' and \'d\' to rotate the')
    text32Size = self.fonts['controls'].size('paddle slightly left and right.')
    text41Size = self.fonts['controls'].size('Hold \'c\' at the same time to')
    text42Size = self.fonts['controls'].size('rotate the paddle further.')
    text51Size = self.fonts['controls'].size('Press \'p\' at any time to')
    text52Size = self.fonts['controls'].size('pause and see this info again.')
    text6Size = self.fonts['controls'].size('Press any key to continue.')

    running = True
    while running:
      screen.fill(colors['background'])

      screen.blit(text1, (self.width/2 - text1Size[0]/2, 20))
      screen.blit(text2, (self.width/2 - text2Size[0]/2, 100))
      screen.blit(text31, (self.width/2 - text31Size[0]/2, 145))
      screen.blit(text32, (self.width/2 - text32Size[0]/2, 175))
      screen.blit(text41, (self.width/2 - text41Size[0]/2, 220))
      screen.blit(text42, (self.width/2 - text42Size[0]/2, 250))
      screen.blit(text51, (self.width/2 - text51Size[0]/2, 295))
      screen.blit(text52, (self.width/2 - text52Size[0]/2, 325))
      screen.blit(text6, (self.width/2 - text6Size[0]/2, 370))

      pygame.display.flip()

      for event in pygame.event.get():
        if event.type == KEYDOWN:
          running = False

  def gameScreen(self):
    world = self.world
    screen = self.screen
    shapes = self.shapes
    colors = self.colors
    paddle = self.paddle

    self.level = Level(self)
    level = self.level
    level.initFromFile('sprites/mario-stable.png', (12, 4))
    self.blocks = level.blocks
    blocks = self.blocks

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

      lives = self.fonts['inGame'].render('Lives left: ' + str(self.lives), True, (0,0,0))
      points = self.fonts['inGame'].render('Points: ' + str(self.points), True, (0,0,0))

      for shape in shapes:
        shape.draw()

      blockNum = 0

      for block in blocks:
        if block.shape:
          blockNum += 1
        block.draw()

      if blockNum <= 0:
        self.winScreen()
        running = False
        break

      # for block in level.blocks:
      #   block.draw()

      linMove = 0
      angMove = 0
      
      pressedKeys = pygame.key.get_pressed()
      if pressedKeys[K_p]:
        self.controlScreen()

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

      if pressedKeys[K_f]:
        ball.density(100.0)
      else:
        ball.density(1.0)

      screen.blit(lives, (20, 400))
      screen.blit(points, (20, 440))

      # Instruct the world to perform a single step of simulation. It is
      # generally best to keep the time step and iterations fixed.
      world.Step(self.timeStep * self.warp, self.iterations, self.iterations)

      pygame.display.flip()
      self.clock.tick(self.fps)

  def winScreen(self):
    screen = self.screen
    colors = self.colors
    world = self.world

    title1 = self.fonts['title'].render('YOU WIN!!', True, (0,0,0))
    title2 = self.fonts['controls'].render('Press any key', True, (0,0,0))
    title1Size = self.fonts['title'].size('YOU WIN!!!')
    title2Size = self.fonts['controls'].size('Press any key')

    running = True
    while running:
      screen.fill(colors['background'])
      
      screen.blit(title1, (self.width/2 - title1Size[0]/2, 75))
      screen.blit(title2, (self.width/2 - title2Size[0]/2, 350))
      screen.blit(self.wimage, self.wimagerect)

      pygame.display.flip()

      for event in pygame.event.get():
        if event.type == QUIT:
          self.isRunning = False
          running = False
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.isRunning = False
          running = False

  def loseScreen(self):
    screen = self.screen
    colors = self.colors
    world = self.world

    title1 = self.fonts['title'].render('YOU LOSE', True, (0,0,0))
    title2 = self.fonts['controls'].render('Press any key', True, (0,0,0))
    title1Size = self.fonts['title'].size('YOU LOSE')
    title2Size = self.fonts['controls'].size('Press any key')

    running = True
    while running:
      screen.fill(colors['background'])
            
      screen.blit(title1, (self.width/2 - title1Size[0]/2, 205))
      screen.blit(title2, (self.width/2 - title2Size[0]/2, 250))

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

  def award(self, name):
    self.points += self.awards[name]

if __name__ == "__main__":
  game = Game()
  game.startScreen()
  while(game.isRunning):
    game.gameScreen()
    game.reset()

  pygame.quit()
