from shape import *

class Block:
  def __init__(self, game, position=(0,0), color=(0,0,0), density=1.0, tough=2, static=False):
    self.game = game
    self.position = position
    self.color = color
    self.maxTough = tough
    self.tough = self.maxTough
    self.density = density
    self.static = static
    self.shape = Shape(game,
        kind = 'box',
        color = color,
        position = (position[0]*game.grid, position[1]*game.grid),
        params = (game.grid/2.0, game.grid/2.0),
        density = density if not static else 0,
        pointer = self,
    )

  def handleCollision(self, cp):
    self.bump()

  def handleBoundary(self):
    self.destroy()

  def bump(self):
    if self.tough is not 0:
      self.tough -= 1

    # Did we kill off static?
    if self.tough is 0:
      if self.static:
        self.static = False
        self.shape.density(self.density)
        self.tough = self.maxTough
        self.game.award('blast')
      else:
        self.game.award('obliterate')
        self.destroy()

  def destroy(self, now=False):
    if not self.shape:
      return

    self.shape.destroy(now)
    self.shape = None
    if self in self.game.blocks:
      self.game.blocks.remove(self)

  def draw(self):
    if not self.shape:
      return

    if self.tough is 0 and not self.static:
      # print("NOT GOOD!!!")
      alpha = 1.0
    else:
      alpha = self.tough / float(self.maxTough)

    self.shape.draw(
        alpha = alpha
    )
