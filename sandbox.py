import pygame
from pygame.locals import *

from Box2D import *

import physics
import draw
from shape import *
from paddle import *
from block import *

class Game:
        def __init__(self):
                # --- constants ---
                self.ppm = 20.0 # pixels per meter
                self.grid = 1.0 / 1.5 # grid cell size in world coords
                self.fps = 60
                self.warp = 0.75 # simulation speed ratio
                self.time_step = 1.0 / self.fps
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
                self.blocks = []
                self.walls = []
                self.levels = []
                # self.paddle = None

                # Define the walls.
                self.initWalls()

                # Define the paddle.
                self.paddle = Paddle(self, 1, 0.5)

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

        def run(self):
                world = self.world
                screen = self.screen
                shapes = self.shapes
                colors = self.colors

                # Define the walls.
                self.initWalls()

                # Define the dynamic body.
                body1 = Shape(self,
                                kind = "box",
                                position = (15.0, 11.0),
                                params = (1.0, 1.0),
                                restitution = 0.8
                )

                # Add shape
                shapes.append(body1)

                # Define another body
                body2 = Shape(self,
                                kind = "box",
                                position = (14.0, 13.0),
                                params = (1.0, 1.0),
                                restitution = 0.8,
                )

                # Add shape
                shapes.append(body2)

                # Define another body
                body3 = Shape(self,
                                kind = "box",
                                position = (12.9, 11.0),
                                params = (1.0, 1.0),
                                restitution = 0.8,
                )

                # Add shape
                shapes.append(body3)

                # Define another body
                body4 = Shape(self,
                                kind = "box",
                                position = (13.8, 9.0),
                                params = (1.0, 1.0),
                                restitution = 0.8,
                )

                # Add shape
                shapes.append(body4)


                # Define another body
                body5 = Shape(self,
                                kind = "circle",
                                position = (4.0, 15.0),
                                params = 1.0,
                                restitution = 0.8,
                                density = 5
                )

                # Add shape
                shapes.append(body5)

                # Define another body
                body6 = Shape(self,
                                kind = "polygon",
                                position = (12.8, 7.5),
                                params = [(0.0,0.0),(3.0,0.0),(3.0,0.5),(0.0,0.5)],
                                restitution = 0.8,
                                density = 0
                )

                # Add shape
                shapes.append(body6)

                block = pygame.image.load("sprites/CoinBlock.jpg").convert()
                block = pygame.transform.scale(block, (50, 50))
                blockrect = block.get_rect()

                # Prepare for simulation. Typically we use a time step of 1/60 of a
                # second (60Hz) and 10 iterations. This provides a high quality simulation
                # in most game scenarios.
                timeStep = 1.0 / 60.0
                iterations = 10

                # Prepare for simulation. Typically we use a time step of 1/60 of a
                # second (60Hz) and 10 iterations. This provides a high quality simulation
                # in most game scenarios.
                timeStep = 1.0 / 60.0
                iterations = 10

                # Used for paddle rotation
                (oldMouseX, oldMouseY) = pygame.mouse.get_pos()

                # This is our little game loop.
                running = True
                while running:
                        (mouseX, mouseY) = pygame.mouse.get_pos()
                        
                        for event in pygame.event.get():
                                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                                        running = False

                        screen.fill(colors['background'])

                        title = self.fonts['title'].render('Hello there!', True, (0,0,0))
                        screen.blit(title, (20, 20))

                        blockrect = blockrect.move([2,2])
                        screen.blit(block, blockrect)

                        for shape in shapes:
                                shape.draw()

                        self.paddle.move((mouseX/self.ppm)-2, oldMouseY-mouseY)
                        self.paddle.draw()

                        # Instruct the world to perform a single step of simulation. It is
                        # generally best to keep the time step and iterations fixed.
                        world.Step(timeStep, iterations, iterations)

                        pygame.display.flip()
                        self.clock.tick(self.fps)

                        oldMouseX = mouseX
                        oldMouseY = mouseY

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
