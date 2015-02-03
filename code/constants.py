#! usr/bin/env python
# All in-game constants
import pygame

# Frames per second the game will try to run at
FPS = 35
# Width of application window
WIDTH = 480
# Height of application window
HEIGHT = 640
# Control mechanism, choose between 'keyboard' and 'mouse'
CONTROL = 'mouse'
# A convienence variable
BLACK = (1, 1, 1)
# Key code definitions
UPKEY = pygame.K_UP
DOWNKEY = pygame.K_DOWN
RIGHTKEY = pygame.K_RIGHT
LEFTKEY = pygame.K_LEFT
SHOOTKEY = pygame.K_a
SLOWKEY = pygame.K_LSHIFT
# Used for defining the player's hitbox
XINFLATION = -23
YINFLATION = -20
