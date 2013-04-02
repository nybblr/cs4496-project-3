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
	normal = None
	position = None
	velocity = None
	id  = None
	state = 0

class Contact(b2ContactListener):
	"""
	Handles all of the contact states passed in from Box2D.
	"""
	test = None
	def __init__(self, game):
		super(Contact, self).__init__()
		self.game = game

	def handleCall(self, state, point):
		# print(point.position)
		if self.test:
			cp          = ContactPoint()
			cp.shape1   = point.shape1
			cp.shape2   = point.shape2
			cp.position = point.position.copy()
			cp.normal   = point.normal.copy()
			cp.velocity = point.velocity.copy()
			cp.id       = point.id
			cp.state    = state
			self.test.points.append(cp)

	def Add(self, point):
		self.handleCall(ContactTypes.added, point)

	# def Persist(self, point):
	# 	self.handleCall(ContactTypes.persisted, point)

	# def Remove(self, point):
	# 	self.handleCall(ContactTypes.removed, point)
