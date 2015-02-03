#! usr/bin/env python
# All Weapon definitions
from vectorclass import Vector
from circleclass import Circle
from bullet import *
from util import imgload

# Default class. Don't create instances of this directly
class Weapon(object):
	def __init__(self, ship):
		self.upgrades = 6
		self.ship = ship
	def upgrade(self):
		self.upgrades += 1
	def fire(self, *args):
		pass
	def update(self, *args):
		pass

# If you're bored turn this on. :)
class Shotgun(Weapon):
	def fire(self, world):
		bullets = []
		bullets.append(Bullet(self.ship.rect.midtop, [random.randint(1, 8), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midtop, [random.randint(1, 8), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midleft, [random.randint(-8, -1), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midleft, [random.randint(-8, -1), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midright, [random.randint(1, 8), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midright, [random.randint(1, 8), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.bottomleft, [random.randint(-8, -1), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.bottomleft, [random.randint(-8, -1), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midbottom, [random.randint(1, 8), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midbottom, [random.randint(1, 8), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midleft, [random.randint(-8, -1), -23], 'shotgunbullet.png', 'shipbullet'))
		bullets.append(Bullet(self.ship.rect.midright, [random.randint(-8, -1), -23], 'shotgunbullet.png', 'shipbullet'))
		world.add(bullets)
		self.ship.stats['shoot_timer'] = self.ship.base_stats['shoot_timer']
		return

# Default weapon
class Spread(Weapon):
	def fire(self, world):
		bullets = []
		if self.upgrades >= 1:
			bullets.append(Bullet(self.ship.rect.topright, [1, -24], 'geometrybullet.png', 'shipbullet'))
			bullets.append(Bullet(self.ship.rect.topleft, [-1, -24], 'geometrybullet.png', 'shipbullet'))
			bullets.append(Bullet(self.ship.rect.midtop, [0, -25], 'geometrybullet.png', 'shipbullet'))
		if self.upgrades >= 2:
			bullets.append(Bullet(self.ship.rect.topright, [2, -23], 'geometrybullet.png', 'shipbullet'))
			bullets.append(Bullet(self.ship.rect.topleft, [-2, -23], 'geometrybullet.png', 'shipbullet'))
		if self.upgrades >= 3:
			bullets.append(Bullet(self.ship.rect.topright, [3, -22], 'bullet.png', 'shipbullet'))
			bullets.append(Bullet(self.ship.rect.topleft, [-3, -22], 'bullet.png', 'shipbullet'))
		if self.upgrades >= 4:
			bullets.append(Bullet(self.ship.rect.topright, [4, -21], 'bullet.png', 'shipbullet'))
			bullets.append(Bullet(self.ship.rect.topleft, [-4, -21], 'bullet.png', 'shipbullet'))
		if self.upgrades >= 5:
			bullets.append(Bullet(self.ship.rect.topleft, [0, -30], 'pistolbullet.png', 'shipbullet'))
			bullets.append(Bullet(self.ship.rect.topright, [0, -30], 'pistolbullet.png', 'shipbullet'))
		if self.upgrades >= 6:
			aliens = world.aliens()
			if len(aliens) > 0:
				heading = Vector.from_points(self.ship.rect.center, aliens.sprites()[0].rect.center)
				heading.normalize()
				heading = heading*25.
				bullets.append(Bullet(self.ship.rect.midtop, list(heading), 'shurikenbullet.png', 'shipbullet', True))
			else:
				bullets.append(Bullet(self.ship.rect.midbottom, [0, 25], 'shurikenbullet.png', 'shipbullet', True))
		if self.upgrades >= 7:
			self.ship.base_stats['shoot_timer'] -= 1
			self.upgrades = 6
			if self.ship.base_stats['shoot_timer'] < 0:
				world.score += 2000
		world.add(bullets)
		return
