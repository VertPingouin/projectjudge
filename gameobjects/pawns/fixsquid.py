from gameobjects.gameobjects import *
import pygame


class FixSquid(GameObject):
    def __init__(self, d, position, frame, depth, *tags):
        GameObject.__init__(self, d, Tags.VISIBLE, Tags.UPDATABLE, Tags.PHYSIC, *tags)

        self.__frame = frame
        self.__depth = depth

        self.activity = Activity(self, None)

        self.position = Position(
            owner=self,
            position=position,
        )


    def update(self, tick):
        pass


    @property
    def frame(self):
        return self.__frame

    @property
    def depth(self):
        return self.__depth