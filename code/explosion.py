#! usr/bin/env python
# The Explosion class. We love to see this on-screen!
from util import imgload
from objects import GameObj
import pygame

class Explosion(GameObj):
	# Explosion class, it blits itself to screen
	# Will automatically update its animation
	def __init__(self, pos, small=False):
		pygame.sprite.Sprite.__init__(self)
		if small == True:
			self.imglist = [imgload('smallexplosion1.png'), imgload('smallexplosion2.png'), imgload('smallexplosion3.png')]
		else:
			self.imglist = [imgload('explosion1.png'), imgload('explosion2.png'), imgload('explosion3.png')]
		self.pos = pos
		self.timer = 0
		self.name = 'explosion'
	def update(self, world):
		self.timer += 1
		if self.timer < 4:
			world.blit(self.imglist[0], self.pos)
		elif self.timer > 4 and self.timer < 8:
			world.blit(self.imglist[1], self.pos)
		elif self.timer > 8:
			world.blit(self.imglist[2], self.pos)
		if self.timer > 12:
			world.kill(self)
		return
