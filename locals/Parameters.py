from extlib.gameobjects.vector2 import Vector2
import pygame

GRAVITY = Vector2(0, 2000)

GAMETICKS = 30
AGAMETICKS = 2
GAMESPEED = 1.0
FPSLIMIT = 30

REFHRES = Vector2(480, 270)
_multiple = 2
SSIZE = int(_multiple * REFHRES[0]), int(_multiple * REFHRES[1])
FLAGS = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE
SCENESIZE = Vector2(480, 270)
GRIDRESOLUTION = 32


