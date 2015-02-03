#! usr/bin/env python
# All the definitions for aliens.
from objects import GameObj
from constants import *
from vectorclass import Vector
from circleclass import Circle
from bullet import *
from util import *
from explosion import *

# Base Alien class. You can create instances of this directly for a generic 'aimer' type alien,
# or create your own custom alien.
class Alien(GameObj):
	def __init__(self, heading, pos, id, speed, world):
		pygame.sprite.Sprite.__init__(self)
		self.images = self.loadAnimations()
		self.rect = self.images[0].get_bounding_rect()
		self.rect.center = pos
		self.heading = heading
		self.speed = speed
		self.pathindex = 0
		self.name = 'alien'
		self.id = id
		self.fireframe = self.setFireframe()
		self.hp = self.setHP()
		self.worth = self.setWorth()
		world.add(self)
	def loadAnimations(self):
		return [imgload('alien.png'), imgload('alien2.png')]
	def setFireframe(self):
		return 30
	def setWorth(self):
		return 10
	def update(self, world):
		move = self.heading*self.speed
		self.rect = self.rect.move(list(move))
		world.blit(self.images[world.timer%len(self.images)], self.rect)
		bullets = world.shipbullets()
		collide = pygame.sprite.spritecollide(self, bullets, False)
		if len(collide) > 0:
			self.hurt(collide, world)
			for i in collide:
				world.add(Explosion(i.rect.center, True))
		if world.timer%self.fireframe == 0:
			self.fire(world)
		return
	def newHeading(self, vector):
		self.heading = vector
		if not self.heading.get_mag() == 0:
			self.heading.normalize()
		return
	def fire(self, world):
		ship = world.getship()
		heading = Vector.from_points(self.rect.midbottom, ship.rect.center)
		if heading.get_mag() > 40:
			world.play('alienshoot')
			heading.normalize()
			heading = heading*5.
			world.add(Bullet(self.rect.midbottom, list(heading), 'alienbullet.png', 'alienbullet'))
		return
	def hurt(self, collide, world):
		self.hp -= len(collide)
		world.play('alienhit')
		world.kill(collide)
		if self.hp <= 0:
			world.explosion(self.rect.topleft)
			world.kill(self)
			world.play('explosion')
			world.scoreAlien(self)
		return
	def setHP(self):
		return 2

# This alien will shoot bullets in a ring around it.
class CircleStrafer(Alien):
	def setWorth(self):
		return 20
	def setHP(self):
		self.bulletmove = 1
		return 5
	def setFireframe(self):
		return 10
	def fire(self, world):
		global alienshoot
		bullets = []
		self.bulletmove += 1
		if self.bulletmove%2 == 0:
			for i in range(-30, 30, 3):
				speed = getHeadingFromAngle(i)*10.
				location = [self.rect.centerx+i, self.rect.centery]
				bullets.append(Bullet(location, list(speed), 'alienbullet5.png', 'alienbullet', True))
				world.add(bullets)
		else:
			for i in range(33, -33, -6):
				speed = getHeadingFromAngle(i)*12.
				location = [self.rect.centerx+i, self.rect.centery]
				bullets.append(Bullet(location, list(speed), 'alienbullet5.png', 'alienbullet', True))
				world.add(bullets)
		return

# This is a giant bee alien that shoots bullets in a ring around it. Nasty!
class GiantKiller(Alien):
	def setWorth(self):
		return 12
	def setHP(self):
		return 2
	def loadAnimations(self):
		return [imgload('alienbee.png')] 
	def fire(self, world):
		global alienshoot
		ship = world.getship()
		if Vector.from_points(self.rect.center, ship.rect.center).get_mag() > 40:
			world.play('alienshoot')
			bullets = []
			for i in range(1, 11):
				heading = getHeadingFromAngle(i*36)
				heading = heading*10.
				bullets.append(Bullet(self.rect.midbottom, list(heading), 'alienbullet3.png', 'alienbullet'))
			world.add(bullets)
		return

# This alien is like a HeadingStrafer on steriods.
class ArmoredVulcan(Alien):
	def setFireframe(self):
		return 11
	def setWorth(self):
		return 15
	def setHP(self):
		return 15
	def loadAnimations(self):
		return [imgload('alienthing.png')]
	def fire(self, world):
		global alienshoot
		ship = world.getship()
		if Vector.from_points(self.rect.center, ship.rect.center).get_mag() > 120:
			world.play('alienshoot')
			bullets = []
			for i in range(-6, 6):
				speed = getHeadingFromAngle(i*3.6)*10
				bullets.append(Bullet(self.rect.center, list(speed), 'alienbullet3.png', 'alienbullet'))
			world.add(bullets)
		return

# This alien shoots bullets in whatever direction its moving. Has a moderate amount of HP
class HeadingStrafer(Alien):
	def setWorth(self):
		return 11
	def setHP(self):
		return 4
	def loadAnimations(self):
		return [imgload('alienthing.png')]
	def fire(self, world):
		global alienshoot
		ship = world.getship()
		if Vector.from_points(self.rect.center, ship.rect.center).get_mag() > 40:
			world.play('alienshoot')
			bullets = []
			heading1 = getHeadingFromAngle(40)
			heading2 = getHeadingFromAngle(-40)
			bullets.append(Bullet(self.rect.midbottom, list(self.heading*10.), 'alienbullet.png', 'alienbullet'))
			bullets.append(Bullet(self.rect.midbottom, list(heading1*10.), 'alienbullet.png', 'alienbullet'))
			bullets.append(Bullet(self.rect.midbottom, list(heading2*10.), 'alienbullet.png', 'alienbullet'))
			world.add(bullets)
		return

# This alien is a giant bee with a TON of HP. Shoots bullets in a ring around it.
class GiantKillerTwo(Alien):
	def setWorth(self):
		return 20
	def setHP(self):
		return 10
	def loadAnimations(self):
		return [imgload('alienbee.png')] 
	def fire(self, world):
		global alienshoot
		ship = world.getship()
		if Vector.from_points(self.rect.center, ship.rect.center).get_mag() > 40:
			world.play('alienshoot')
			bullets = []
			for i in range(1, 11):
				heading = getHeadingFromAngle(i*36)
				heading = heading*10.
				bullets.append(Bullet(self.rect.midbottom, list(heading), 'alienbullet3.png', 'alienbullet', True))
			world.add(bullets)
		return

# This alien will shoot slow-moving bullets at the player. Not very powerful
class WeakAimer(Alien):
	def setHP(self):
		return 1
	def setFireframe(self):
		return 50
	def setWorth(self):
		return 6

# This alien is just cannon fodder. Fun to shoot! :)
class LevelOneFrag(Alien):
	def setHP(self):
		return 1
	def fire(self, world):
		return
	def loadAnimations(self):
		return [imgload('dumbalien.png'), imgload('dumbalien1.png'), imgload('dumbalien2.png'), imgload('dumbalien3.png')]
	def setWorth(self):
		return 3

# This alien shoots six fast-moving diamonds at the player.
class LongshotAimer(Alien):
	def setHP(self):
		return 7
	def setWorth(self):
		return 20
	def setFireframe(self):
		return 30
	def fire(self, world):
		world.play('alienshoot')
		bullets=[]
		ship = world.getship()
		vector = Vector.from_points(self.rect.center, ship.rect.center)
		vector.normalize()
		for i in range(1, 6):
			speed = list(vector*i*5.)
			bullets.append(Bullet(self.rect.center, speed, 'alienbullet4.png', 'alienbullet', True))
		world.add(bullets) 
		return

