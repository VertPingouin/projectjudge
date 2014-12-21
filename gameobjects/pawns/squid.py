from gameobjects.gameobjects import *
import pygame

class Squid(GameObject):
    def __init__(self, d, position, frame, depth, *tags):
        GameObject.__init__(self, d, Tags.VISIBLE, Tags.UPDATABLE, Tags.PHYSIC, *tags)

        self.__frame = frame
        self.__depth = depth

        self.activity = Activity(self, None)

        self.position = Position(
            owner=self,
            position=position,
        )

        self.rigidbody = RigidBody(
            owner=self,
            collider=BoxCollider(owner=self, box=pygame.Rect(0, 0, 24, 32)),
        )

    def update(self, tick):
        self.rigidbody.update(tick)


    @property
    def frame(self):
        return self.__frame

    @property
    def depth(self):
        return self.__depth