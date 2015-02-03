#! usr/bin/env python
# Just some helper functions and classes
from math import sin, cos, atan2
import pygame, os
from vectorclass import Vector
from circleclass import Circle

"""bulletimgdict = {'pistolbullet.png':imgload('pistolbullet.png'), 'alienbullet.png':imgload('alienbullet.png'), 'alienbullet2.png':imgload('alienbullet2.png'),\
'bullet.png':imgload('bullet.png'), 'geometrybullet.png':imgload('geometrybullet.png'), 'alienbullet3.png':imgload('alienbullet3.png'),\
'alienbullet4.png':imgload('alienbullet4.png'), 'shurikenbullet.png':imgload('shurikenbullet.png') , 'alienbullet5.png':imgload('alienbullet5.png'),
'shotgunbullet.png':imgload('shotgunbullet.png')}"""

# Used for mathematical calculations: getting angles to/from unit vectors
def getHeadingFromAngle(angle):
	x = sin(angle*3.14/180.)
	y = cos(angle*3.14/180.)
	heading = Vector(x, y)
	return heading
def getAngleFromHeading(heading):
	angle = float(atan2(heading.y, heading.x))
	return angle
# A simple timer
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
		return

# Loads an image and sets its colorkey
def imgload(imgfile, colorkey=(255, 255, 255), imaged=True):
	try:
		if imaged:
			img = pygame.image.load(os.path.join('images', imgfile))
		else:
			img = pygame.image.load(imgfile)
	except pygame.error, error_message:
		raise SystemExit, error_message
	img.set_colorkey(colorkey)
	return img

# Loads all sounds in the 'sounds' subfolder
def loadSounds():
	sounds = {}
	for sound in os.listdir(os.getcwd()):
		if sound[-4:] == '.ogg':
			sounds[sound[0:-4]] = pygame.mixer.Sound(sound)
	return sounds
# Loads all images in the './images/bulletimages' subfolder into a dict and returns it
def loadBulletImages():
	bulletimages = {}
	imagepath = os.path.join(os.getcwd(), 'images')
	bulletpath = os.path.join(imagepath, 'bulletimages')
	for imagename in os.listdir(bulletpath):
		image = imgload(os.path.join(bulletpath, imagename), imaged=False)
		bulletimages[imagename] = image
	return bulletimages

