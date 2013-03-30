from shape import *

class Paddle:
    def __init__(self, game):
        self.game = game
        self.position = (1,0.1)
        self.color = (197,147,83)
        
        # Define the dynamic body. We set its position and call the body factory.
        bodyDef = b2BodyDef()
        bodyDef.position.Set(self.position[0], self.position[1])
        bodyNew = game.world.CreateBody(bodyDef)

        # Define another shape for our dynamic body.
        shapeDef = b2PolygonDef()

        shapeDef.setVertices([(0.0,0.0),(4.0,0.0),(4.0,0.5),(0.0,0.5)])

        # Set the density to be non-zero, so it will be dynamic.
        shapeDef.density = 10.0

        # Override the default friction.
        shapeDef.friction = 0.0

        # Set the restitution constant for bounce
        shapeDef.restitution = 1.1

        # Add the shape to the body.
        bodyNew.CreateShape(shapeDef)

        # Now tell the dynamic body to compute it's mass properties base on its shape.
        bodyNew.SetMassFromShapes()

        self.body = bodyNew

    def move(self, linearX, angularY):
        deltaX = self.body.position[0] - linearX
        self.body.SetLinearVelocity(b2Vec2(-2*deltaX,0))
        #if self.body.position[1] < 2 and self.body.position[1] > -0.5:
        #    self.body.SetAngularVelocity(angularY)
        self.body.SetAngularVelocity(angularY)

    def draw(self):
        body = self.body
        game = self.game
        screen = self.game.screen
        for shape in body.shapeList:
            vertices = [b2Mul(body.GetXForm(), v)*game.ppm for v in shape.vertices]
            vertices = [(v[0], game.height-v[1]) for v in vertices]
            pygame.draw.polygon(screen, self.color, vertices)
