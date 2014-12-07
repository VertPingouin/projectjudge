from OpenGL.GL import *
from OpenGL.GLU import *
from locals import Parameters


def applyortho2d(left, right, bottom, top):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(left, right, bottom, top)
    glPushMatrix()
    glPopMatrix()
    glFlush()


def defineviewport(wi, hi):
    glViewport(0, 0, wi, hi)


def pixelcoord(oglc, scenesize):
    # transform opengl coordinates into pixel coordinates
    return (oglc[0] * float(scenesize[0]))/2, (1 + oglc[1] * float(scenesize[1]))/2


def oglcoord(pixcoord, scenesize):
    # transform pixel coordinates into opengl coordinates
    return 2*(pixcoord[0] / float(scenesize[0])), 2*(pixcoord[1] / float(scenesize[1]))


def oglsize(pixsize, scenesize):
    # transform pixel size into opengl size
    return pixsize[0] / float(scenesize[0]), pixsize[1] / float(scenesize[1])


def clear():
    glClear( GL_COLOR_BUFFER_BIT)


def drawframe(frame, pos, siz, proj=True, r=1.0, g=1.0, b=1.0, alpha=1.0):
    if proj:
        glMatrixMode(GL_MODELVIEW)
    else:
        glMatrixMode(GL_PROJECTION)

    pos = oglcoord(pos, Parameters.SCENESIZE)
    siz = oglsize(siz, Parameters.SCENESIZE)

    glLoadIdentity()
    glPushMatrix()

    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glTranslated(-1, 1, 0)
    glScalef(1, -1, 1)
    glTranslated(pos[0]+siz[0], pos[1]+siz[1], 0)
    glScalef(siz[0], siz[1], 1)

    glColor4f(r, g, b, alpha)

    glBindTexture(GL_TEXTURE_2D, frame.texid)

    glBegin(GL_QUADS)

    glTexCoord2f(frame.coords[0], frame.coords[1])
    glVertex2f(-1.0, -1.0)

    glTexCoord2f(frame.coords[2], frame.coords[1])
    glVertex2f(1.0, -1.0)

    glTexCoord2f(frame.coords[2], frame.coords[3])
    glVertex2f(1.0, 1.0)

    glTexCoord2f(frame.coords[0], frame.coords[3])
    glVertex2f(-1.0, 1.0)

    glEnd()
    glPopMatrix()
    # glFlush()

