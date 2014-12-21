from gameobjects.gameobjects import *
import pygame


class Blocker(GameObject):
    def __init__(self, d, position, size, depth, *tags):
        GameObject.__init__(self, d, Tags.PHYSIC, Tags.BLOCKER, *tags)

        self.__depth = depth

        self.position = Position(
            owner=self,
            position=position,
        )

        self.rigidbody = RigidBody(
            owner=self,
            collider=BoxCollider(owner=self, box=pygame.Rect((0, 0), size)),
            gravityscale=1.0,
            lineardrag=0.95,
            iskinematic=True
        )