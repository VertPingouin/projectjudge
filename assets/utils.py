from OpenGL.GL import *
import pygame


def createtexture(pygamesurface):
    rect = pygamesurface.get_rect()
    texturedata = pygame.image.tostring(pygamesurface, "RGBA", 1)

    textureindex = glGenTextures(1)
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, textureindex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 rect.width, rect.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, texturedata)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

    return textureindex


def unloadtexture(id):
    glDeleteTextures(id)