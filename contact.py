from Box2D import *

from level import *
from shape import *
from block import *
from paddle import *

class ContactTypes:
  """
  Acts as an enum, holding the types necessary for contacts:
  Added, persisted, and removed
  """
  unknown = 0
  added = 1
  persisted = 2
  removed = 3

class ContactPoint:
  """
  Structure holding the necessary information for a contact point.
  All of the information is copied from the contact listener callbacks.
  """
  shape1 = None
  shape2 = None
  other = None
  normal = None
  position = None
  velocity = None
  id  = None
  state = 0

class Contact(b2ContactListener):
  """
  Handles all of the contact states passed in from Box2D.
  """
  def __init__(self, game):
    super(Contact, self).__init__()
    self.game = game

  def handleCall(self, state, point):
    ball = self.game.ball
    paddle = self.game.paddle
    obj1 = point.shape1.GetUserData()
    obj2 = point.shape2.GetUserData()

    cp          = ContactPoint()
    cp.shape1   = point.shape1
    cp.shape2   = point.shape2
    cp.position = point.position.copy()
    cp.normal   = point.normal.copy()
    cp.velocity = point.velocity.copy()
    cp.id       = point.id
    cp.state    = state

    # Does the event involve the ball?
    if obj1 is ball or obj2 is ball:
      this  = obj2 if obj2 is ball else obj1
      other = obj2 if obj1 is ball else obj1
      cp.this  = this
      cp.other = other

      # Try to notify the other object.
      # try:
      if isinstance(other, Block):
        other.handleCollision(cp)
      # except AttributeError:
        # print("No collision handler found for "+str(other))
    elif obj1 is paddle or obj2 is paddle:
      this  = obj2 if obj2 is paddle else obj1
      other = obj2 if obj1 is paddle else obj1
      cp.this  = this
      cp.other = other

      if isinstance(other, Block):
        other.handleCollision(cp)

  def Add(self, point):
    self.handleCall(ContactTypes.added, point)

  # def Persist(self, point):
  # 	self.handleCall(ContactTypes.persisted, point)

  # def Remove(self, point):
  # 	self.handleCall(ContactTypes.removed, point)
