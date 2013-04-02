from Box2D import *

from level import *
from shape import *
from block import *
from paddle import *

class Contact(b2ContactListener):
	"""
	Handles all of the contact states passed in from Box2D.
	"""
	def __init__(self, game):
		super(Contact, self).__init__()
		self.game = game

	def handleCall(self, state, point):
		print("Contact!")
		print(point.position)

		if self.test:
			cp          = fwContactPoint()
			cp.shape1   = point.shape1
			cp.shape2   = point.shape2
			cp.position = point.position.copy()
			cp.normal   = point.normal.copy()
			cp.velocity = point.velocity.copy()
			cp.id       = point.id
			cp.state    = state
			self.test.points.append(cp)

	def Add(self, point):
		self.handleCall(Contact.contactAdded, point)
		print("Contact!")

	def Persist(self, point):
		self.handleCall(Contact.contactPersisted, point)
		print("Contact!")

	def Remove(self, point):
		self.handleCall(Contact.contactRemoved, point)
		print("Contact!")

	def Result(self, point):
		# self.handleCall(Contact.contactRemoved, point)
		print("Contact!")
