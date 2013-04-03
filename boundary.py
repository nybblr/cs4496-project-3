from Box2D import *

from level import *
from shape import *
from block import *
from paddle import *

class Boundary(b2BoundaryListener):
  """
  Handles all of the boundary events passed in from Box2D.
  """
  def __init__(self, game):
    super(Boundary, self).__init__()
    self.game = game

  def handleCall(self, body):
    obj = body.GetUserData()

    if isinstance(obj, Block):
      obj.handleBoundary()
    # except AttributeError:
      # print("No collision handler found for "+str(other))

  def Violation(self, body):
    self.handleCall(body)

  # def Persist(self, point):
  # 	self.handleCall(ContactTypes.persisted, point)

  # def Remove(self, point):
  # 	self.handleCall(ContactTypes.removed, point)

