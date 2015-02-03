#! usr/bin/env python
# The definitions for all *things* that appear in-game.
from util import imgload
import pygame
import random

# Base class. Don't create instances of this directly
class GameObj(pygame.sprite.Sprite):
	def __init__(self, world):
		pygame.sprite.Sprite.__init__(self)
		self.name = ''
	def update(self, world):
		pass

# Just a sparkling particle used for effects.
# It goes straight down, like the player is moving forwards
class Star(GameObj):
	def __init__(self, pos, speed):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect((pos), (2, 2))
		self.speed = speed
		self.name = 'star'
	def update(self, world):
		self.rect = self.rect.move(self.speed)
		if self.rect.bottom > world.height:
			world.kill(self)
		surface = pygame.Surface(self.rect.size)
		surface.fill([random.randint(70, 255), random.randint(70, 255), random.randint(70, 255)])
		world.blit(surface, self.rect)
		return

# A particle used for effects
class Particle(GameObj):
	def __init__(self, pos, speed, size, length, color=[255, 255, 255]):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(pos, size)
		self.speed = speed
		self.length = length
		self.color = color
		self.name = 'particle'
	def update(self, world):
		self.rect = self.rect.move(self.speed)
		self.length -= 1
		if self.length <= 0:
			world.kill(self)
		pygame.draw.rect(world.screen, self.color, self.rect)
		return

