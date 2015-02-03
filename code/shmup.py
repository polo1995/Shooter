#! usr/bin/env python

# all the imports
import pygame
from sys import exit, argv
from vectorclass import Vector
from circleclass import Circle
import random
import pickle
import math
import os
from util import *
from ship import *
from objects import *
from aliens import *
from explosion import *

# needed here because this file is where the display is initialized
def imgload(imgfile, colorkey=(255, 255, 255)):
	try:
		img = pygame.image.load(imgfile)
	except pygame.error, error_message:
		raise SystemExit, error_message
	img = img.convert()
	img.set_colorkey(colorkey)
	return img

# Begin defining classes! :)
class AlienUpdater():
	# Calls functions inside alien instances to update movement.
	def __init__(self, path, num, speed, spawntype):
		self.path = path
		self.num = num
		self.numspawned = 0
		self.ids = []
		self.alienspeed = speed
		self.spawntype = spawntype
	def update(self, world):
		if world.timer%20 == 0 and self.numspawned < self.num:
			self.numspawned += 1
			exec(self.spawntype+'(Vector(), self.path[0], world.nextid, self.alienspeed, world)')
			self.ids.append(world.nextid)
			world.advanceId()
		for alien in world.aliens():
			rect = pygame.Rect((0, 0), (1, 1))
			if alien.id in self.ids:
				rect.center = alien.rect.center
				if rect.inflate(alien.speed, alien.speed).collidepoint(self.path[alien.pathindex]):
					if alien.pathindex == len(self.path)-1:
						world.kill(alien)
					else:
						alien.rect.center = self.path[alien.pathindex]
						vector = Vector.from_points(self.path[alien.pathindex], self.path[alien.pathindex+1])
						if list(vector) == [0, 0]:
							vector = Vector(0.1, 0.1)
						alien.newHeading(vector)
						alien.pathindex += 1
				else:
					alien.newHeading(Vector.from_points(alien.rect.center, self.path[alien.pathindex]))
		if self.numspawned == self.num and self.ids == []:
			self.finished = True
		else:
			self.finished = False
		return

class World():
	def __init__(self, level, screen):
		self.screen = screen
		self.entities = pygame.sprite.Group()
		self.timer = 0
		self.height = self.screen.get_height()
		self.width = self.screen.get_width()
		self.clock = pygame.time.Clock()
		if pygame.mixer:
			self.sounds = loadSounds()
		self.level = level
		self.levelupdaters = []
		self.leveltimer = Timer()
		self.levelindex = 0
		self.nextid = 0
		self.score = 0
		self.score_multiplier = 1
		self.font = pygame.font.SysFont(None, 20)
		self.alienskilled = 0
		self.aliens_hit_without_dying = 0
		self.multiplier_cutoff = 9
		self.maxentities = 0
		self.ship = Ship(self)
		self.nextupgrade = 70
	def add(self, sprites):
		self.entities.add(sprites)
		return
	def kill(self, sprites):
		if hasattr(sprites, '__iter__'):
			for i in sprites:
				if i.name == 'alien':
					for updater in self.levelupdaters:
						if i.id in updater.ids:
							updater.ids.remove(i.id)
		else:
			if sprites.name == 'alien':
				for updater in self.levelupdaters:
					if sprites.id in updater.ids:
						updater.ids.remove(sprites.id)
		self.entities.remove(sprites)
		return
	def play(self, soundname):
		try:
			self.sounds[soundname].play()
		except:
			pass
		return
	def update(self, timepass):
		self.timer += 1
		self.checkStars()
		self.checkLevel(timepass)
		self.ship.update(self)
		self.entities.update(self)
		self.drawScore()
		return
	def drawScore(self):
		score = self.font.render(str(self.score), True, [250, 250, 250])
		self.blit(score, [0, 0])
		multiplier = self.font.render(('x' + str(self.score_multiplier)), True, [250, 250, 250])
		self.blit(multiplier, [0, multiplier.get_height()])
		return
	def shipbullets(self):
		group = pygame.sprite.Group()
		for i in self.entities:
			if i.name == 'shipbullet':
				group.add(i)
		return group
	def alienbullets(self):
		group = pygame.sprite.Group()
		for i in self.entities:
			if i.name == 'alienbullet':
				group.add(i)
		return group
	def aliens(self):
		group = pygame.sprite.Group()
		for i in self.entities:
			if i.name == 'alien':
				group.add(i)
		return group
	def getship(self):
		return self.ship
	def things(self, name):
		group = pygame.sprite.Group()
		for i in self.entities:
			if i.name == name:
				group.add(i)
		return group
	def resetMultiplier(self):
		self.score_multiplier -= 2
		if self.score_multiplier <= 0:
			self.score_multiplier = 1
		self.aliens_hit_without_dying = 0
	def explosion(self, pos):
		self.add(Explosion(pos))
		return
	def checkStars(self):
		if self.timer%5 == 0:
			self.add(Star([random.randint(0, self.width), 0], [0, random.randint(7, 20)]))
	def checkLevel(self, timepass):
		self.leveltimer.update(timepass)
		if self.leveltimer.finished == True:
			if self.levelindex < len(self.level):
				i = self.level[self.levelindex]
				self.wave(i[1], int(i[0]), i[3], i[4])
				self.levelindex += 1
				self.leveltimer = Timer(i[2])
		else:
			if self.levelupdaters == []:
				self.leveltimer = Timer()
		for alienupdater in self.levelupdaters:
			alienupdater.update(self)
			if alienupdater.finished == True:
				self.levelupdaters.remove(alienupdater)
		return
	def advanceId(self):
		self.nextid += 1
	def wave(self, path, aliens, alienspeed, spawntype):
		self.levelupdaters.append(AlienUpdater(path, aliens, alienspeed, spawntype))
	def blit(self, img, pos):
		self.screen.blit(img, pos)
		return
	def blit(self, img, rect):
		self.screen.blit(img, rect)
		return
	def scoreAlien(self, alien):
		global gunupgrade
		self.alienskilled += 1
		self.aliens_hit_without_dying += 1
		if self.aliens_hit_without_dying >= self.multiplier_cutoff:
			self.score_multiplier += 1
			self.aliens_hit_without_dying = 0
		self.score += alien.worth*self.score_multiplier
		if self.score > self.nextupgrade:
			self.getship().gun.upgrade()
			self.nextupgrade = self.score+1000*self.score_multiplier
			self.play('gunupgrade')
		return

def menu(position, options, screen):
	clock = pygame.time.Clock()
	font = pygame.font.Font(pygame.font.get_default_font(), 32)
	text = []
	for i in options:
		text.append(font.render(str(i), True, [200, 200, 0]))
	rects = []
	startpos = position[:]
	for i in text:
		rects.append(pygame.Rect(startpos, (i.get_width(), i.get_height())))
		startpos[1] += 32
	cursor = 0
	menurect = pygame.Rect(position, (rects[-1].right-rects[0].left, rects[-1].bottom-rects[0].top))
	while True:
		for e in pygame.event.get():
			if e.type == pygame.K_ESCAPE:
				return
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_UP:
					cursor += 1
					if cursor > len(text)-1:
						cursor = 0
				elif e.key == pygame.K_DOWN:
					cursor -= 1
					if cursor < 0:
						cursor = len(text)-1
				elif e.key == pygame.K_RETURN:
					return options[cursor]
		pygame.draw.rect(screen, [0, 255, 0], menurect)
		pygame.draw.rect(screen, [255, 255, 0], menurect, 1)
		for i in text:
			if text.index(i) == cursor:
				pygame.draw.rect(screen, [0, 255, 0], rects[text.index(i)])
			screen.blit(i, rects[text.index(i)])
		pygame.display.flip()
		clock.tick(10)

def loadLevel(path, screen):
	world = World(path, screen)
	return world

def main():
	global BLACK, FPS
	pygame.init()
	screen = pygame.display.set_mode([480, 640], pygame.DOUBLEBUF)
	path = open('./levels/Level2.txt', 'r')
	data = pickle.load(path)
	path.close()
	world = loadLevel(data, screen)
	# Main loop
	while True:
		# Get input and set flags.
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					pygame.quit()
					exit()
				elif e.key == pygame.K_p:
					while True:
						e = pygame.event.wait()
						if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
							break
		# Clear the screen
		screen.fill(BLACK)
		# Update ship, aliens, and bullets.
		# Also cap the framerate at 35 fps and make everything runs at the same speed
		timepass=world.clock.tick(FPS)/1000.
		pygame.display.set_caption('shmup'+'	FPS: '+str(timepass*1000.))
		pygame.draw.circle(screen, [255, 255, 255], pygame.mouse.get_pos(), 2)
		world.update(timepass)
		# Update display
		pygame.display.flip()
	return
if __name__ == '__main__':
	main()
