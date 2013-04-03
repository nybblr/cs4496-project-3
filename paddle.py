from shape import *

class Paddle:
  def __init__(self, game, height, angle):
    self.game = game
    self.position = (10, height)
    self.color = (197,147,83)
    self.angle = angle

    # Define the dynamic body. We set its position and call the body factory.
    bodyDef = b2BodyDef()
    bodyDef.position.Set(self.position[0], self.position[1])
    bodyNew = game.world.CreateBody(bodyDef)

    # Define another shape for our dynamic body.
    shapeDef = b2PolygonDef()
    shapeDef.setVertices([(-2.0,0.0),(2.0,0.0),(2.0,0.5),(-2.0,0.5)])

    # Set the density to be non-zero, so it will be dynamic.
    shapeDef.density = 100.0

    # Override the default friction.
    shapeDef.friction = 0.0

    # Set the restitution constant for bounce
    shapeDef.restitution = 1.5

    # Add the shape to the body.
    bodyNew.CreateShape(shapeDef)

    # Now tell the dynamic body to compute it's mass properties base on its shape.
    bodyNew.SetMassFromShapes()

    # Stops the paddle from sleeping when not moving
    bodyNew.AllowSleeping(False)

    self.body = bodyNew

    # Restrict paddle along the x axis
    lineJointDef = b2LineJointDef()
    lineJointDef.Initialize(game.walls[0].body, self.body, self.body.position, (1,0))
    self.lineJoint = game.world.CreateJoint(lineJointDef)
    self.lineJointDef = lineJointDef

  def move(self, linearX, angularY):
    deltaX = linearX - self.body.position[0]
    if self.body.position[0] > 3 and self.body.position[0] < self.game.mwidth - 3:
      self.body.SetLinearVelocity(b2Vec2(50*deltaX,0))
    elif self.body.position[0] <= 3 and deltaX > 0:
      self.body.SetLinearVelocity(b2Vec2(50*deltaX,0))
    elif self.body.position[0] >= self.game.mwidth - 3 and deltaX < 0:
      self.body.SetLinearVelocity(b2Vec2(50*deltaX,0))
    else:
      self.body.SetLinearVelocity(b2Vec2(0,0))

    if self.body.GetAngle() > -self.angle and self.body.GetAngle() < self.angle:
      self.body.SetAngularVelocity(angularY)
    elif self.body.GetAngle() >= self.angle and angularY < 0:
      self.body.SetAngularVelocity(angularY)
    elif self.body.GetAngle() <= -self.angle and angularY > 0:
      self.body.SetAngularVelocity(angularY)
    elif self.body.GetAngle() >= self.angle:
      self.body.setAngle(self.angle)
    elif self.body.GetAngle() <= -self.angle:
      self.body.setAngle(-self.angle)
    else:
      self.body.SetAngularVelocity(0)

  def draw(self):
    body = self.body
    game = self.game
    screen = self.game.screen
    for shape in body.shapeList:
      vertices = [b2Mul(body.GetXForm(), v)*game.ppm for v in shape.vertices]
      vertices = [(v[0], game.height-v[1]) for v in vertices]
      pygame.draw.polygon(screen, self.color, vertices)

class PaddleKey:
  def __init__(self, game, height, angle):
    self.game = game
    self.position = (10, height)
    self.color = (197,147,83)
    self.angle = 2 # Current angle index
    self.possibleAngles = (-0.5, -0.25, 0, 0.25, 0.5)

    # Define the dynamic body. We set its position and call the body factory.
    bodyDef = b2BodyDef()
    bodyDef.position.Set(self.position[0], self.position[1])
    bodyNew = game.world.CreateBody(bodyDef)

    # Define another shape for our dynamic body.
    shapeDef = b2PolygonDef()
    shapeDef.setVertices([(-2.0,0.0),(2.0,0.0),(2.0,0.5),(-2.0,0.5)])

    # Set the density to be non-zero, so it will be dynamic.
    shapeDef.density = 100.0

    # Override the default friction.
    shapeDef.friction = 1.0

    # Set the restitution constant for bounce
    shapeDef.restitution = 1.5

    # Add the shape to the body.
    bodyNew.CreateShape(shapeDef)

    # Now tell the dynamic body to compute it's mass properties base on its shape.
    bodyNew.SetMassFromShapes()

  # Stops the paddle from sleeping when not moving
    bodyNew.AllowSleeping(False)

    self.body = bodyNew

    # Restrict paddle along the x axis
    lineJointDef = b2LineJointDef()
    lineJointDef.Initialize(game.walls[0].body, self.body, self.body.position, (1,0))
    self.lineJoint = game.world.CreateJoint(lineJointDef)
    self.lineJointDef = lineJointDef

  def move(self, linearX, angularY):
    #deltaX = linearX - self.body.position[0]
    deltaX = linearX
    if self.body.position[0] > 3 and self.body.position[0] < self.game.mwidth - 3:
      self.body.SetLinearVelocity(b2Vec2(50*deltaX,0))
    elif self.body.position[0] <= 3 and deltaX > 0:
      self.body.SetLinearVelocity(b2Vec2(50*deltaX,0))
    elif self.body.position[0] >= self.game.mwidth - 3 and deltaX < 0:
      self.body.SetLinearVelocity(b2Vec2(50*deltaX,0))
    else:
      self.body.SetLinearVelocity(b2Vec2(0,0))

##        if self.body.GetAngle() > -self.angle and self.body.GetAngle() < self.angle:
##            self.body.SetAngularVelocity(angularY)
##        elif self.body.GetAngle() >= self.angle and angularY < 0:
##            self.body.SetAngularVelocity(angularY)
##        elif self.body.GetAngle() <= -self.angle and angularY > 0:
##            self.body.SetAngularVelocity(angularY)
##        elif self.body.GetAngle() >= self.angle:
##            self.body.setAngle(self.angle)
##        elif self.body.GetAngle() <= -self.angle:
##            self.body.setAngle(-self.angle)
##        else:
##            self.body.SetAngularVelocity(0)

    # if self.angle - angularY >= 0 and self.angle - angularY <= 4:
    self.angle = angularY + 2
    self.body.setAngle(self.possibleAngles[self.angle])
    self.body.SetAngularVelocity(0)

  # def density(self, value):
  #   for shape in self.body.shapeList:
  #     shape.SetDensity(value)

  #   self.body.SetMassFromShapes()
  #   self.body.wakeup()

  def draw(self):
    body = self.body
    game = self.game
    screen = self.game.screen
    for shape in body.shapeList:
      vertices = [b2Mul(body.GetXForm(), v)*game.ppm for v in shape.vertices]
      vertices = [(v[0], game.height-v[1]) for v in vertices]
      pygame.draw.polygon(screen, self.color, vertices)
