from gameobjects import GameObject
from locals import Tags
from extlib.gameobjects.vector2 import Vector2

import pygame


class CollisionManager(GameObject):
    def __init__(self, d):
        GameObject.__init__(self, d, Tags.COLLISIONMANAGER, Tags.UPDATABLE)

    def update(self, tick):
        physics = self._directory.get(Tags.PHYSIC)

        for o1 in physics:
            for o2 in physics:
                if o1.rigidbody.collider.colliderect(o2.rigidbody.collider) and o1 != o2:
                    o1.position.conform(o2)
                    o1.rigidbody.rest()

