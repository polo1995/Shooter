#! usr/bin/env python
from math import sqrt
from pygame import Rect
class Circle():
	def __init__(self, x, y, radius):
		self.x = x
		self.y = y
		self.radius = radius
		self.pos = [self.x, self.y]
	def move(self, vector):
		self.x += vector[0]
		self.y += vector[1]
	def collidecircle(self, circle):
		x, y = circle.x-self.x, circle.y-self.y
		distance = sqrt(x**2+y**2)
		if abs(distance) < circle.radius+self.radius:
			return True
		else:
			return False
	@classmethod
	def from_rect(klass, rect):
		x, y = rect.center[0], rect.center[1]
		radius = min([rect.width, rect.height])/2
		return klass(x, y, radius)
	@classmethod
	def from_pos(klass, pos, radius):
		return klass(pos[0], pos[1], radius)
	def rect(self):
		pos = [self.x-self.radius, self.y-self.radius]
		return [pos, [self.radius*2, self.radius*2]]
