from locals import Parameters
from locals import Tags

from gameobjects.gameobjects import *

import pygame
import opengl


class Renderer(GameObject):
    def __init__(self, d):
        GameObject.__init__(self, d, Tags.RENDERER)

        pygame.init()

        pygame.display.set_mode(Parameters.SSIZE, Parameters.FLAGS)
        opengl.clear()

    def draw(self, betweenframe):
        opengl.clear()

        for sprite in self._directory.get(Tags.VISIBLE):
            opengl.drawframe(sprite.frame, sprite.position.getrenderposition(betweenframe), sprite.frame.size)

        pygame.display.flip()


