#! usr/bin/env python
# The Ship definition, aka the player character
from objects import GameObj
from constants import *
from vectorclass import Vector
from circleclass import Circle
from weapons import *
from bullet import *
from util import imgload

class Ship(GameObj):
	# The player character.
	# He can move himself, and blit himself to the main display surface.
	# Functions include:
	# __init__(self, speed=700.0, shoot_timer=2, hp=100):
	#	Creates a new player character, ready to use.
	# update(self):
	#	Calls all other functions needed to use the player.
	# draw(self):
	#	Draws the player character's image to the main display surface, at the middle of his location.
	# updatePowerups(self):
	#	Nothing yet.
	# checkWalls(self):
	#	Prevents the player character from going out of the screen.
	# doMovement(self):
	#	Updates the player's rect to the new location, using his vector.
	# checkMovement(self):
	#	Determines what control scheme is wanted, and updates the player's vector accordingly.
	def __init__(self, world, speed=15.0, shoot_timer=4, lives=3):
		pygame.sprite.Sprite.__init__(self)
		self.images = self.loadImages()
		self.rect = self.images['normal'][0].get_bounding_rect()
		self.xinf = XINFLATION
		self.yinf = YINFLATION
		self.rect = self.rect.inflate(self.xinf, self.yinf)
		self.speed = speed
		self.shoot_timer = 0
		self.base_stats={'speed':speed, 'shoot_timer':shoot_timer, 'lives':lives}
		self.stats = {'speed':speed, 'shoot_timer':shoot_timer, 'lives':lives}
		self.moving = False
		self.movingdirection = None
		self.vector = Vector()
		self.weapons = 1
		self.name = 'ship'
		self.respawntimer = 0
		self.respawning = False
		self.invincible = False
		self.rect.midbottom = [world.width/2, world.height]
		self.gun = Spread(self)
	def loadImages(self):
		images = {'normal':[imgload('falconship.png'), imgload('falconship1.png')],
		'right':[imgload('falconshipright.png'), imgload('falconshipright1.png')],
		'left':[imgload('falconshipleft.png'), imgload('falconshipleft1.png')]}
		return images
	# Calls all needed methods for homeostasis in the ship ;)
	def update(self, world):
		self.checkRespawnTimer()
		if self.respawning == False:
			self.updateShootTimer()
			self.updateMovement(world)
			self.checkWalls(world)
			if self.invincible == True:
				if world.timer%5 == 0:
					self.draw(world)
			else:
				self.draw(world)
			self.checkHit(world)
		return
	# Updates the player's shootingtimer
	def updateShootTimer(self):
		if self.stats['shoot_timer'] > 0:
			self.stats['shoot_timer'] -= 1
		return
	# Checks to make sure the respawn timer is in order
	def checkRespawnTimer(self):
		if self.respawntimer > 0:
			self.respawntimer -= 1
		if self.respawntimer > 0 and self.respawntimer < 30:
			self.respawning = False
			self.invincible = True
		else:
			self.invincible = False
		return
	# Checks for harmful collisions against aliens and/or bullets
	def checkHit(self, world):
		self.checkBulletCollisions(world)
		self.checkAlienCollisions(world)
		return
	# Checks for bullet collisions
	def checkBulletCollisions(self, world):
		alienbullets = world.alienbullets()
		collide = pygame.sprite.spritecollideany(self, alienbullets)
		circle = Circle.from_rect(self.rect)
		circle.radius = 4
		circle.y -= 5
		if collide != None and self.invincible == False:
			if collide.circlecollide(circle) == True:
				self.gotHurt(world)
				world.kill(collide)
		return
	# Checks for alien collisions
	def checkAlienCollisions(self, world):
		aliens = world.aliens()
		collide = pygame.sprite.spritecollideany(self, aliens)
		if collide != None and self.invincible == False:
			self.gotHurt(world)
			world.kill(collide)
		return
	# Resets all the needed variables after a harmful collision
	def gotHurt(self, world):
		world.play('shiphit')
		world.resetMultiplier()
		world.explosion(self.rect.move(self.xinf/2, self.yinf/2).topleft)
		self.stats['lives'] -= 1
		self.rect.midbottom = [world.width/2, world.height]
		self.respawning = True
		self.respawntimer = 60
		return
	# Draws the player to the screen.
	def draw(self, world):
		if self.movingdirection == 'right':
			img = self.images['right'][world.timer%len(self.images['right'])]
		elif self.movingdirection == 'left':
			img = self.images['left'][world.timer%len(self.images['left'])]
		else:
			img = self.images['normal'][world.timer%len(self.images['normal'])]
		world.blit(img, self.rect.inflate(-self.xinf+1, -self.yinf+1))
		return
	# Checks to see if the player is trying to go off the screen! :)
	def checkWalls(self, world):
		if self.rect.right > world.width:
			self.rect.right = world.width
		elif self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > world.height:
			self.rect.bottom = world.height
		return
	# Checks to see which control mechanism is in use and calls the appriopriate methods
	def updateMovement(self, world):
		global CONTROL
		keys = pygame.key.get_pressed()
		if CONTROL == 'keyboard':
			self.checkKeyboardControl(keys)
		elif CONTROL == 'mouse':
			self.checkMouseControl()
		self.checkSpecialKeys(keys, world)
		return
	# Checks to see if any other keys are pressed, and updates needed variables
	def checkSpecialKeys(self, keys, world):
		global SLOWKEY, SHOOTKEY
		if keys[SLOWKEY]:
			self.speed = self.base_stats['speed']/3
		else:
			self.speed = self.base_stats['speed']
		if keys[SHOOTKEY] or pygame.mouse.get_pressed()[0]:
			if self.stats['shoot_timer'] <= 0:
				world.play('laser1')
				self.gun.fire(world)
				self.stats['shoot_timer'] = self.base_stats['shoot_timer']
		return
	# Chekcs for keyboard presses and updates player's position accordingly
	def checkKeyboardControl(self, keys):
		global UPKEY, RIGHTKEY, LEFTKEY, DOWNKEY
		self.vector = Vector(0, 0)
		if keys[UPKEY]:
			self.vector.y = -1
		elif keys[DOWNKEY]:
			self.vector.y = 1
		if keys[RIGHTKEY]:
			self.vector.x = 1
			self.movingdirection = 'right'
		elif keys[LEFTKEY]:
			self.vector.x = -1
			self.movingdirection = 'left'
		else:
			self.movingdirection = None
		if list(self.vector) != [0, 0]:
			self.vector.normalize()
			self.vector = self.vector*self.speed
			self.rect = self.rect.move(tuple(self.vector))
		return
	# Checks for mouse movement and updates player's position accordingly
	def checkMouseControl(self):
		rect = pygame.Rect((0, 0), (self.speed*1.3, self.speed*1.3))
		rect.center = self.rect.center
		x, y = pygame.mouse.get_pos()
		collide = rect.collidepoint((x, y))
		if collide:
			self.moving=False
			self.rect.center = (x, y)
			self.movingdirection = None
		else:
			self.moving = True
			if x > self.rect.centerx:
				self.movingdirection = 'right'
			elif x < self.rect.centerx:
				self.movingdirection = 'left'
		if self.moving == True:
			heading = Vector.from_points(self.rect.center, [x, y])
			heading.normalize()
			self.vector = heading*self.speed
			tuplevector = tuple(self.vector)
			self.rect = self.rect.move(tuplevector)
		return
