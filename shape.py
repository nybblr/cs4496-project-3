import pygame
from pygame.locals import *

from Box2D import *

import Queue

class Shape:
  destroyed = list()

  @classmethod
  def destroyPending(klass):
    for item in klass.destroyed:
      (world, body) = item
      world.DestroyBody(body)

    klass.destroyed = list()

  def __init__(self, game, body=None, color=(0,0,0), kind="box", position=(0, 0), params=(), density=1.0, friction=0.3, restitution=1.0, pointer=None):
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
      shape = bodyNew.CreateShape(shapeDef)

      # Point to this shape if no pointer given (for events).
      data = pointer if pointer else self

      # Set the pointer for quick access (events).
      shape.SetUserData(data)

      # Now tell the dynamic body to compute it's mass properties base on its shape.
      bodyNew.SetMassFromShapes()

      self.body = bodyNew

    else:
      self.body = body

  def destroy(self, now=False):
    self.__class__.destroyed.append((self.game.world, self.body))
    self.body = None

    if now:
      Shape.destroyPending()

  def draw(self, alpha=1.0):
    if not self.body:
      return

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

        color = self.applyAlpha(self.color, defaultAlpha=alpha)
        rgb = self.toScreenColor(color, defaultAlpha=alpha)
        # rgb = (color[0], color[1], color[2])
        # alpha = color[3]

        # s = pygame.Surface((game.width,game.height))
        # s.set_alpha(alpha)
        pygame.draw.polygon(screen, rgb, vertices)
        # screen.blit(s, (0,0))

  def toScreenColor(self, color, defaultAlpha=1.0):
    # Reformat colors
    r = color[0]
    g = color[1]
    b = color[2]
    a = defaultAlpha

    # Was alpha included?
    if len(color) is 4:
      a = color[3]

    sane = (int(r*255), int(g*255), int(b*255), int(a*255))
    return sane

  def applyAlpha(self, color, defaultAlpha=1.0):
    r = color[0]
    g = color[1]
    b = color[2]
    a = defaultAlpha

    # Was alpha included?
    if len(color) is 4:
      a = color[3]

    r = r*a + (1-a)
    g = g*a + (1-a)
    b = b*a + (1-a)

    return (r,g,b)
