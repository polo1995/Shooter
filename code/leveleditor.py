#! usr/bin/env python

import pygame, sys, os, pickle, random
from pygame.locals import *
from vectorclass import Vector
from circleclass import Circle
from sys import argv
pygame.init()
screen = pygame.display.set_mode([480, 640])
screen.fill([0, 0, 0])
if len(argv) > 1:
	editfile = open(argv[1], 'r')
	path = pickle.load(editfile)
	editfile.close()
else:
	path = []
clock = pygame.time.Clock()
held_down = False
currentedit = 0
font = pygame.font.Font(None, 22)
controlpoints = []
rect = screen.get_rect()
controlpoints.extend((rect.topleft, rect.midtop, rect.topright))
controlpoints.extend((rect.midleft, rect.center, rect.midright))
controlpoints.extend((rect.bottomleft, rect.midbottom, rect.bottomright))
smallrect = rect.inflate(-rect.width/3, -rect.height/3)
smallrect.center = rect.center
controlpoints.extend((smallrect.topleft, smallrect.midtop, smallrect.topright))
controlpoints.extend((smallrect.midleft, smallrect.center, smallrect.midright))
controlpoints.extend((smallrect.bottomleft, smallrect.midbottom, smallrect.bottomright))
def dialog(name):
	global screen, clock, font
	text = ''
	while True:
		e = pygame.event.poll()
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_BACKSPACE:
				if len(text) > 0:
					text = text[:-1]
			elif e.key == pygame.K_RETURN:
				return text
			else:
				text = text+e.unicode
		screen.fill([0, 0, 0])
		screen.blit(font.render(str(name), True, [255, 255, 255]), [100, 170])
		screen.blit(font.render(text, True, [255, 255, 255], [0, 100, 50]), [200, 200])
		clock.tick(30)
		pygame.display.flip()
class Timer():
	def __init__(self, seconds=0):
		self.seconds = seconds
		self.finished = False
	def update(self, framerate):
		self.seconds -= framerate
		if self.seconds <= 0:
			self.finished = True
		else:
			self.finished = False
class SoCalledAlien(pygame.sprite.Sprite):
	def __init__(self, heading, position, id, speed):
		pygame.sprite.Sprite.__init__(self)
		self.heading = heading
		self.rect = pygame.Rect((0, 0), (20, 20))
		self.rect.center = position
		self.id = id
		self.speed = speed
		self.pathindex = 0
	def update(self):
		global screen
		self.rect = self.rect.move(list(self.heading*self.speed))
		pygame.draw.rect(screen, [255, 0, 0], self.rect)
		return
	def newHeading(self, heading):
		self.heading = heading
		self.heading.normalize()
class AlienUpdater():
	# Calls functions inside alien instances to update movement.
	def __init__(self, path, num, speed):
		self.path = path
		self.num = num
		self.numspawned = 0
		self.ids = []
		self.alienspeed = speed
	def update(self, world):
		if world.timer%20 == 0 and self.numspawned < self.num:
			self.numspawned += 1
			alien = SoCalledAlien(Vector(), self.path[0], world.nextid, self.alienspeed)
			world.add(SoCalledAlien(Vector(), self.path[0], world.nextid, self.alienspeed))
			self.ids.append(world.nextid)
			world.advanceId()
		for alien in world.aliens():
			rect = pygame.Rect((0, 0), (1, 1))
			if alien.id in self.ids:
				rect.center = alien.rect.center
				if rect.inflate(alien.speed, alien.speed).collidepoint(self.path[alien.pathindex]):
					if alien.pathindex == len(self.path)-1:
						world.kill(alien)
						world.resetMultiplier()
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
class FakeWorld():
	def __init__(self, path):
		self.nextid = 0
		self.group = pygame.sprite.Group()
		self.leveltimer = Timer()
		self.level = path
		self.levelupdaters = []
		self.levelindex = 0
		self.timer = 0
	def resetMultiplier(self):
		pass
	def kill(self, things):
		self.group.remove(things)
	def add(self, things):
		self.group.add(things)
	def aliens(self):
		return self.group
	def wave(self, path, aliens, alienspeed, spawntype):
		self.levelupdaters.append(AlienUpdater(path, aliens, alienspeed, spawntype))
	def update(self, timepass):
		self.timer += 1
		self.leveltimer.update(timepass)
		if self.leveltimer.finished == True:
			if self.levelindex < len(self.level):
				i = self.level[self.levelindex]
				self.wave(i[1], int(i[0]), i[3])
				self.levelindex += 1
				self.leveltimer = Timer(i[2])
		for alienupdater in self.levelupdaters:
			alienupdater.update(self)
			if alienupdater.finished == True:
				self.levelupdaters.remove(alienupdater)
		self.group.update()
		return
	def advanceId(self):
		self.nextid += 1
	def wave(self, path, aliens, alienspeed):
		self.levelupdaters.append(AlienUpdater(path, aliens, alienspeed))
def display(path):
	global screen, currentlinecolor
	world = FakeWorld(path)
	print len(path)
	while True:
		screen.fill([0, 0, 0])
		for i in path:
			if len(i[1]) > 1:
				startpos = i[1][0]
				for pos in i[1]:
					pygame.draw.aaline(screen, [230, 230, 230], startpos, pos)
					startpos = pos[:]
		e = pygame.event.poll()
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_BACKSPACE:
				return
		timepass = clock.tick(30)/1000.
		world.update(timepass)
		pygame.display.flip()
	return
def findDistance(p1, p2):
	x, y = p1[0]-p2[0], p1[1]-p2[1]
	distance = sqrt(x**2 + y**2)
	return distance
while True:
	screen.fill([0, 0, 0])
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif e.type == pygame.MOUSEMOTION:
			mousebuttons = pygame.mouse.get_pressed()
			if mousebuttons[0]:
				try:
					for i in controlpoints:
						if Circle(pos[0], pos[1], 2).collidecircle(Circle(i[0], i[1], 4)) == True:
							pos = i
							path[currentedit][1].append(pos)
						else:
							if controlpoints.index(i)+1 == len(controlpoints):
								pos = (int(pos[0]), int(pos[1]))
								path[currentedit][1].append(pos)
				except: pass
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			elif e.key == pygame.K_c:
				path = []
			elif e.key == pygame.K_BACKSPACE:
				if len(path) > 0:
					path.remove(path[currentedit])
				if currentedit == len(path):
					currentedit = len(path)-1
			elif e.key == pygame.K_s:
				name = dialog('Name of path?')
				try:
					savefile = open(name, 'w')
					pickle.dump(path, savefile)
					savefile.close()
				except: pass
			elif e.key == pygame.K_n:
				path.append(['', [], 0, 0., ''])
				currentedit = len(path)-1
			elif e.key == pygame.K_a:
				num = dialog('How many aliens?')
				try:
					path[currentedit][0] = str(num)
				except:
					pass
			elif e.key == pygame.K_d:
				num = dialog('Time till next wave?')
				try:
					path[currentedit][2] = int(num)
				except: pass
			elif e.key == pygame.K_v:
				num = dialog('What\'s the speed of the aliens?')
				try:
					path[currentedit][3] = float(num)
				except: pass
			elif e.key == pygame.K_SPACE:
				pos = pygame.mouse.get_pos()
				try:
					for i in controlpoints:
						print Circle(pos[0], pos[1], 2).collidecircle(Circle(i[0], i[1], 4))
						if Circle(pos[0], pos[1], 2).collidecircle(Circle(i[0], i[1], 4)) == True:
							pos = i
							path[currentedit][1].append(pos)
							break
						else:
							if controlpoints.index(i)+1 == len(controlpoints):
								pos = (int(pos[0]), int(pos[1]))
								path[currentedit][1].append(pos)
				except: pass
			elif e.key == pygame.K_t:
				name = dialog('What type of aliens are they?')
				path[currentedit][4] = name
			elif e.key == pygame.K_p:
				print path
			elif e.key == pygame.K_RETURN:
				display(path)
			elif e.key == pygame.K_e:
				try:
					currentedit = int(dialog('Which path to edit?'))-1
					if currentedit > len(path)-1:
						currentedit = len(path)-1
				except: pass
	for i in controlpoints:
		pygame.draw.circle(screen, [255, 255, 0], i, 3)
	for i in path:
		if len(i[1]) > 1:
			startpos = i[1][0]
			for pos in i[1]:
				if path.index(i) == currentedit:
					pygame.draw.aaline(screen, [255, 0, 0], startpos, pos)
				else:
					pygame.draw.aaline(screen, [230, 230, 230], startpos, pos)
				startpos = pos[:]
	if len(path) > 0:
		text = ('Num: '+path[currentedit][0]+' '+'Speed: '+str(path[currentedit][3])+' '+'Type: '+path[currentedit][4]+' '+'LengthTime: '+str(path[currentedit][2]))
		textsurf = font.render(text, True, [100, 100, 100])
		screen.blit(textsurf, [0, 0])
	pygame.display.flip()
	clock.tick(4)
