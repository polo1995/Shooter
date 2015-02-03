#! usr/bin/env python
# The Bullet class definition. This is where the fun happens
from circleclass import Circle
from util import imgload, loadBulletImages
from objects import GameObj
import pygame

bulletimages = loadBulletImages()
class Bullet(GameObj):
	# Bullet class. Updates and blits itself to screen.
	def __init__(self, pos, speed, img, name, rotate=False):
		global bulletimages
		pygame.sprite.Sprite.__init__(self)
		self.rect = bulletimages[img].get_bounding_rect()
		self.rect.midbottom = pos
		self.rect.centery = pos[1]
		self.speed = speed
		self.name = name
		self.img = img
		self.timer = 0
		self.rotate = rotate
	def update(self, world):
	        global bulletimgdict
		self.rect = self.rect.move(self.speed)
		if self.rect.bottom < 0 or self.rect.top > world.height or self.rect.left > world.width or self.rect.right < 0:
			world.kill(self)
		if self.rotate:
			rotateimg = pygame.transform.rotate(bulletimages[self.img], self.timer)
			blitlocation = (self.rect.centerx - rotateimg.get_width()/2, self.rect.centery-rotateimg.get_height()/2)
			world.blit(rotateimg, blitlocation)
		else:
			world.blit(bulletimages[self.img], self.rect)
		#pygame.draw.rect(world.screen, [255, 255, 255], self.rect, 1)
		#pygame.draw.circle(world.screen, [255, 255, 255], Circle.from_rect(self.rect).pos, min(self.rect.width, self.rect.height)/2, 1)
		self.timer += 20
		if self.timer > 360:
			self.timer = 0
		return
	def circlecollide(self, circle):
		return Circle.from_rect(self.rect).collidecircle(circle)
