from locals import Parameters
from locals import Tags

import pygame
import gameobjects
import opengl


class Renderer(gameobjects.GameObject):
    def __init__(self, d):
        gameobjects.GameObject.__init__(self, d, Tags.RENDERER)

        pygame.init()
        #opengl.clear()
        pygame.display.set_mode(Parameters.SSIZE, Parameters.FLAGS)

    def draw(self, betweenframe):
        opengl.clear()

        for sprite in self._directory.get(Tags.VISIBLE):
            opengl.drawframe(sprite.frame, sprite.position.getrenderposition(betweenframe), sprite.frame.size)

        pygame.display.flip()


