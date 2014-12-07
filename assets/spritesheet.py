from xml.etree import ElementTree
from extlib.gameobjects.vector2 import Vector2

from asset import Asset
import pygame
import utils
import os


class Frame:
    """
    A frame combines 2 infos : the texture id in opengl memory and coordinate of the picture to display.
    It can be passed directly to the rendered in order to draw it.
    """
    def __init__(self, textureid, coords, size):
        self.__coords = coords
        self.__textureid = textureid
        self.__size = size

    @property
    def texid(self):
        return self.__textureid

    @property
    def coords(self):
        return self.__coords

    @property
    def size(self):
        return self.__size


class FrameSet:
    """
    A frameset is a group of frames. It give access to every frame with a __getitem__ method.
    """
    def __init__(self, textureid, coords, size):
        self.__frames = []

        for coord in coords:
            self.__frames.append(Frame(textureid, coord, size))

    def __getitem__(self, item):
        return self.__frames[item]

    def __iter__(self):
        return iter(self.__frames)


class SpriteSheet(Asset):
    """
    a spritesheet is a group of namesd framesets created after an xml file and a png file.
    """
    def __init__(self, path):
        Asset.__init__(self)
        self.__path = path
        self.__framesets = {}

    def load(self):
        Asset.load(self)
        xmlfile = ElementTree.parse(os.path.join(self.__path, 'data.xml'))
        image = pygame.image.load(os.path.join(self.__path, xmlfile.findall('./filename')[0].text))

        textureid = utils.createtexture(image)

        framewidth = int(xmlfile.findall('./framewidth')[0].text)
        frameheight = int(xmlfile.findall('./frameheight')[0].text)

        hnb = image.get_width() / framewidth
        vnb = image.get_height() / frameheight

        for fs in xmlfile.findall('./animation'):
            name = fs.findall('./name')[0].text

            beginframe = int(fs.findall('./beginframe')[0].text)
            endframe = int(fs.findall('./endframe')[0].text)

            coords = []

            i = 1
            for y in range(1, vnb + 1):
                for x in range(1, hnb + 1):
                    if i in range(beginframe, endframe + 1):
                        coords.append((
                            (x - 1) * 1/float(hnb),
                            1 - (y - 1) * 1/float(vnb),
                            x * 1/float(hnb),
                            1 - y * 1/float(vnb)))
                    i += 1
            self.__framesets[name] = FrameSet(textureid, coords, Vector2(framewidth, frameheight))

    def unload(self):
        if self.loaded:
            Asset.unload(self)
            texid = int(self.__framesets.values()[0][0].texid)
            utils.unloadtexture(texid)
            self.__framesets = {}

    def __getattr__(self, item):
        if self.loaded:
            return self.__framesets[item]
        else:
            Asset._missingasset(self)